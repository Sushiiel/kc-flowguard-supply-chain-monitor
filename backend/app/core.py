from fastapi import APIRouter
from .engine import engine

router = APIRouter()

@router.post("/inject")
def inject_event(data: dict):
    processed = engine.process(data)
    return processed

@router.get("/kpis")
def get_kpis():
    return engine.kpis()

@router.get("/snapshot")
def get_snapshot():
    return engine.snapshot()