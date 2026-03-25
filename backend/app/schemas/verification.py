from pydantic import BaseModel


class RunVerificationRequest(BaseModel):
    grantee_upload_id: str
    enrollment_upload_id: str
    threshold: int = 88


class ReviewResultRequest(BaseModel):
    review_status: str
    review_notes: str | None = None
    matched_enrollment_id: str | None = None
