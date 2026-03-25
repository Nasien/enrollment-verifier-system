import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.database import Base, engine
from app.models import *  # noqa
from app.routes import auth, uploads, verification, reports, dashboard

load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Enrollment Verifier API")

origins = [item.strip() for item in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(uploads.router)
app.include_router(verification.router)
app.include_router(reports.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {"message": "Enrollment Verifier API is running"}
