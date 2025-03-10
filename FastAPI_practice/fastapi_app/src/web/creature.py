from fastapi import APIRouter, HTTPException
from model.creature import Creature
from service import creature as service
from error import Duplicate, Missing

router = APIRouter(prefix="/creature")


@router.get("/", summary="Returns a list of all the creatures.", tags=["Creatures"])
@router.get("", summary="Returns a list of all the creatures.", tags=["Creatures"])
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{name}", summary="Returns a creature.", tags=["Creatures"])
def get_one(name) -> Creature | None:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


# all the remaining endpoints do nothing yet.
@router.post("", status_code=201, summary="Creatures a creature.", tags=["Creatures"])
@router.post("/", status_code=201, summary="Creatures a creature.", tags=["Creatures"])
def create(creature: Creature) -> Creature:
    try:
        return service.create(creature)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.patch("/", summary="Updates a creature.", tags=["Creatures"])
@router.patch("", summary="Updates a creature.", tags=["Creatures"])
def modify(name: str, creature: Creature) -> Creature | None:
    try:
        return service.modify(name, creature)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


# @router.put("/", summary="Returns a list of all the creatures.", tags=["Creatures"])
# def replace(creature: Creature) -> Creature:
#     return service.replace(creature)


@router.delete(
    "/{name}", status_code=204, summary="Deletes a creature.", tags=["Creatures"]
)
def delete(name: str):
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
