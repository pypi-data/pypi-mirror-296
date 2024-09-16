from sqlalchemy import Column, Integer, inspect, Index, Float, String

from aporacle.data.db.sql.models import Base


class Feed(Base):
    __tablename__ = "Feed"
    __table_args__ = (
        Index("os_feed_base_quote_index", "feed", "base", "quote"),
    )

    id = Column(String(255), primary_key=True, nullable=False)
    chain = Column(String(255), nullable=False)
    feed = Column(String(255), nullable=False)
    base = Column(String(255), nullable=True)
    quote = Column(String(255), nullable=True)
    address = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    decimals = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    start_collecting_data_at_timestamp = Column(Float, default=0, nullable=True)
    end_collecting_data_at_timestamp = Column(Float, default=0, nullable=True)
    begin_support_at_timestamp = Column(Float, default=0, nullable=True)
    end_support_at_timestamp = Column(Float, default=0, nullable=True)
    last_update_at_timestamp = Column(String(255), nullable=False)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}