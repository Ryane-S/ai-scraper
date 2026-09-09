from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
def health():
    """Récupère le statut de l'application."""
    return {"message": "OK !"}