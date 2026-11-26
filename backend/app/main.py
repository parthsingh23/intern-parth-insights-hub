import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .repositories.postgres_sales_repository import PostgresSalesRepository
from .repositories.sales_repository import SalesRepository
from .routers.health import router as health_router
from .routers.sales import router as sales_router
from .services.sales_service import SalesService

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


@asynccontextmanager
async def lifespan(app: FastAPI):
    repository_type = os.getenv("REPOSITORY", "file").strip().lower()

    if repository_type == "file":
        repository = SalesRepository()
    elif repository_type == "postgres":
        repository = PostgresSalesRepository()
    else:
        raise ValueError(f"Unsupported REPOSITORY value: {repository_type}")

    app.state.sales_service = SalesService(repository)
    yield


app = FastAPI(
    title="Emami Sales Analytics API",
    description="API for querying and analysing secondary sales data.",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Backend for the insights hub"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "; ".join(error["msg"] for error in exc.errors()),
            }
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        headers=exc.headers,
        content={
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": str(exc.detail),
            }
        },
    )


app.include_router(health_router)
app.include_router(sales_router)
