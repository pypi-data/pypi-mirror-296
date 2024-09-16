import logging
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import importlib
import glob
from enum import Enum
from komoutils.core import KomoBase
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ArtifactManagementMode(Enum):
    CREATE_IF_NOT_EXISTS = 1
    RESET_ALL = 2


class DataViewBase(KomoBase):
    def __init__(self):
        # Hardcoded database credentials
        self.db_name = "ftsodb"
        self.db_user = "root"
        self.db_password = "example"

        self.db_app_user = 'ftsodb'
        self.db_app_password = 'ftsodb'

        # Get environment variables for host and port
        self.db_host = os.getenv('DB_HOST') or "127.0.0.1"
        self.db_port = os.getenv('DB_PORT') or 3306

        # Create the fully formed db_url for SQLAlchemy
        self.db_url = f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}"

        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)

    def ensure_database_exists(self):
        try:
            with self.engine.connect() as connection:
                # Check if the database exists
                result = connection.execute(text(f"SHOW DATABASES LIKE '{self.db_name}'"))
                if not result.fetchone():
                    # Create the database
                    connection.execute(text(f"CREATE DATABASE {self.db_name}"))
                    self.log_with_clock(log_level=logging.INFO, msg=f"Database '{self.db_name}' created.")

                    # Check if user exists
                    result = connection.execute(text(f"SELECT 1 FROM mysql.user WHERE user = '{self.db_app_user}'"))
                    if not result.fetchone():
                        # Create user with read and write rights
                        connection.execute(
                            text(f"CREATE USER '{self.db_app_user}'@'%' IDENTIFIED BY '{self.db_app_password}'"))
                        self.log_with_clock(log_level=logging.INFO, msg=f"User '{self.db_app_user}' created.")

                    # Grant privileges (do this even if user already exists)
                    connection.execute(text(f"GRANT ALL PRIVILEGES ON {self.db_name}.* TO '{self.db_app_user}'@'%'"))
                    self.log_with_clock(log_level=logging.INFO,
                                        msg=f"Privileges granted to '{self.db_app_user}' on '{self.db_name}'.")
                else:
                    self.log_with_clock(log_level=logging.INFO, msg=f"Database '{self.db_name}' already exists.")

                # Use the database
                connection.execute(text(f"USE {self.db_name}"))
        except SQLAlchemyError as e:
            self.log_with_clock(log_level=logging.ERROR, msg=f"Error ensuring database existence: {str(e)}")

    def check_db_connection(self):
        try:
            with self.Session() as session:
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

        with self.Session() as session:
            if mode == ArtifactManagementMode.RESET_ALL:
                self._reset_all_artifacts(session)

            # Always create tables first
            self._create_tables(session)

            # Then create other artifacts
            self._create_views()
            self._create_triggers()
            self._create_stored_procedures()

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

        # Drop stored procedures
        procedure_names = self._get_existing_procedures(session)
        for procedure_name in procedure_names:
            session.execute(text(f"DROP PROCEDURE IF EXISTS {procedure_name}"))

        # Drop tables
        table_models = self._load_modules('models')
        for model_module in table_models:
            for name, cls in model_module.__dict__.items():
                if isinstance(cls, type) and issubclass(cls, Base) and cls != Base:
                    cls.__table__.drop(self.engine, checkfirst=True)

        session.commit()
        self.log_with_clock(log_level=logging.INFO, msg="All artifacts have been reset.")

    def _get_existing_views(self, session):
        result = session.execute(text("SHOW FULL TABLES WHERE Table_type = 'VIEW'"))
        return [row[0] for row in result]

    def _get_existing_triggers(self, session):
        result = session.execute(text("SHOW TRIGGERS"))
        return [row[0] for row in result]

    def _get_existing_procedures(self, session):
        result = session.execute(text(f"SHOW PROCEDURE STATUS WHERE Db = '{self.db_name}'"))
        return [row[1] for row in result]

    def _create_tables(self, session):
        self.log_with_clock(log_level=logging.INFO, msg="Creating tables...")
        session.execute(text(f"USE {self.db_name}"))
        table_models = self._load_modules('models')
        for model_module in table_models:
            for name, cls in model_module.__dict__.items():
                if isinstance(cls, type) and issubclass(cls, Base) and cls != Base:
                    cls.__table__.schema = self.db_name  # Set the schema explicitly
                    cls.__table__.create(self.engine, checkfirst=True)
        session.commit()
        self.log_with_clock(log_level=logging.INFO, msg="Tables created.")

    def _create_triggers(self):
        self.log_with_clock(log_level=logging.INFO, msg="Creating triggers...")
        trigger_files = self._load_sql_files('triggers')
        with self.Session() as session:
            for trigger_file in trigger_files:
                with open(trigger_file, 'r') as f:
                    trigger_sql = f.read()
                session.execute(text(trigger_sql))
            session.commit()
        self.log_with_clock(log_level=logging.INFO, msg="Triggers created.")

    def _create_views(self):
        self.log_with_clock(log_level=logging.INFO, msg="Creating views...")
        view_files = self._load_sql_files('views')
        with self.Session() as session:
            session.execute(text(f"USE {self.db_name}"))  # Select the database
            for view_file in view_files:
                with open(view_file, 'r') as f:
                    view_sql = f.read()
                session.execute(text(view_sql))
            session.commit()
        self.log_with_clock(log_level=logging.INFO, msg="Views created.")

    def _create_stored_procedures(self):
        self.log_with_clock(log_level=logging.INFO, msg="Creating stored procedures...")
        procedure_files = self._load_sql_files('procedures')
        with self.Session() as session:
            session.execute(text(f"USE {self.db_name}"))  # Select the database
            for procedure_file in procedure_files:
                with open(procedure_file, 'r') as f:
                    procedure_sql = f.read()
                # Drop the procedure if it exists
                procedure_name = procedure_sql.split('CREATE PROCEDURE')[1].split('(')[0].strip()
                session.execute(text(f"DROP PROCEDURE IF EXISTS {procedure_name}"))
                # Create the procedure
                session.execute(text(procedure_sql))
            session.commit()
        self.log_with_clock(log_level=logging.INFO, msg="Stored procedures created.")

    def _load_modules(self, folder_name):
        module_path = os.path.join(os.path.dirname(__file__), folder_name)
        self.log_with_clock(log_level=logging.DEBUG, msg=f"Looking for modules in: {module_path}")
        module_files = glob.glob(os.path.join(module_path, '*.py'))
        self.log_with_clock(log_level=logging.DEBUG, msg=f"Found module files: {module_files}")
        modules = []
        for module_file in module_files:
            module_name = os.path.basename(module_file)[:-3]  # Remove .py extension
            if module_name == '__init__':
                continue  # Skip __init__.py
            full_module_name = f'aporacle.data.db.sql.{folder_name}.{module_name}'
            self.log_with_clock(log_level=logging.DEBUG, msg=f"Attempting to import: {full_module_name}")
            try:
                module = importlib.import_module(full_module_name)
                modules.append(module)
                self.log_with_clock(log_level=logging.DEBUG, msg=f"Successfully imported: {full_module_name}")
            except ImportError as e:
                self.log_with_clock(log_level=logging.ERROR, msg=f"Error importing module {full_module_name}: {str(e)}")
        return modules

    def _load_sql_files(self, folder_name):
        folder_path = os.path.join(os.path.dirname(__file__), folder_name)
        self.log_with_clock(log_level=logging.DEBUG, msg=f"Looking for SQL files in: {folder_path}")
        sql_files = glob.glob(os.path.join(folder_path, '*.sql'))
        self.log_with_clock(log_level=logging.DEBUG, msg=f"Found SQL files: {sql_files}")
        return sql_files
