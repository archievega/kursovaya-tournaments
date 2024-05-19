from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from src.tournament.routers import router as tournament_router
from src.auth.routers import router as auth_router


app = FastAPI(
    title="GlukoSports",
    routes=[
        Mount(
            "/static",
            app=StaticFiles(directory="static"),
            name="static",
        ),
    ],
)


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


main_router = APIRouter()

main_router.include_router(auth_router)
main_router.include_router(tournament_router)

app.include_router(main_router)
