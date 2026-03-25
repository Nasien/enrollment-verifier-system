from io import BytesIO
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.verification_result import VerificationResult
from app.models.grantee import Grantee
from app.models.enrollment import EnrollmentRecord
from app.models.user import User
from app.utils.security import get_current_user

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/session/{session_id}/export")
def export_session(session_id: str, status: str | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(VerificationResult).filter(VerificationResult.session_id == session_id)
    if status:
        query = query.filter(VerificationResult.match_status == status)
    items = query.all()
    if not items:
        raise HTTPException(status_code=404, detail="No results found")

    rows = []
    for item in items:
        grantee = db.query(Grantee).filter(Grantee.id == item.grantee_id).first()
        enrollment = db.query(EnrollmentRecord).filter(EnrollmentRecord.id == item.matched_enrollment_id).first() if item.matched_enrollment_id else None
        rows.append({
            "Grantee Name": grantee.full_name if grantee else "",
            "Matched Enrollment Name": enrollment.full_name if enrollment else "",
            "Match Status": item.match_status,
            "Match Score": float(item.match_score),
            "Review Status": item.review_status,
            "Review Notes": item.review_notes or "",
        })

    df = pd.DataFrame(rows)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Verification Results")
    output.seek(0)
    filename = f"verification_{session_id}.xlsx"
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
