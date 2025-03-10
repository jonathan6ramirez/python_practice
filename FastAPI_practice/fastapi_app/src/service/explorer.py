from model.explorer import Explorer
import data.explorer as data


def get_all() -> list[Explorer]:
    return data.get_all()


def get_one(name: str) -> Explorer | None:
    return data.get_one(name)


def create(explorer: Explorer) -> Explorer:
    return data.create(explorer)


def replace(name: str, explorer: Explorer) -> Explorer:
    return data.replace(name, explorer)


# NOTE: Should the name string be the one to be passed to the name_orig parameter since that
# is what is being read to select the row and update it with the body parameters
def modify(name: str, explorer: Explorer) -> Explorer | None:
    return data.modify(name, explorer)


def delete(name: str):
    return data.delete(name)
