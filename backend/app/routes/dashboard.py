from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.upload import Upload
from app.models.verification_session import VerificationSession
from app.models.verification_result import VerificationResult
from app.models.user import User
from app.utils.security import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/metrics")
def metrics(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total_uploads = db.query(Upload).count()
    total_sessions = db.query(VerificationSession).count()
    total_results = db.query(VerificationResult).count()
    exact = db.query(VerificationResult).filter(VerificationResult.match_status == "exact_match").count()
    possible = db.query(VerificationResult).filter(VerificationResult.match_status == "possible_match").count()
    not_found = db.query(VerificationResult).filter(VerificationResult.match_status == "not_found").count()
    return {
        "total_uploads": total_uploads,
        "total_sessions": total_sessions,
        "total_results": total_results,
        "exact_matches": exact,
        "possible_matches": possible,
        "not_found": not_found,
    }
