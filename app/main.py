from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .versions.v0 import v0_main

app = FastAPI(
    title="PROVEDGE Simulation Platform API",
    description="Backend service for PROVEDGE Simulation Platform API written in Python, using FastAPI.",
    version="0.0.1"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    v0_main.router,
    prefix="/api/v0",
    #responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {
        "status": "SUCCESS",
        "message": "Welcome, It's PROVEDGE Simulation Platform API.",
        "quote": {
            "quote": "If I had asked people what they wanted, they would have said faster horses.",
            "owner": "Henry Ford"
        } 
    }