import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class EnrollmentRecord(Base):
    __tablename__ = "enrollment_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    upload_id: Mapped[str] = mapped_column(String(36), ForeignKey("uploads.id"), index=True)
    full_name: Mapped[str] = mapped_column(String(255), index=True)
    normalized_name: Mapped[str] = mapped_column(String(255), index=True)
    hei_name: Mapped[str] = mapped_column(String(255), index=True)
    academic_year: Mapped[str] = mapped_column(String(50), index=True)
    semester: Mapped[str] = mapped_column(String(50), index=True)
    source_row: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
