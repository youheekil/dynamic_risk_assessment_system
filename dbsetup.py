import sqlalchemy as _sqlalchemy
from sqlalchemy import Column, String, Integer, Boolean
import psycopg2

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/postgres"

engine = _sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = _sqlalchemy.sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=engine)

Base = _sqlalchemy.declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Model
class FinalData(Base):
    __tablename__ = "finaldata"
    id = Column(Integer, primary_key=True, nullable=False)
    corporation = Column(String)
    lastmonth_activity = Column(Integer)
    lastyear_activity = Column(Integer)
    number_of_employee = Column(Integer)
    exited = Column(Boolean)

