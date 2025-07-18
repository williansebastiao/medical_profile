from fastapi import APIRouter

from . import health, patient

router = APIRouter()

router.include_router(health.router)
router.include_router(patient.router)
