from fastapi import FastAPI
from app.routes import users,books
from app.logging import configure_logger

logger = configure_logger()

app = FastAPI(title="Book Tracker API")

app.include_router(users.router)
app.include_router(books.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Book Tracker API"}
