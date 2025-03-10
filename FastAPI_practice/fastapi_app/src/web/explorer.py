from fastapi import APIRouter, HTTPException
from model.explorer import Explorer
from service import explorer as service
from error import Duplicate, Missing

router = APIRouter(prefix="/explorer")


@router.get("", summary="Returns a list of all the explorers.", tags=["Explorers"])
@router.get("/", summary="Returns a list of all the explorers.", tags=["Explorers"])
def get_all() -> list[Explorer]:
    return service.get_all()


@router.get("/{name}", summary="Returns an explorer.", tags=["Explorers"])
def get_one(name: str) -> Explorer | None:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("", status_code=201, summary="Creates an explorer.", tags=["Explorers"])
@router.post("/", status_code=201, summary="Creates an explorer.", tags=["Explorers"])
def create(explorer: Explorer) -> Explorer:
    try:
        return service.create(explorer)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.patch("", summary="Udates an explorer.", tags=["Explorers"])
@router.patch("/", summary="Udates an explorer.", tags=["Explorers"])
def modify(name: str, explorer: Explorer) -> Explorer | None:
    try:
        return service.modify(name, explorer)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


# INFO: Is this enpoint even being used????
# @router.put("")
# @router.put("/")
# def replace(name: str, explorer: Explorer) -> Explorer:
#     print("the put endpoint is getting called")
#     return service.replace(name, explorer)


@router.delete(
    "/{name}", status_code=204, summary="Deletes an explorer.", tags=["Explorers"]
)
def delete(name: str):
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
