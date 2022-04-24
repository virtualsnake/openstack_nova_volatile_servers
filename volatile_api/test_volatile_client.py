import sys
from unittest.mock import patch, MagicMock

import pytest

sys.modules['openstack'] = MagicMock()
sys.modules['openstack.exceptions'] = MagicMock()
from volatile_api.volatile_client import client


@pytest.fixture
def os_connection():
    with patch('volatile_api.volatile_client.client.conn') as mock_connection:
        yield mock_connection


class TestClient:
    def test_getServer(self, os_connection):
        client.getServer("test1")
        os_connection.get_server.assert_called_once_with("test1")

    def test_getServers(self, os_connection):
        client.getServers()
        os_connection.list_servers.assert_called_once_with()

    def test_createServer(self, os_connection: MagicMock):
        data = {"name": "test2", "id": "test_id"}
        os_connection.create_server.return_value = data
        os_connection.get_server_by_id.return_value = data
        server = client.createServer("test2", "normal")
        os_connection.get_server_by_id.assert_called_once_with("test_id")
        os_connection.create_server.assert_called_once_with(
            "test2", image=os_connection.get_image(), flavor=os_connection.get_flavor(),
            network=os_connection.get_network(), wait=True, auto_ip=False
        )
        assert server == data

    def test_deleteServer(self, os_connection):
        pass

    def test__deleteVolatileServer(self, os_connection):
        pass
