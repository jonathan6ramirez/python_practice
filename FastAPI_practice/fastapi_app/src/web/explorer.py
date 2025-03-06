from fastapi import APIRouter
from model.explorer import Explorer
import service.explorer as service

router = APIRouter(prefix="/explorer")

print("the explorer file is being opened.")


@router.get("")
@router.get("/")
def get_all(name: str | None = None) -> list[Explorer]:
    print("/explorer/ route called")
    return service.get_all(name)


@router.get("/{name}")
def get_one(name) -> Explorer | None:
    return service.get_one(name)


# all the remaining endpoints do nothing yet.
@router.post("")
@router.post("/")
def create(explorer: Explorer) -> Explorer:
    return service.create(explorer)


@router.patch("")
@router.patch("/")
def modify(name: str, explorer: Explorer) -> Explorer:
    return service.modify(name, explorer)


@router.put("")
@router.put("/")
def replace(name: str, explorer: Explorer) -> Explorer:
    print("the put endpoint is getting called")
    return service.replace(name, explorer)


@router.delete("/{name}")
def delete(explorer: Explorer) -> bool:
    return service.delete(explorer)
