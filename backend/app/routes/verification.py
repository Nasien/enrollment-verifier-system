from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.upload import Upload
from app.models.user import User
from app.models.verification_session import VerificationSession
from app.models.verification_result import VerificationResult
from app.models.grantee import Grantee
from app.models.enrollment import EnrollmentRecord
from app.schemas.verification import RunVerificationRequest, ReviewResultRequest
from app.services.audit_service import log_action
from app.services.verification_service import run_verification
from app.utils.security import get_current_user

router = APIRouter(prefix="/verification", tags=["verification"])


@router.post("/run")
def run(payload: RunVerificationRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    grantee_upload = db.query(Upload).filter(Upload.id == payload.grantee_upload_id, Upload.upload_type == "grantee").first()
    enrollment_upload = db.query(Upload).filter(Upload.id == payload.enrollment_upload_id, Upload.upload_type == "enrollment").first()
    if not grantee_upload or not enrollment_upload:
        raise HTTPException(status_code=404, detail="Upload record not found")

    session = VerificationSession(
        grantee_upload_id=grantee_upload.id,
        enrollment_upload_id=enrollment_upload.id,
        hei_name=grantee_upload.hei_name,
        academic_year=grantee_upload.academic_year,
        semester=grantee_upload.semester,
        scholarship=grantee_upload.scholarship,
        batch=grantee_upload.batch,
        threshold=payload.threshold,
        created_by=current_user.id,
        status="running",
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    run_verification(db, session, payload.threshold)
    log_action(db, current_user.id, "run_verification", "verification_session", session.id, {"threshold": payload.threshold})
    return {"message": "Verification completed", "session_id": session.id}


@router.get("/sessions")
def list_sessions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sessions = db.query(VerificationSession).order_by(VerificationSession.created_at.desc()).all()
    return sessions


@router.get("/sessions/{session_id}")
def session_detail(session_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = db.query(VerificationSession).filter(VerificationSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    results = db.query(VerificationResult).filter(VerificationResult.session_id == session_id).all()

    formatted = []
    for item in results:
        grantee = db.query(Grantee).filter(Grantee.id == item.grantee_id).first()
        enrollment = db.query(EnrollmentRecord).filter(EnrollmentRecord.id == item.matched_enrollment_id).first() if item.matched_enrollment_id else None
        formatted.append({
            "id": item.id,
            "grantee_id": item.grantee_id,
            "grantee_name": grantee.full_name if grantee else None,
            "matched_enrollment_id": item.matched_enrollment_id,
            "matched_name": enrollment.full_name if enrollment else None,
            "match_status": item.match_status,
            "match_score": float(item.match_score),
            "review_status": item.review_status,
            "review_notes": item.review_notes,
        })

    summary = {
        "total": len(formatted),
        "exact_match": len([x for x in formatted if x["match_status"] == "exact_match"]),
        "possible_match": len([x for x in formatted if x["match_status"] == "possible_match"]),
        "not_found": len([x for x in formatted if x["match_status"] == "not_found"]),
    }
    return {"session": session, "summary": summary, "results": formatted}


@router.patch("/results/{result_id}/review")
def review_result(result_id: str, payload: ReviewResultRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = db.query(VerificationResult).filter(VerificationResult.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    result.review_status = payload.review_status
    result.review_notes = payload.review_notes
    if payload.matched_enrollment_id:
        result.matched_enrollment_id = payload.matched_enrollment_id
    result.reviewed_by = current_user.id
    result.reviewed_at = datetime.utcnow()
    db.commit()
    log_action(db, current_user.id, "review_result", "verification_result", result.id, {"review_status": payload.review_status})
    return {"message": "Review updated successfully"}
