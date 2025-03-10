import pytest
from model.explorer import Explorer
from service import explorer as code
from error import Missing

# page 119

sample = Explorer(
    name="Jonathan Ramirez",
    country="US",
    description="Online Services Developer / Enterprise Systems Support Analyst",
)


def test_create():
    resp = code.create(sample)
    assert resp == sample


def test_get_exists():
    resp = code.get_one("Jonathan Ramirez")
    assert resp == sample


def test_get_missing():
    with pytest.raises(Missing):
        _ = code.get_one("boxturle")
