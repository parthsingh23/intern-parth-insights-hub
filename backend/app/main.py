from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .repositories.sales_repository import SalesRepository
from .routers.health import router as health_router
from .routers.sales import router as sales_router
from .services.sales_service import SalesService


@asynccontextmanager
async def lifespan(app: FastAPI):
    repository = SalesRepository()
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
