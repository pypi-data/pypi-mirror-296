from typing import Any

import pytest

from openfigi_client import MappingJob, OpenFigi, Query
from openfigi_client.exceptions import HTTPError, TooManyMappingJobsError
from openfigi_client.models import (
    FigiResult,
    MappingJobResult,
    MappingJobResultFigiList,
    MappingJobResultFigiNotFound,
)


@pytest.fixture(scope="module")
def vcr_config(record_mode: str) -> dict[str, Any]:
    """Return VCR configuration."""
    return {"filter_headers": ["authorization"], "record_mode": record_mode or "none"}


def test_headers() -> None:
    """Test that the HTTP headers include the API key when the latter is provided."""
    api_key = "XXXXXXXXXX"
    headers_without_key = {"Content-Type": "application/json"}
    headers_with_key = headers_without_key | {"X-OPENFIGI-APIKEY": api_key}

    assert OpenFigi().headers == headers_without_key
    assert OpenFigi(api_key=api_key).headers == headers_with_key


@pytest.mark.vcr()
def test_map_one_job() -> None:
    """Test a mapping request for an existing ticker (e.g. IBM US)."""
    mapping_job = MappingJob(id_type="TICKER", id_value="IBM", exch_code="US")
    mapping_jobs = [mapping_job]
    results = OpenFigi().map(mapping_jobs)

    assert results
    assert all(isinstance(x, MappingJobResultFigiList) for x in results)


@pytest.mark.vcr()
def test_map_two_jobs() -> None:
    """Test a mapping request for two existing tickers (e.g. IBM US and XRX US)."""
    mapping_job_ibm = MappingJob(id_type="TICKER", id_value="IBM", exch_code="US")
    mapping_job_xerox = MappingJob(id_type="TICKER", id_value="XRX", exch_code="US")
    mapping_jobs = [mapping_job_ibm, mapping_job_xerox]
    results = OpenFigi().map(mapping_jobs)

    assert results
    assert all(isinstance(x, MappingJobResultFigiList) for x in results)


@pytest.mark.vcr()
def test_map_two_jobs_one_of_which_is_in_error() -> None:
    """Test a mapping request for two tickers, one of them being unknown."""
    mapping_job_ibm = MappingJob(id_type="TICKER", id_value="IBM", exch_code="US")
    mapping_job_error = MappingJob(
        id_type="TICKER",
        id_value="UNKNOWN_TICKER",
        exch_code="US",
    )
    mapping_jobs = [mapping_job_ibm, mapping_job_error]
    results = OpenFigi().map(mapping_jobs)

    assert results
    assert all(isinstance(x, MappingJobResult) for x in results)
    assert isinstance(results[0], MappingJobResultFigiList)
    assert isinstance(results[1], MappingJobResultFigiNotFound)


def test_map_too_many_jobs_in_one_request() -> None:
    """Test that an exception is raised if too many MappingJob are provided in one request."""
    mapping_jobs = [
        MappingJob(id_type="TICKER", id_value="IBM", exch_code="US"),
    ] * 11

    with pytest.raises(TooManyMappingJobsError):
        _ = OpenFigi().map(mapping_jobs)


@pytest.mark.vcr()
def test_too_many_mapping_requests() -> None:
    """Test that an exception is raised if too many MappingJob requests are sent."""
    mapping_jobs = [MappingJob(id_type="TICKER", id_value="IBM", exch_code="US")]

    with pytest.raises(HTTPError):  # noqa: PT012
        for _i in range(50):
            _ = OpenFigi().map(mapping_jobs)


@pytest.mark.vcr()
def test_filter_single_api_call() -> None:
    """Test a search request for a little known security (i.e. only requires one remote call)."""
    query = Query(query="SJIM")
    results = OpenFigi().filter(query)

    assert results
    assert all(isinstance(x, FigiResult) for x in results)


@pytest.mark.vcr()
def test_filter_instrument_not_found() -> None:
    """Test that a search for something that does not exist returns an empty list."""
    query = Query(query="UNKNOWN_TICKER")
    results = OpenFigi().filter(query)

    assert isinstance(results, list)
    assert len(results) == 0


@pytest.mark.slow()
@pytest.mark.vcr()
def test_filter_multi_api_call() -> None:
    """
    Test that a search for a query with over 100 results (and therefore necessiting several calls
    taking into acccount the rate limitations) works fine.

    Careful: this test can take up to 20min to run if the query returns the maximum of 15,000 results
    and no API key was provided.
    """
    query = Query(query="CTA")
    results = OpenFigi().filter(query)

    assert results
    assert all(isinstance(x, FigiResult) for x in results)


@pytest.mark.vcr()
def test_get_total_number_of_matches() -> None:
    """Test that the total number of matches for a given query is returned."""
    # Test for a query that has matches
    query = Query(query="IBM")
    matches = OpenFigi().get_total_number_of_matches(query)

    assert isinstance(matches, int)

    # Test for a query that has no matches
    query = Query(query="UNKNOWN_TICKER")
    matches = OpenFigi().get_total_number_of_matches(query)

    assert matches == 0


@pytest.mark.vcr()
def test_get_id_types() -> None:
    """Test that the list of available ID types is returned."""
    id_types = OpenFigi().get_id_types()

    assert isinstance(id_types, list)
    assert all(isinstance(x, str) for x in id_types)
    assert "TICKER" in id_types


@pytest.mark.vcr()
def test_get_exch_codes() -> None:
    """Test that the list of available exchange codes is returned."""
    exch_codes = OpenFigi().get_exch_codes()

    assert isinstance(exch_codes, list)
    assert all(isinstance(x, str) for x in exch_codes)
    assert "US" in exch_codes


@pytest.mark.vcr()
def test_get_mic_codes() -> None:
    """Test that the list of available MIC codes is returned."""
    mic_codes = OpenFigi().get_mic_codes()

    assert isinstance(mic_codes, list)
    assert all(isinstance(x, str) for x in mic_codes)
    assert "BATS" in mic_codes


@pytest.mark.vcr()
def test_get_currencies() -> None:
    """Test that the list of available currencies is returned."""
    currencies = OpenFigi().get_currencies()

    assert isinstance(currencies, list)
    assert all(isinstance(x, str) for x in currencies)
    assert "USD" in currencies


@pytest.mark.vcr()
def test_get_market_security_descriptions() -> None:
    """Test that the list of available market security descriptions is returned."""
    market_security_descriptions = OpenFigi().get_market_sec_des()

    assert isinstance(market_security_descriptions, list)
    assert all(isinstance(x, str) for x in market_security_descriptions)
    assert "Equity" in market_security_descriptions


@pytest.mark.vcr()
def test_get_security_types() -> None:
    """Test that the list of available security types is returned."""
    security_types = OpenFigi().get_security_types()

    assert isinstance(security_types, list)
    assert all(isinstance(x, str) for x in security_types)
    assert "Equity Index" in security_types


@pytest.mark.vcr()
def test_get_security_types_2() -> None:
    """Test that the list of available security types 2 is returned."""
    security_types_2 = OpenFigi().get_security_types_2()

    assert isinstance(security_types_2, list)
    assert all(isinstance(x, str) for x in security_types_2)
    assert "Common Stock" in security_types_2


@pytest.mark.vcr()
def test_get_state_codes() -> None:
    """Test that the list of available state codes is returned."""
    state_codes = OpenFigi().get_state_codes()

    assert isinstance(state_codes, list)
    assert all(isinstance(x, str) for x in state_codes)
    assert "AB" in state_codes
