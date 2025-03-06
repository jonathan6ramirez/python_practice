from model.explorer import Explorer
import data.explorer as data


def get_all(name: str | None) -> list[Explorer]:
    return data.get_all(name)


def get_one(name: str) -> Explorer | None:
    return data.get_one(name)


def create(explorer: Explorer) -> Explorer:
    return data.create(explorer)


def replace(name: str, explorer: Explorer) -> Explorer:
    return data.replace(name, explorer)


def modify(name: str, explorer: Explorer) -> Explorer:
    return data.modify(id, explorer)


def delete(explorer: Explorer) -> bool:
    return data.delete(explorer)
