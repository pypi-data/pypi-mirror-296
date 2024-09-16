import logging
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import importlib
import glob
from enum import Enum
from komoutils.core import KomoBase


class ArtifactManagementMode(Enum):
    CREATE_IF_NOT_EXISTS = 1
    RESET_ALL = 2


class DataViewBase(KomoBase):  # Changed class name here
    def __init__(self):
        # Hardcoded database credentials
        db_name = "ftsodb"
        db_user = "root"
        db_password = "example"

        self.db_app_user = 'ftsodb'
        self.db_app_password = 'ftsodb'

        # Get environment variables for host and port
        db_host = os.getenv('DB_HOST') or "127.0.0.1"
        db_port = os.getenv('DB_PORT') or 3306

        # Create the fully formed db_url for SQLAlchemy
        db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/"

        self.engine = create_engine(db_url)
        self.session = sessionmaker(bind=self.engine)

        # Ensure the database exists
        self.ensure_database_exists(db_name, db_user, db_password)

    def ensure_database_exists(self, db_name, db_user, db_password):
        try:
            with self.session() as session:
                # Check if the database exists
                result = session.execute(text("SHOW DATABASES LIKE :db_name"), {'db_name': db_name})
                if not result.fetchone():
                    # Create the database
                    session.execute(text(f"CREATE DATABASE {db_name}"))
                    self.log_with_clock(log_level=logging.INFO, msg=f"Database '{db_name}' created.")

                    # Create user with read and write rights
                    session.execute(text(f"CREATE USER '{self.db_app_user}'@'%' IDENTIFIED BY '{self.db_app_password}'"))
                    session.execute(text(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{self.db_app_user}'@'%'"))
                    self.log_with_clock(log_level=logging.INFO,
                                        msg=f"User '{self.db_app_user}' created with privileges on '{db_name}'.")
                else:
                    self.log_with_clock(log_level=logging.INFO, msg=f"Database '{db_name}' already exists.")
        except SQLAlchemyError as e:
            self.log_with_clock(log_level=logging.ERROR, msg=f"Error ensuring database existence: {str(e)}")

    def check_db_connection(self):
        try:
            with self.session() as session:
                session.execute(text("SELECT 1"))
            self.log_with_clock(log_level=logging.INFO, msg="Database connection successful.")
            return True
        except SQLAlchemyError as e:
            self.log_with_clock(log_level=logging.ERROR, msg=f"Error connecting to the database: {str(e)}")
            return False

    def manage_artifacts(self, mode=ArtifactManagementMode.CREATE_IF_NOT_EXISTS):
        if not self.check_db_connection():
            self.log_with_clock(log_level=logging.ERROR,
                                msg="Cannot manage artifacts due to database connection error.")
            return

        with self.session() as session:
            if mode == ArtifactManagementMode.RESET_ALL:
                self._reset_all_artifacts(session)
            self._create_tables(session)
            self._create_triggers(session)
            self._create_views(session)
            self._create_stored_procedures(session)  # New method call

    def _reset_all_artifacts(self, session):
        self.log_with_clock(log_level=logging.INFO, msg="Resetting all artifacts...")
        # Drop views
        view_names = self._get_existing_views(session)
        for view_name in view_names:
            session.execute(text(f"DROP VIEW IF EXISTS {view_name}"))

        # Drop triggers
        trigger_names = self._get_existing_triggers(session)
        for trigger_name in trigger_names:
            session.execute(text(f"DROP TRIGGER IF EXISTS {trigger_name}"))

        # Drop tables
        table_models = self._load_modules('models')
        for model in reversed(table_models):  # Reverse to handle dependencies
            model.metadata.drop_all(self.engine)

        session.commit()
        self.log_with_clock(log_level=logging.INFO, msg="All artifacts have been reset.")

    def _get_existing_views(self, session):
        result = session.execute(text("SHOW FULL TABLES WHERE Table_type = 'VIEW'"))
        return [row[0] for row in result]

    def _get_existing_triggers(self, session):
        result = session.execute(text("SHOW TRIGGERS"))
        return [row[0] for row in result]

    def _create_tables(self, session):
        self.log_with_clock(log_level=logging.INFO, msg="Creating tables...")
        table_models = self._load_modules('models')
        for model in table_models:
            model.metadata.create_all(self.engine)
        self.log_with_clock(log_level=logging.INFO, msg="Tables created.")

    def _create_triggers(self, session):
        self.log_with_clock(log_level=logging.INFO, msg="Creating triggers...")
        trigger_files = glob.glob(os.path.join(os.path.dirname(__file__), '..', 'triggers', '*.sql'))
        for trigger_file in trigger_files:
            with open(trigger_file, 'r') as f:
                trigger_sql = f.read()
            session.execute(text(trigger_sql))
        session.commit()
        self.log_with_clock(log_level=logging.INFO, msg="Triggers created.")

    def _create_views(self, session):
        self.log_with_clock(log_level=logging.INFO, msg="Creating views...")
        view_files = glob.glob(os.path.join(os.path.dirname(__file__), '..', 'views', '*.sql'))
        for view_file in view_files:
            with open(view_file, 'r') as f:
                view_sql = f.read()
            session.execute(text(view_sql))
        session.commit()
        self.log_with_clock(log_level=logging.INFO, msg="Views created.")

    def _create_stored_procedures(self, session):
        self.log_with_clock(log_level=logging.INFO, msg="Creating stored procedures...")
        procedure_files = glob.glob(os.path.join(os.path.dirname(__file__), '..', 'procedures', '*.sql'))
        for procedure_file in procedure_files:
            with open(procedure_file, 'r') as f:
                procedure_sql = f.read()
            session.execute(text(procedure_sql))
        session.commit()
        self.log_with_clock(log_level=logging.INFO, msg="Stored procedures created.")

    def _load_modules(self, folder_name):
        module_files = glob.glob(os.path.join(os.path.dirname(__file__), '..', folder_name, '*.py'))
        modules = []
        for module_file in module_files:
            module_name = os.path.basename(module_file)[:-3]  # Remove .py extension
            module = importlib.import_module(f'aporacle.data.db.sql.{folder_name}.{module_name}')
            modules.append(module)
        return modules
