import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Upload(Base):
    __tablename__ = "uploads"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    upload_type: Mapped[str] = mapped_column(String(50), nullable=False)
    hei_name: Mapped[str] = mapped_column(String(255), index=True)
    academic_year: Mapped[str] = mapped_column(String(50), index=True)
    semester: Mapped[str] = mapped_column(String(50), index=True)
    scholarship: Mapped[str] = mapped_column(String(50), nullable=True)
    batch: Mapped[str] = mapped_column(String(50), nullable=True)
    uploaded_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    row_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(50), default="processed")
