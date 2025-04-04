from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def greet():
    return "Welcome to Delta Finances"
