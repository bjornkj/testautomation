import requests
import pytest
import http
from test_gorest import api_token
GOREST_USERS = "https://gorest.co.in/public/v1/users"



def create_user():
    person = {"name": "Testperson Testsson",
              "email": "enannan@mailaddress.se",
              "gender": "male",
              "status": "active"}

    res = requests.post(GOREST_USERS, data=person,
                        headers={"authorization": f"Bearer {api_token()}"})
    print(res)
    print(res.json())

create_user()
