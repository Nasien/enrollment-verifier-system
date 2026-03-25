from pydantic import BaseModel


class UploadResponse(BaseModel):
    id: str
    file_name: str
    upload_type: str
    hei_name: str
    academic_year: str
    semester: str
    scholarship: str | None = None
    batch: str | None = None
    row_count: int
    status: str
