from .database import Base, SessionLocal, engine
from .models import Users

Base.metadata.create_all(bind=engine)
