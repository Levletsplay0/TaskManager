from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String)
    token = Column(String, nullable=True, unique=True)

class Projects(Base):
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    owner_id = Column(Integer, nullable=False)

    tasks = relationship("Tasks", back_populates="project", cascade="all, delete-orphan")



class Tasks(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)

    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_completed = Column(Boolean, default=False, nullable=False)

    project = relationship("Projects", back_populates="tasks")