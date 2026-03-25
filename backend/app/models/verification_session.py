import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class VerificationSession(Base):
    __tablename__ = "verification_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    grantee_upload_id: Mapped[str] = mapped_column(String(36), ForeignKey("uploads.id"), index=True)
    enrollment_upload_id: Mapped[str] = mapped_column(String(36), ForeignKey("uploads.id"), index=True)
    hei_name: Mapped[str] = mapped_column(String(255), index=True)
    academic_year: Mapped[str] = mapped_column(String(50), index=True)
    semester: Mapped[str] = mapped_column(String(50), index=True)
    scholarship: Mapped[str] = mapped_column(String(50), nullable=True)
    batch: Mapped[str] = mapped_column(String(50), nullable=True)
    threshold: Mapped[int] = mapped_column(Integer, default=88)
    created_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(50), default="draft")
