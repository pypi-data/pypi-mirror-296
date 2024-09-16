from sqlalchemy.ext.declarative import declarative_base

FlareProofsBase = declarative_base()


def get_declarative_base():
    from .metadata import Metadata  # noqa: F401
    return FlareProofsBase
