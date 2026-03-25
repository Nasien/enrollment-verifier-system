from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.upload import Upload
from app.models.grantee import Grantee
from app.models.enrollment import EnrollmentRecord
from app.models.user import User
from app.services.audit_service import log_action
from app.services.excel_parser import parse_excel
from app.utils.security import get_current_user

router = APIRouter(prefix="/uploads", tags=["uploads"])


def _check_duplicate_upload(db: Session, upload_type: str, hei_name: str, academic_year: str, semester: str, scholarship: str | None, batch: str | None):
    return db.query(Upload).filter(
        Upload.upload_type == upload_type,
        Upload.hei_name == hei_name,
        Upload.academic_year == academic_year,
        Upload.semester == semester,
        Upload.scholarship == scholarship,
        Upload.batch == batch,
    ).first()


@router.post("/grantee")
async def upload_grantee(
    file: UploadFile = File(...),
    hei_name: str = Form(...),
    academic_year: str = Form(...),
    semester: str = Form(...),
    scholarship: str = Form(...),
    batch: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = _check_duplicate_upload(db, "grantee", hei_name, academic_year, semester, scholarship, batch)
    if existing:
        raise HTTPException(status_code=409, detail="A grantee upload with the same HEI, AY, semester, scholarship, and batch already exists.")

    contents = await file.read()
    parsed_rows, _ = parse_excel(contents)
    upload = Upload(
        file_name=file.filename,
        upload_type="grantee",
        hei_name=hei_name,
        academic_year=academic_year,
        semester=semester,
        scholarship=scholarship,
        batch=batch,
        uploaded_by=current_user.id,
        row_count=len(parsed_rows),
        status="processed",
    )
    db.add(upload)
    db.commit()
    db.refresh(upload)

    db.bulk_save_objects([
        Grantee(
            upload_id=upload.id,
            full_name=row["full_name"],
            normalized_name=row["normalized_name"],
            hei_name=hei_name,
            academic_year=academic_year,
            semester=semester,
            scholarship=scholarship,
            batch=batch,
            source_row=row["source_row"],
        )
        for row in parsed_rows
    ])
    db.commit()
    log_action(db, current_user.id, "upload_grantee", "upload", upload.id, {"row_count": len(parsed_rows)})
    return {"message": "Grantee file uploaded successfully", "upload_id": upload.id, "row_count": len(parsed_rows)}


@router.post("/enrollment")
async def upload_enrollment(
    file: UploadFile = File(...),
    hei_name: str = Form(...),
    academic_year: str = Form(...),
    semester: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = _check_duplicate_upload(db, "enrollment", hei_name, academic_year, semester, None, None)
    if existing:
        raise HTTPException(status_code=409, detail="An enrollment upload with the same HEI, AY, and semester already exists.")

    contents = await file.read()
    parsed_rows, _ = parse_excel(contents)
    upload = Upload(
        file_name=file.filename,
        upload_type="enrollment",
        hei_name=hei_name,
        academic_year=academic_year,
        semester=semester,
        scholarship=None,
        batch=None,
        uploaded_by=current_user.id,
        row_count=len(parsed_rows),
        status="processed",
    )
    db.add(upload)
    db.commit()
    db.refresh(upload)

    db.bulk_save_objects([
        EnrollmentRecord(
            upload_id=upload.id,
            full_name=row["full_name"],
            normalized_name=row["normalized_name"],
            hei_name=hei_name,
            academic_year=academic_year,
            semester=semester,
            source_row=row["source_row"],
        )
        for row in parsed_rows
    ])
    db.commit()
    log_action(db, current_user.id, "upload_enrollment", "upload", upload.id, {"row_count": len(parsed_rows)})
    return {"message": "Enrollment file uploaded successfully", "upload_id": upload.id, "row_count": len(parsed_rows)}


@router.get("/history")
def get_upload_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    uploads = db.query(Upload).order_by(Upload.uploaded_at.desc()).all()
    return uploads
