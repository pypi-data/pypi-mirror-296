import asyncio
from collections.abc import Callable
from typing import Any

import pytest

from openfigi_client import (
    FigiResult,
    MappingJob,
    MappingJobResult,
    MappingJobResultFigiList,
    MappingJobResultFigiNotFound,
    OpenFigiAsync,
    OpenFigiSync,
    Query,
)
from openfigi_client.exceptions import HTTPError, TooManyMappingJobsError

ClientType = OpenFigiSync | OpenFigiAsync


@pytest.fixture(scope="module")
def vcr_config(record_mode: str) -> dict[str, Any]:
    """Return VCR configuration."""
    return {"filter_headers": ["authorization"], "record_mode": record_mode or "none"}


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """Return the anyio backend."""
    return "asyncio"


@pytest.fixture(params=[OpenFigiSync, OpenFigiAsync])
def client(request: pytest.FixtureRequest) -> ClientType:
    """Return a client instance."""
    return request.param()


async def run_sync_or_async(func: Callable, *args: object, **kwargs: object) -> Any:
    """Function to run sync and async client."""
    if asyncio.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    return func(*args, **kwargs)


@pytest.mark.anyio
async def test_headers(client: ClientType) -> None:
    """Test that the HTTP headers include the API key when the latter is provided."""
    api_key = "XXXXXXXXXX"
    headers_without_key = {"Content-Type": "application/json"}
    headers_with_key = headers_without_key | {"X-OPENFIGI-APIKEY": api_key}

    assert client.headers == headers_without_key
    assert client.__class__(api_key=api_key).headers == headers_with_key


@pytest.mark.anyio
@pytest.mark.vcr
async def test_map_one_job(client: ClientType) -> None:
    """Test a mapping request for an existing ticker (e.g. IBM US)."""
    mapping_job = MappingJob(id_type="TICKER", id_value="IBM", exch_code="US")
    mapping_jobs = [mapping_job]
    results = await run_sync_or_async(client.map, mapping_jobs)

    assert results
    assert all(isinstance(x, MappingJobResultFigiList) for x in results)


@pytest.mark.anyio
@pytest.mark.vcr
async def test_map_two_jobs(client: ClientType) -> None:
    """Test a mapping request for two existing tickers (e.g. IBM US and XRX US)."""
    mapping_job_ibm = MappingJob(id_type="TICKER", id_value="IBM", exch_code="US")
    mapping_job_xerox = MappingJob(id_type="TICKER", id_value="XRX", exch_code="US")
    mapping_jobs = [mapping_job_ibm, mapping_job_xerox]
    results = await run_sync_or_async(client.map, mapping_jobs)

    assert results
    assert all(isinstance(x, MappingJobResultFigiList) for x in results)


@pytest.mark.anyio
@pytest.mark.vcr
async def test_map_two_jobs_one_of_which_is_in_error(client: ClientType) -> None:
    """Test a mapping request for two tickers, one of them being unknown."""
    mapping_job_ibm = MappingJob(id_type="TICKER", id_value="IBM", exch_code="US")
    mapping_job_error = MappingJob(
        id_type="TICKER",
        id_value="UNKNOWN_TICKER",
        exch_code="US",
    )
    mapping_jobs = [mapping_job_ibm, mapping_job_error]
    results = await run_sync_or_async(client.map, mapping_jobs)

    assert results
    assert all(isinstance(x, MappingJobResult) for x in results)
    assert isinstance(results[0], MappingJobResultFigiList)
    assert isinstance(results[1], MappingJobResultFigiNotFound)


@pytest.mark.anyio
async def test_map_too_many_jobs_in_one_request(client: ClientType) -> None:
    """Test that an exception is raised if too many MappingJob are provided in one request."""
    mapping_jobs = [
        MappingJob(id_type="TICKER", id_value="IBM", exch_code="US"),
    ] * 11

    with pytest.raises(TooManyMappingJobsError):
        await run_sync_or_async(client.map, mapping_jobs)


@pytest.mark.anyio
@pytest.mark.vcr
async def test_too_many_mapping_requests(client: ClientType) -> None:
    """Test that an exception is raised if too many MappingJob requests are sent."""
    mapping_jobs = [MappingJob(id_type="TICKER", id_value="IBM", exch_code="US")]

    with pytest.raises(HTTPError):  # noqa: PT012
        for _i in range(50):
            await run_sync_or_async(client.map, mapping_jobs)


@pytest.mark.anyio
@pytest.mark.vcr
async def test_filter_single_api_call(client: ClientType) -> None:
    """Test a search request for a little known security (i.e. only requires one remote call)."""
    query = Query(query="SJIM")
    results = await run_sync_or_async(client.filter, query)

    assert results
    assert all(isinstance(x, FigiResult) for x in results)


