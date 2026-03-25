from sqlalchemy.orm import Session
from app.models.grantee import Grantee
from app.models.enrollment import EnrollmentRecord
from app.models.verification_result import VerificationResult
from app.models.verification_session import VerificationSession
from app.services.name_matcher import score_name


def run_verification(db: Session, session: VerificationSession, threshold: int = 88):
    grantees = db.query(Grantee).filter(Grantee.upload_id == session.grantee_upload_id).all()
    enrollments = db.query(EnrollmentRecord).filter(EnrollmentRecord.upload_id == session.enrollment_upload_id).all()

    enrollment_map = {}
    for record in enrollments:
        enrollment_map.setdefault(record.normalized_name, []).append(record)

    results = []
    for grantee in grantees:
        exact_candidates = enrollment_map.get(grantee.normalized_name, [])
        if exact_candidates:
            result = VerificationResult(
                session_id=session.id,
                grantee_id=grantee.id,
                matched_enrollment_id=exact_candidates[0].id,
                match_status="exact_match",
                match_score=100,
            )
            db.add(result)
            results.append(result)
            continue

        best_match = None
        best_score = 0
        for enrolled in enrollments:
            score = score_name(grantee.normalized_name, enrolled.normalized_name)
            if score > best_score:
                best_score = score
                best_match = enrolled

        if best_match and best_score >= threshold:
            result = VerificationResult(
                session_id=session.id,
                grantee_id=grantee.id,
                matched_enrollment_id=best_match.id,
                match_status="possible_match",
                match_score=best_score,
            )
        else:
            result = VerificationResult(
                session_id=session.id,
                grantee_id=grantee.id,
                matched_enrollment_id=None,
                match_status="not_found",
                match_score=best_score,
            )
        db.add(result)
        results.append(result)

    session.status = "completed"
    db.commit()
    return results
