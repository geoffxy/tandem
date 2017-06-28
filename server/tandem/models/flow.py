from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from tandem.database.instances import postgres


class Flow(postgres.DeclarativeBase):
    __tablename__ = 'flows'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(255))
    frequency = Column('frequency', Integer)
    viewport = Column('viewport', postgresql.ARRAY(Integer, dimensions=1))
    actions = relationship("Action")

    def __init__(self, name, frequency, viewport):
        self.name = name
        self.frequency = frequency
        self.viewport = viewport

    def add_action(self, action):
        pass
