import datetime as dt

import msgspec
import pytest

from openfigi_client._models import (
    NullableDateInterval,
    validate_nullable_date_interval,
)


class DummyModel(msgspec.Struct):
    """A model for testing."""

    expiration: NullableDateInterval


@pytest.mark.parametrize(
    "expiration",
    [
        [dt.date(2023, 1, 1)],
        [dt.date(2023, 1, 1), dt.date(2023, 1, 2), dt.date(2023, 1, 3)],
        [None, None],
        [dt.date(2020, 1, 1), dt.date(2023, 1, 1)],
    ],
)
def test_invalid_inputs_should_raise_exception(
    expiration: list[dt.date | None],
) -> None:
    """Test that an invalid combination of inputs raises a ValidationError exception."""
    with pytest.raises(TypeError):
        validate_nullable_date_interval(expiration)


@pytest.mark.parametrize(
    "expiration",
    [
        [dt.date(2023, 1, 1), dt.date(2023, 12, 31)],
        [None, dt.date(2023, 12, 31)],
        [dt.date(2023, 1, 1), None],
    ],
)
def test_valid_inputs_should_instantiate(expiration: list[dt.date | None]) -> None:
    """Test that a valid combination of inputs instantiates the list."""
    assert validate_nullable_date_interval(expiration) is None


@pytest.mark.parametrize(
    ("expiration", "result"),
    [
        (
            [dt.date(2023, 1, 1), dt.date(2023, 12, 31)],
            '{"expiration":["2023-01-01","2023-12-31"]}',
        ),
        ([None, dt.date(2023, 12, 31)], '{"expiration":[null,"2023-12-31"]}'),
        ([dt.date(2023, 1, 1), None], '{"expiration":["2023-01-01",null]}'),
    ],
)
def test_dates_should_be_correctly_serialized(
    expiration: list[dt.date | None],
    result: str,
) -> None:
    """Test that the NullableDateInterval objects are correctly serialized into YYYY-MM-DD format."""
    test_json = msgspec.json.encode(DummyModel(expiration=expiration)).decode()

    assert test_json == result
