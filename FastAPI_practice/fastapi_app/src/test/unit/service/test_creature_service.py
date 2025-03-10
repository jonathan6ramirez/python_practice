import pytest
from model.creature import Creature
from service import creature as code
from error import Missing

# page 119

sample = Creature(
    name="Yeti",
    aka="Abominable Snowman",
    country="CN",
    area="Himalayas",
    description="Hirsute Himalayan",
)


def test_create():
    resp = code.create(sample)
    assert resp == sample


def test_get_exists():
    resp = code.get_one("Yeti")
    assert resp == sample


def test_get_missing():
    with pytest.raises(Missing):
        _ = code.get_one("boxturle")
