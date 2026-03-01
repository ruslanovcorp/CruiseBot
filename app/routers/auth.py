from fastapi import APIRouter

router = APIRouter(prefix="/auth")

@router.get("/test")
def test():
    return {"auth": "ok"}