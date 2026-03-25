import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class VerificationResult(Base):
    __tablename__ = "verification_results"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("verification_sessions.id"), index=True)
    grantee_id: Mapped[str] = mapped_column(String(36), ForeignKey("grantees.id"), index=True)
    matched_enrollment_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("enrollment_records.id"), nullable=True)
    match_status: Mapped[str] = mapped_column(String(50), index=True)
    match_score: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    review_status: Mapped[str] = mapped_column(String(50), default="pending", index=True)
    review_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewed_by: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
