#!/usr/bin/env python

from sqlalchemy import (
    Column,
    String,
)

from aporacle.data.db.sql.models import FlareProofsBase


class Metadata(FlareProofsBase):
    __tablename__ = "Metadata"

    key = Column(String(255), primary_key=True, nullable=False)
    value = Column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"Metadata(key='{self.key}', value='{self.value}')"
