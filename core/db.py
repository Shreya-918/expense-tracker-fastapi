#configuration about database
from sqlalchemy import create_engine
from sqlalchemy.orm import Session,sessionmaker,DeclarativeBase
DATABASE_URL="sqlite:///./expense_new.db"

#craete engine
engine=create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

#sessional
SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#dependency

def get_db():
    db=SessionLocal()
    try :
        yield db
    finally:
        db.close()
class Base(DeclarativeBase):
    pass
