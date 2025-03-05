from model.creature import Creature

# fake data, replaced in chapter 10 by a real database and sql
_creatures = [
    Creature(
        name="Yeti",
        aka="Abominable Snowman",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
    ),
    Creature(
        name="Bigfoot",
        aka="Yeti's Cousin Eddie",
        country="US",
        area="*",
        description="Sasquatch",
    ),
]


def get_all() -> list[Creature]:
    """Return all creatures."""
    return _creatures


def get_one(name: str) -> Creature | None:
    """Return a specific creature."""
    for _creature in _creatures:
        if _creature.name == name:
            return _creature
    return None


# The following are nonfunctional for now,
# so they just act like they work, without modifying
# the actual fake_creatures list:


def create(creature: Creature) -> Creature:
    """Add an creature."""
    return creature


def modify(creature: Creature) -> Creature:
    """Partially modify an creature."""
    return creature


def replace(creature: Creature) -> Creature:
    """Completely replace a creature."""
    return creature


def delete(name: str) -> bool | None:
    """Delete an creature; return None if it existed"""
    return None
