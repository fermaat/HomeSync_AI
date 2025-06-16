from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cfg import settings
from src.api.routes import router
from src.database.connection import create_db_and_tables

app = FastAPI(title="HomeSync AI Backend")


# Config CORS
origins = [
    # TODO: export ports to settings
    "http://localhost:19006",  # Expo Go Port
    "http://localhost:8081",  # Metro Bundler Port
    f"exp://{settings.local_ip}:8081",  # Expo Go local network URL
    f"http://{settings.local_ip}:8000",  #
    # TODO: add React Native app URL when deploying to production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    print("Creating database tables if they don't exist...")
    create_db_and_tables()
    print("Database tables check complete.")


app.include_router(router, prefix="/api/v1")
