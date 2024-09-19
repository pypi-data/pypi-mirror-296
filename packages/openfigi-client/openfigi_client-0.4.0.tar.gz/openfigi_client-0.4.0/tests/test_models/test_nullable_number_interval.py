import pytest

from openfigi_client._models import validate_nullable_number_interval


@pytest.mark.parametrize("strike", [[0], [0, 1, 2], [None, None], [1, 0]])
def test_invalid_inputs_should_raise_exception(strike: list[int | None]) -> None:
    """Test that an invalid combination of inputs raises a ValidationError exception."""
    with pytest.raises(TypeError):
        validate_nullable_number_interval(strike)


@pytest.mark.parametrize("strike", [[0, 1], [None, 1], [0, None]])
def test_valid_inputs_should_instantiate(strike: list[int | None]) -> None:
    """Test that a valid combination of inputs instantiates the list."""
    assert validate_nullable_number_interval(strike) is None
