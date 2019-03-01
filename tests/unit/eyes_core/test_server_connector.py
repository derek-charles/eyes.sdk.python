import os

import pytest
from mock import patch

from applitools.core import EyesError, ServerConnector, TestResults
from applitools.core.utils.compat import urljoin

API_KEY = "TEST API KEY"
CUSTOM_EYES_SERVER = "http://custom-eyes-server.com"
RUNNING_SESSION_URL = urljoin(CUSTOM_EYES_SERVER, ServerConnector.API_SESSIONS_RUNNING)


@pytest.fixture(scope="function")
def connector():
    # type: () -> ServerConnector
    return ServerConnector(CUSTOM_EYES_SERVER)


@pytest.fixture(scope="function")
def configured_connector():
    # type: () -> ServerConnector
    connector = ServerConnector(CUSTOM_EYES_SERVER)
    connector.api_key = API_KEY
    return connector


@pytest.fixture(scope="function")
def started_connector(configured_connector):
    configured_connector._request = configured_connector._request_factory.create(
        server_url=configured_connector.server_url,
        api_key=configured_connector.api_key,
        timeout=configured_connector.timeout,
    )
    return configured_connector


class MockResponse:
    def __init__(self, json_data, status_code, headers=None):
        self.json_data = json_data
        self.status_code = status_code
        self.headers = headers

    def raise_for_status(self):
        pass

    def json(self):
        return self.json_data

    @property
    def ok(self):
        return self.status_code in (200, 201)


def _request_check(*args, **kwargs):
    if not kwargs["params"]["apiKey"]:
        raise ValueError("API KEY Must be installed")
    if args[0] is None:
        raise ValueError("URL must be present")


def mocked_requests_delete(*args, **kwargs):
    _request_check(*args, **kwargs)
    url = args[0]
    if url == urljoin(RUNNING_SESSION_URL, "some_session_id"):
        return MockResponse(STOP_SESSION, 200)
    return MockResponse(None, 404)


def mocked_requests_post(*args, **kwargs):
    _request_check(*args, **kwargs)
    url = args[0]
    if url == RUNNING_SESSION_URL:
        return MockResponse(
            {
                "id": RUNNING_SESSION["session_id"],
                "url": RUNNING_SESSION["session_url"],
            },
            201,
        )
    elif url == urljoin(RUNNING_SESSION_URL, "some_session_id"):
        return MockResponse({"asExpected": True}, 200)
    elif url == urljoin(RUNNING_SESSION_URL, "data"):
        return MockResponse(
            {}, 200, headers={"Location": RUNNING_SESSION["session_url"]}
        )
    return MockResponse(None, 404)


START_INFO = {
    "agentId": "eyes.core.python/3.15.4",
    "appIdOrName": "TestApp",
    "scenarioIdOrName": "TestName",
    "batchInfo": {
        "name": None,
        "startedAt": "YYYY-MM-DD HH:MM:SS.mmmmmm",
        "id": "UUID ID",
    },
    "envName": None,
    "environment": None,
    "defaultMatchSettings": {"matchLevel": "STRICT", "exact": None},
    "verId": None,
    "branchName": None,
    "parentBranchName": None,
    "properties": [],
}

RUNNING_SESSION = {
    "session_id": "some_session_id",
    "session_url": "http://some-session-url.com",
    "is_new_session": True,
}

STOP_SESSION = {
    "steps": 1,
    "matches": 1,
    "mismatches": 0,
    "missing": 0,
    "exactMatches": None,
    "strictMatches": None,
    "contentMatches": None,
    "layoutMatches": None,
    "noneMatches": None,
    "status": "Passed",
}


def test_set_get_server_url():
    # type: () -> None
    connector = ServerConnector(CUSTOM_EYES_SERVER)
    assert connector.server_url == CUSTOM_EYES_SERVER


def test_set_default_server_url_if_none_passed_as_url():
    connector = ServerConnector(None)
    assert connector.server_url == ServerConnector.DEFAULT_SERVER_URL


def test_set_get_api_key(connector):
    # type: (ServerConnector) -> None
    connector.api_key = API_KEY
    assert connector.api_key == API_KEY


def test_get_api_key_if_not_settled(connector):
    # type: (ServerConnector) -> None
    os.environ["APPLITOOLS_API_KEY"] = API_KEY
    assert connector.api_key == API_KEY


def test_set_get_timeout(connector):
    # type: (ServerConnector) -> None
    connector.timeout = 100
    assert connector.timeout == 100


def test_is_session_started_True(started_connector):
    assert started_connector.is_session_started


def test_is_session_started_False(configured_connector):
    assert not configured_connector.is_session_started


def test_start_session(configured_connector):
    # type: (ServerConnector) -> None
    with patch("requests.post", side_effect=mocked_requests_post):
        respo = configured_connector.start_session(START_INFO)
    assert respo == RUNNING_SESSION


def test_match_window(started_connector):
    #  type: (ServerConnector) -> None
    with patch("requests.post", side_effect=mocked_requests_post):
        as_expected = started_connector.match_window(RUNNING_SESSION, b"data")
    assert as_expected


def test_post_dom_snapshot(started_connector):
    #  type: (ServerConnector) -> None
    with patch("requests.post", side_effect=mocked_requests_post):
        dom_url = started_connector.post_dom_snapshot("{HTML: []")
    assert dom_url == RUNNING_SESSION["session_url"]


def test_stop_session(started_connector):
    #  type: (ServerConnector) -> None
    with patch("requests.delete", side_effect=mocked_requests_delete):
        respo = started_connector.stop_session(
            RUNNING_SESSION, is_aborted=False, save=False
        )
    pr = STOP_SESSION
    assert vars(respo) == vars(
        TestResults(
            pr["steps"],
            pr["matches"],
            pr["mismatches"],
            pr["missing"],
            pr["exactMatches"],
            pr["strictMatches"],
            pr["contentMatches"],
            pr["layoutMatches"],
            pr["noneMatches"],
            pr["status"],
        )
    )
    # should be False after stop_session
    assert not started_connector.is_session_started


def test_raise_error_when_session_was_not_run(configured_connector):
    with pytest.raises(EyesError):
        configured_connector.match_window(RUNNING_SESSION, b"data")
    with pytest.raises(EyesError):
        configured_connector.post_dom_snapshot("{HTML: []")
    with pytest.raises(EyesError):
        configured_connector.stop_session(RUNNING_SESSION, is_aborted=False, save=False)


def test_request_with_changed_values(configured_connector):
    new_timeout = 99999
    new_api_key = "NEW API KEY"
    new_server_url = "http://new-server.com/"
    configured_connector.timeout = new_timeout
    configured_connector.api_key = new_api_key
    configured_connector.server_url = new_server_url

    with patch("requests.post") as mocked_post:
        configured_connector.start_session(START_INFO)

    assert mocked_post.call_args[1]["timeout"] == new_timeout
    assert mocked_post.call_args[1]["params"]["apiKey"] == new_api_key
    assert new_server_url in mocked_post.call_args[0][0]