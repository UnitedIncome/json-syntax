import pytest

from json_syntax.examples import loose_dates as exam
from json_syntax.helpers import J2P, P2J, IP, IJ, python_minor

from datetime import date, datetime
from unittest.mock import Mock


def Fail():
    return Mock(lookup=Mock(side_effect=RuntimeError))


@pytest.mark.skipif(
    python_minor < (3, 7), reason="datetime.isoformat not supported before python 3.7"
)
def test_iso_dates_loose():
    "Test the iso_dates_loose rule will generate encoders and decoders for dates using ISO8601, accepting datetimes as input to dates."

    decoder = exam.iso_dates_loose(verb=J2P, typ=date, ctx=Fail())
    assert decoder("1776-07-04") == date(1776, 7, 4)
    assert decoder("6543-02-01T09:09:09") == date(6543, 2, 1)

    encoder = exam.iso_dates_loose(verb=P2J, typ=date, ctx=Fail())
    assert encoder(date(1776, 7, 4)) == "1776-07-04"

    inspect = exam.iso_dates_loose(verb=IP, typ=date, ctx=Fail())
    assert inspect(date(1776, 7, 4))
    assert not inspect(datetime(1776, 7, 4, 3, 3))
    assert not inspect("2000-01-01")
    assert not inspect("2000-01-01T03:03:03")
    assert not inspect("string")

    inspect = exam.iso_dates_loose(verb=IJ, typ=date, ctx=Fail())
    assert not inspect(date(1776, 7, 4))
    assert not inspect(datetime(1776, 7, 4, 3, 3))
    assert inspect("2000-01-01")
    assert inspect("2000-01-01T03:03:03")
    assert not inspect("string")
