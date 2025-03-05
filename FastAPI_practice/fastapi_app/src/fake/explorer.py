from model.explorer import Explorer

# fake data, replaced in chapter 10 by a real database and sql
_explorers = [
    Explorer(
        name="Claude Hande",
        country="FR",
        description="Scarce during full moons.",
    ),
    Explorer(
        name="Noah Weiser",
        country="DE",
        description="Myopic machete man",
    ),
]


def get_all() -> list[Explorer]:
    """Return all explorers."""
    print("get_all is being called.")
    return _explorers


def get_one(name: str) -> Explorer | None:
    """Return a specific explorer."""
    for _explorer in _explorers:
        if _explorer.name == name:
            return _explorer
    return None


# The following are nonfunctional for now,
# so they just act like they work, without modifying
# the actual fake_explorers list:


def create(explorer: Explorer) -> Explorer:
    """Add an explorer."""
    return explorer


def modify(explorer: Explorer) -> Explorer:
    """Partially modify an explorer."""
    return explorer


def replace(explorer: Explorer) -> Explorer:
    """Completely replace an explorer."""
    return explorer


def delete(name: str) -> bool | None:
    """Delete an explorer; return None if it existed"""
    return None
