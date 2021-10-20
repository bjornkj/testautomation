import http.client
from dataclasses import dataclass
import requests
import pytest
from http import HTTPStatus


@dataclass
class User:
    id: int
    name: str
    email: str
    gender: str
    status: str


API_TOKEN = "api_token"
GOREST_USERS = "https://gorest.co.in/public/v1/users"


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


@pytest.fixture
def header(api_token):
    # {"authorization": "Bearer 3998tyrhg4235uh23"}
    return {"authorization": f"Bearer {api_token}"}


def expected_http_code(exp: int, got: int) -> str:
    return f"Expected {exp} got {got}"


def format_fails(fails: list[str]) -> str:
    return "Errors:\n" + "\n".join(fails)



# Här har vi lagt testdatan som en fixture, kan hanteras på andra sätt
@pytest.fixture
def user_data():
    return {"name": "Testperson Testsson",
            "email": "ensdf@mladres4s.se",
            "gender": "male",
            "status": "active"}


# Följande fixture skapar en ny användare baserat på datan i user_data
# vi får som resultat det responseobjekt som skapas vid anrop mot APIet
# Användaren kommer automatiskt att tas bort när testet är klart
@pytest.fixture
def user_request(user_data, header) -> requests.Response:
    result = requests.post(GOREST_USERS, data=user_data, headers=header)
    yield result
    requests.delete(GOREST_USERS + f"/{result.json()['data']['id']}",
                    headers=header)


# Följande fixture använder user_request fixturen men "packar upp" datan och skapar en instans av User-klassen som
# vi får tillgång till om vi använder fixturen
@pytest.fixture
def user(user_request) -> User:
    yield User(**user_request.json()['data'])


# Ett mycket enkelt test som kontrollerar om vi fick rätt svarskod när vi skapar en ny användare
def test_user_request(user_request):
    assert user_request.status_code == HTTPStatus.CREATED


# Ett simpelt test där vi kontrollerar att innehållet i den respons vi får när vi skapar en ny
# user matchar den data vi skickade
def test_user_content(user, user_data):
    assert user.name == user_data['name']


# Här är ett lite mer utförligt test där vi inte nyttjar en fixtur för att skapa ny användare'
# Vi tvingas därför att själva ta bort användaren i slutet av testet.
# Var uppmärksamma på hur den typen av kod är placerad i förhållande till asserts!
# Om en assert fallerar kommer körningen av testet att stanna och eventuell kod efter
# asserten kommer inte köras.
# I det här testet vill vi kontrollera flera saker och för att undvika ovan nämnda problem
# med att körningen avbryts när en assert fallerar gör vi istället motsvarande kontroller
# med hjälp av vanliga if-satser och sparar resultatet i en lista.
# I slutet av testet görs istället en assert på att listan med fel är tom.
def test_create_user(user_data, header):
    fails = []
    result = requests.post(GOREST_USERS, data=user_data, headers=header)
    result_data = result.json()
    if not result.status_code == HTTPStatus.CREATED:
        fails.append(f"Expected result code {HTTPStatus.CREATED} got {result.status_code}")

    del_result = requests.delete(GOREST_USERS + f"/{result_data['data']['id']}",
                                 headers=header)
    if not del_result.status_code == HTTPStatus.NO_CONTENT:
        fails.append(f"Expected result code {HTTPStatus.NO_CONTENT} gpt {del_result.status_code}")
    assert not fails, '\n'.join(fails)
