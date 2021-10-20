import requests
import pytest
from dataclasses import dataclass
from http import HTTPStatus

API_TOKEN = "api_token"
GOREST_USERS = "https://gorest.co.in/public/v1/users"


@dataclass
class User:
    id: int
    name: str
    email: str
    gender: str
    status: str


# Ett test kan delas in i 3-4 olika delar
# 1. Arrange arrangera,
# 2. Act, agera, interagera med SUT
# 3. Assert, kontrollera att utfallet blev som förväntat
# 4. Cleanup, städa, rensa upp sådant vi gjort som kan störa ytterligare tester


# Undvik att spara känslig information i din kod, särskilt om den är under versionskontroll
@pytest.fixture
def api_token() -> str:
    with open(API_TOKEN) as f:
        return f.read().strip()


def expected_http_code(exp: int, got: int) -> str:
    return f"Expected {exp} got {got}"


def format_fails(fails: list[str]) -> str:
    return "Errors:\n" + "\n".join(fails)


@pytest.fixture
def header(api_token) -> dict:
    return {"authorization": f"Bearer {api_token}"}


@pytest.fixture
def user_data():
    return {"name": "Testperson Testsson",
            "email": "enasdf@mladres4s.se",
            "gender": "male",
            "status": "active"}


@pytest.fixture
def user(header, user_data):
    res = requests.post(GOREST_USERS, data=user_data,
                        headers=header)
    yield User(**res.json()['data'])
    requests.delete(f"{GOREST_USERS}/{res.json()['data']['id']}",
                    headers=header)


def test_some_test(user, user_data):
    assert user.name == user_data['name']


def test_create_user(header, user_data):
    fails = []

    result = requests.post(GOREST_USERS, data=user_data,
                           headers=header)
    result_json = result.json()
    if not result.status_code == HTTPStatus.CREATED:
        fails.append(expected_http_code(HTTPStatus.CREATED, result.status_code))

    res_delete = requests.delete(f"{GOREST_USERS}/{result_json['data']['id']}",
                                 headers=header)

    if not res_delete.status_code == HTTPStatus.NO_CONTENT:
        fails.append(expected_http_code(HTTPStatus.CREATED, res_delete.status_code))
    assert not fails, format_fails(fails)


def test_get_all_users():
    fails = []
    result = requests.get(GOREST_USERS)
    result_json = result.json()
    if not result.status_code == HTTPStatus.OK:
        fails.append(expected_http_code(HTTPStatus.OK, result.status_code))
    if "meta" not in result_json:
        fails.append("meta field not present in result json")
    if "data" not in result_json:
        fails.append("data field not present in result json")

    assert not fails, format_fails(fails)
