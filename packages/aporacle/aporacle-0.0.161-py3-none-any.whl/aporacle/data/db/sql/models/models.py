from datetime import datetime, timedelta

from komoutils.core.time import the_time_now_is
from sqlalchemy import Column, Integer, inspect, Index, Float, String, JSON, Boolean, UniqueConstraint

from aporacle.data.db.sql.data_view_base import Base


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


class Evaluation(Base):
    __tablename__ = "Evaluation"
    __table_args__ = (
        UniqueConstraint('chain', 'voting_round', 'feed', 'name', name='uq_evaluation'),
        Index("os_chain_feed_name_index", "chain", "feed", "name")
    )

    id = Column(String(255), primary_key=True, nullable=False)
    chain = Column(String(255), nullable=False)
    voting_round = Column(Integer, nullable=False)
    feed = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    prediction = Column(Float, nullable=False)
    price = Column(Float, nullable=True)
    correction_factor = Column(Float, nullable=True)
    avg_correction_error = Column(Float, nullable=True)  # Average Correction Error
    avg_last_n_corrections = Column(Float, nullable=True)  # Average of Last N Corrections
    timestamp = Column(String(255), nullable=False)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @staticmethod
    def clear_old_records(session):
        six_hours_ago = datetime.utcnow() - timedelta(seconds=60 * 60 * 24)  # 24 hours
        session.query(Evaluation).filter(Evaluation.timestamp < six_hours_ago.isoformat()).delete()
        session.commit()


class FeedResult(Base):
    __tablename__ = "FeedResult"
    __table_args__ = (Index("os_feed_result_chain_voting_round_feed_index",
                            "chain", "voting_round", "feed"),
                      )

    id = Column(String(255), primary_key=True, nullable=False)  # Changed from Text to String(255)
    chain = Column(String(255), nullable=False)  # Changed from Text to String(255)
    voting_round = Column(Integer, nullable=False)
    feed = Column(String(255), nullable=False)  # Changed from Text to String(255)
    price = Column(Float, nullable=True)
    upper = Column(Float, nullable=True)
    lower = Column(Float, nullable=True)
    rewarded = Column(Boolean, nullable=False, default=False)
    timestamp = Column(String(255), nullable=False)  # Changed from Text to String(255)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @staticmethod
    def clear_old_records(session):
        six_hours_ago = datetime.utcnow() - timedelta(seconds=60 * 60 * 24)  # 24 hours
        session.query(FeedResult).filter(FeedResult.timestamp < six_hours_ago.isoformat()).delete()
        session.commit()


class Metadata(Base):
    __tablename__ = "Metadata"

    key = Column(String(255), primary_key=True, nullable=False)
    value = Column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"Metadata(key='{self.key}', value='{self.value}')"


class Prediction(Base):
    __tablename__ = "Prediction"
    __table_args__ = (UniqueConstraint('chain', 'voting_round', 'feed', 'name', name='uq_prediction'),)

    id = Column(String(255), primary_key=True, nullable=False)
    chain = Column(String(255), nullable=False)
    voting_round = Column(Integer, nullable=False)
    feed = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    prediction = Column(Float, nullable=False)
    timestamp = Column(String(255), nullable=False)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @staticmethod
    def clear_old_records(session):
        six_hours_ago = datetime.utcnow() - timedelta(seconds=60)
        session.query(Prediction).filter(Prediction.timestamp < six_hours_ago.isoformat()).delete()
        session.commit()


class PreparedSymbol(Base):
    __tablename__ = "PreparedSymbol"

    id = Column(String(255), primary_key=True, nullable=False)
    chain = Column(String(255), nullable=False)
    voting_round = Column(Integer, nullable=False)
    feed = Column(String(255), nullable=False)
    symbol = Column(String(255), nullable=False)
    model_name = Column(String(255), nullable=False)
    data = Column(JSON, nullable=True)
    data_sizes = Column(Integer, nullable=True)
    timestamp = Column(String(255), nullable=False)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @staticmethod
    def clear_old_records(session):
        one_minute = datetime.utcnow() - timedelta(minutes=1)
        session.query(PreparedSymbol).filter(PreparedSymbol.timestamp < one_minute.isoformat()).delete()
        session.commit()


