from sqlalchemy import Column, Integer, inspect, Index, Float, String

from aporacle.data.db.sql.models import FlareProofsBase


class Voter(FlareProofsBase):
    __tablename__ = "Voter"
    # Define a composite index key
    __table_args__ = (
        Index('os_entity_submit_index', "entity_address", "submit_address"),  # Create the index
    )

    id = Column(String(255), primary_key=True, nullable=False)
    chain = Column(String(255), nullable=False)
    # name = Column(String, default='', nullable=False)
    entity_address = Column(String, nullable=False)
    submit_address = Column(String, nullable=False)
    submit_signature_address = Column(String, nullable=False)
    signing_policy_address = Column(String, nullable=False)
    delegation_address = Column(String)
    # sortition_addresses = relationship("SortitionAddress", backref="voter")
    reward_epoch = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    last_update_at_timestamp = Column(String(255), nullable=False)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}