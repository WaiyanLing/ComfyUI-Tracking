from datetime import datetime

from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime, and_, or_, Text, Date, func, JSON, VARCHAR
from sqlalchemy.orm import sessionmaker

from .connect_db import get_engine

Base = declarative_base()

class Record(Base):
    __tablename__ = 'record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_key = Column(VARCHAR(128), nullable=False, comment="user_key")
    session_id = Column(VARCHAR(128), nullable=False, comment="session_id")
    workflow_id = Column(VARCHAR(128), nullable=False, comment="workflow_id")
    workflow = Column(JSON, nullable=False, comment="workflow")
    result = Column(JSON, nullable=False, comment="result_so_far")
    create_time = Column(DateTime, nullable=False, comment="create_time")

class RecordManager(object):
    def __init__(self, engine: Engine = get_engine("workflow_tracking")):
        self._eg = engine
        self.is_exist_table()

    def is_exist_table(self):
        has_table = self._eg.dialect.has_table(self._eg.connect(), "workflow_tracking")
        if not has_table:
            Base.metadata.create_all(self._eg)
        return True

    def add_record(
            self,
            ts: Record
    ) -> bool:
        Session = sessionmaker(bind=self._eg)
        session = Session()
        now = datetime.now()
        ts.create_time = now
        session.add(ts)
        session.commit()
        session.close()
        return True
