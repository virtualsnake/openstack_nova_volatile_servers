import pytest
import requests


@pytest.fixture
def api_url():
    return "http://localhost:5000"


@pytest.fixture
def clean_env(api_url):
    def clean():
        for server in requests.get(api_url + "/servers").json()['servers']:
            requests.delete(api_url + "/servers/" + server['id'])

    clean()
    yield
    clean()


@pytest.fixture
def predefined_server(api_url, clean_env, request):
    json_data = {"server_type": request.param['type'],
                 "server_name": request.param['name']}
    print(f"Post json {json_data}")
    response = requests.post(api_url + "/servers", json=json_data)
    print(response.content)
    assert response.status_code == 201


class TestServer:
    def test_get(self, api_url):
        response = requests.get(api_url + "/servers/not_existing_server")
        assert response.status_code == 404

    def test_delete_not_existing(self, api_url, clean_env):
        for _ in range(2):
            response = requests.delete(api_url + "/servers/not_existing_server")
            assert response.status_code == 204

    @pytest.mark.parametrize("predefined_server,server_name",
                             [({'name': 'pre_test1', 'type': 'normal'}, 'pre_test1'),
                              ({'name': 'pre_test2', 'type': 'volatile'}, 'pre_test2')],
                             indirect=["predefined_server"])
    def test_delete(self, api_url, predefined_server, server_name):
        response = requests.delete(api_url + "/servers/" + server_name)
        assert response.status_code == 204
        response = requests.get(api_url + "/servers")
        assert len(response.json()['servers']) == 0


class TestServerList:
    def test_get(self, api_url, clean_env):
        response = requests.get(api_url + "/servers")
        assert response.status_code == 200
        assert response.json() == {'servers': []}

    @pytest.mark.parametrize("server_name,server_type,expected_error_code", [("test1", "normal", 201),
                                                                             ("test2", "volatile", 201),
                                                                             ("test3", "incorrect_type", 400)])
    def test_post(self, server_name, server_type, expected_error_code, api_url, clean_env):
        response = requests.post(api_url + "/servers",
                                 json={"server_type": server_type, "server_name": server_name})
        assert response.status_code == expected_error_code
        if expected_error_code >= 400:
            return
        assert 'servers' in response.json()
        servers = response.json()['servers']
        assert len(servers) == 1
        assert servers[0]["name"] == server_name
        assert servers[0]["type"] == server_type
        assert 'id' in servers[0]

# TODO: implement e2e cases when "volatile" server deleted in order to create space for new one