@pytest.mark.anyio
@pytest.mark.vcr
async def test_filter_instrument_not_found(client: ClientType) -> None:
    """Test that a search for something that does not exist returns an empty list."""
    query = Query(query="UNKNOWN_TICKER")
    results = await run_sync_or_async(client.filter, query)

    assert isinstance(results, list)
    assert len(results) == 0


@pytest.mark.anyio
@pytest.mark.slow
@pytest.mark.vcr
async def test_filter_multi_api_call(client: ClientType) -> None:
    """
    Test that a search for a query with over 100 results (and therefore necessitating several calls
    taking into account the rate limitations) works fine.

    Careful: this test can take up to 20min to run if the query returns the maximum of 15,000 results
    and no API key was provided.
    """
    query = Query(query="CTA")
    results = await run_sync_or_async(client.filter, query)

    assert results
    assert all(isinstance(x, FigiResult) for x in results)


@pytest.mark.anyio
@pytest.mark.vcr
async def test_get_total_number_of_matches(client: ClientType) -> None:
    """Test that the total number of matches for a given query is returned."""
    # Test for a query that has matches
    query = Query(query="IBM")
    matches = await run_sync_or_async(client.get_total_number_of_matches, query)

    assert isinstance(matches, int)

    # Test for a query that has no matches
    query = Query(query="UNKNOWN_TICKER")
    matches = await run_sync_or_async(client.get_total_number_of_matches, query)

    assert matches == 0


@pytest.mark.anyio
@pytest.mark.vcr
async def test_get_id_types(client: ClientType) -> None:
    """Test that the list of available ID types is returned."""
    id_types = await run_sync_or_async(client.get_id_types)

    assert isinstance(id_types, list)
    assert all(isinstance(x, str) for x in id_types)
    assert "TICKER" in id_types


@pytest.mark.anyio
@pytest.mark.vcr
async def test_get_exch_codes(client: ClientType) -> None:
    """Test that the list of available exchange codes is returned."""
    exch_codes = await run_sync_or_async(client.get_exch_codes)

    assert isinstance(exch_codes, list)
    assert all(isinstance(x, str) for x in exch_codes)
    assert "US" in exch_codes


@pytest.mark.anyio
@pytest.mark.vcr
async def test_get_mic_codes(client: ClientType) -> None:
    """Test that the list of available MIC codes is returned."""
    mic_codes = await run_sync_or_async(client.get_mic_codes)

    assert isinstance(mic_codes, list)
    assert all(isinstance(x, str) for x in mic_codes)
    assert "BATS" in mic_codes


@pytest.mark.anyio
@pytest.mark.vcr
async def test_get_currencies(client: ClientType) -> None:
    """Test that the list of available currencies is returned."""
    currencies = await run_sync_or_async(client.get_currencies)

    assert isinstance(currencies, list)
    assert all(isinstance(x, str) for x in currencies)
    assert "USD" in currencies


@pytest.mark.anyio
@pytest.mark.vcr
async def test_get_market_security_descriptions(client: ClientType) -> None:
    """Test that the list of available market security descriptions is returned."""
    market_security_descriptions = await run_sync_or_async(client.get_market_sec_des)

    assert isinstance(market_security_descriptions, list)
    assert all(isinstance(x, str) for x in market_security_descriptions)
    assert "Equity" in market_security_descriptions


@pytest.mark.anyio
@pytest.mark.vcr
async def test_get_security_types(client: ClientType) -> None:
    """Test that the list of available security types is returned."""
    security_types = await run_sync_or_async(client.get_security_types)

    assert isinstance(security_types, list)
    assert all(isinstance(x, str) for x in security_types)
    assert "Equity Index" in security_types


@pytest.mark.anyio
@pytest.mark.vcr
async def test_get_security_types_2(client: ClientType) -> None:
    """Test that the list of available security types 2 is returned."""
    security_types_2 = await run_sync_or_async(client.get_security_types_2)

    assert isinstance(security_types_2, list)
    assert all(isinstance(x, str) for x in security_types_2)
    assert "Common Stock" in security_types_2


@pytest.mark.anyio
@pytest.mark.vcr
async def test_get_state_codes(client: ClientType) -> None:
    """Test that the list of available state codes is returned."""
    state_codes = await run_sync_or_async(client.get_state_codes)

    assert isinstance(state_codes, list)
    assert all(isinstance(x, str) for x in state_codes)
    assert "AB" in state_codes
