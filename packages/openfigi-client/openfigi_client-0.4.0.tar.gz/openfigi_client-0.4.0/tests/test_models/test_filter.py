import msgspec
import pytest

from openfigi_client._models import Filter


def test_min_one_field() -> None:
    """Test that at least one field is required."""
    with pytest.raises(ValueError):  # noqa: PT011
        _ = Filter()


def test_query_is_optional() -> None:
    """Verify that the query field is optional."""
    filter_ = Filter(mic_code="BATS")
    assert isinstance(filter_, Filter)


def test_query_min_length() -> None:
    """Verify that the query field has a minimum length."""
    with pytest.raises(msgspec.ValidationError):
        _ = Filter(query="")