class Provider(Base):
    __tablename__ = "Provider"

    id = Column(String(255), primary_key=True, nullable=False)
    chain = Column(String(255), nullable=False)
    reward_epoch = Column(Integer, nullable=True)
    reward_epoch_start = Column(Float, nullable=True)
    reward_epoch_end = Column(Float, nullable=True)
    voting_round = Column(Integer, nullable=False)
    voting_round_start = Column(Float, nullable=False)
    voting_round_end = Column(Float, nullable=False)
    voting_round_submission_start_buffer = Column(Integer, nullable=False, default=20)
    voting_round_submission_end_buffer = Column(Integer, nullable=False, default=10)
    feeds = Column(JSON, nullable=False)
    voters = Column(JSON, nullable=False)
    commits = Column(JSON, nullable=True)
    reveals = Column(JSON, nullable=True)
    timestamp = Column(String(255), nullable=False)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Submission(Base):
    __tablename__ = "Submission"

    id = Column(String(255), primary_key=True, nullable=False)
    chain = Column(String(255), nullable=False)
    voting_round = Column(Integer, nullable=False)
    feed = Column(String(255), nullable=False)
    algorithm_name = Column(String(255), nullable=False)
    submission = Column(Float, nullable=False)
    is_default = Column(Boolean, nullable=False, default=False)
    timestamp = Column(String(255), nullable=False)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @staticmethod
    def clear_old_records(session):
        six_hours_ago = datetime.utcnow() - timedelta(seconds=60 * 60 * 24)  # 24 hours
        session.query(Submission).filter(Submission.timestamp < six_hours_ago.isoformat()).delete()
        session.commit()


class TrainedModel(Base):
    __tablename__ = "TrainedModel"
    __table_args__ = (Index("os_chain_feed_name_target_index", "chain", "feed", "name", "target"),)

    id = Column(String(255), primary_key=True, nullable=False)
    chain = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    feed = Column(String(255), nullable=False)
    symbols = Column(JSON, nullable=False)
    model_type = Column(String(255), nullable=False)
    r2 = Column(Float, nullable=False)
    rmse = Column(Float, nullable=False)
    feature_count = Column(Float, nullable=True)
    target = Column(Integer, nullable=True)
    scaler_mean = Column(JSON, nullable=True)
    scaler_scale = Column(JSON, nullable=True)
    coefficients = Column(JSON, nullable=True)
    intercept = Column(Float, nullable=True)
    performance = Column(JSON, nullable=True, default={})
    ranking = Column(Integer, nullable=True, default=0)
    last_evaluation_voting_round = Column(Integer, nullable=True, default=0)
    last_evaluation_time = Column(String(255), nullable=True, default='')
    running = Column(Integer, nullable=True, default=0)
    predicting = Column(Integer, nullable=True, default=0)
    # Metrics columns
    running_r_squared = Column(Float, nullable=True, default=0)  # R² (R-squared) - Running evaluation metric
    directional_accuracy = Column(Float, nullable=True)  # Directional Accuracy
    overestimation_frequency = Column(Float, nullable=True)  # Overestimation Frequency
    underestimation_frequency = Column(Float, nullable=True)  # Underestimation Frequency
    average_overestimation_degree = Column(Float, nullable=True)  # Average Overestimation Degree
    average_underestimation_degree = Column(Float, nullable=True)  # Average Underestimation Degree

    correction_factor = Column(Float, nullable=True)  # Running Correction Factor (if applicable)
    avg_correction_error = Column(Float, nullable=True)  # Average Correction Error
    avg_last_n_corrections = Column(Float, nullable=True)  # Average of Last N Corrections

    mae = Column(Float, nullable=True)  # Mean Absolute Error (MAE)
    rmse_metric = Column(Float, nullable=True)  # Root Mean Squared Error (RMSE)
    mape = Column(Float, nullable=True)  # Mean Absolute Percentage Error (MAPE)
    prediction_stability = Column(Float, nullable=True)  # Prediction Stability (e.g., standard deviation)
    complexity_penalty = Column(Float, nullable=True)  # Complexity Penalty (if applicable)
    timestamp = Column(String(255), nullable=False, default=the_time_in_iso_now_is())

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Transaction(Base):
    __tablename__ = "Transaction"
    __table_args__ = (Index("os_chain_voting_round_tag_index",
                            "chain", "voting_round", "tag"),
                      )

    id = Column(String(255), primary_key=True, nullable=False)
    chain = Column(String(255), nullable=False)
    reward_epoch = Column(Integer, nullable=False)
    voting_round = Column(Integer, nullable=False)
    tag = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    payload = Column(String(1024), nullable=False)
    valid = Column(Boolean, nullable=False, default=True)
    timestamp = Column(String(255), nullable=False)
    created_at = Column(Float, default=the_time_now_is())
    ttl = Column(Integer, default=360)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Voter(Base):
    __tablename__ = "Voter"
    # Define a composite index key
    __table_args__ = (
        Index('os_entity_submit_index', "entity_address", "submit_address"),  # Create the index
    )

    id = Column(String(255), primary_key=True, nullable=False)
    chain = Column(String(255), nullable=False)
    # name = Column(String(255), default='', nullable=False)
    entity_address = Column(String(255), nullable=False)
    submit_address = Column(String(255), nullable=False)
    submit_signature_address = Column(String(255), nullable=False)
    signing_policy_address = Column(String(255), nullable=False)
    delegation_address = Column(String)
    # sortition_addresses = relationship("SortitionAddress", backref="voter")
    reward_epoch = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    last_update_at_timestamp = Column(String(255), nullable=False)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
