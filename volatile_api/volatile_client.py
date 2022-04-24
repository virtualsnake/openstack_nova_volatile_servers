import enum
import logging

import openstack
import openstack.exceptions

from volatile_api.utils import initLogger

FLAVOR = 'SL1.1-1024-8'
IMAGE = "Ubuntu 18.04 LTS 64-bit"
CIDR = '10.0.0.0/24'
NETWORK = "private"
SUBNET = '{}_subnet'.format(NETWORK)

# openstack.enable_logging(True, stream=sys.stdout)

logger = logging.getLogger(__name__)

initLogger(logger)


class ServerTypes(enum.Enum):
    normal = "normal"
    volatile = "volatile"


def extractServerType(server):
    # default is normal type
    ret = ServerTypes.normal.value
    if server:
        metadata = getattr(server, "metadata", None)
        if metadata is None:
            metadata = server.get("metadata", None)
        if metadata:
            ret = metadata.get("server_type", ServerTypes.normal.value)
    return ret


class OpenStackClient:
    def __init__(self):
        # openstacksdk will produce a cloud config object named envvars containing your values from the environment.
        self.conn = openstack.connect(cloud='envvars')

    def getServer(self, name):
        return self.conn.get_server(name)

    def getServers(self):
        return self.conn.list_servers()

    def createServer(self, name: str, server_type: str) -> dict:
        logger.debug(f"createServer(self, {name}, {server_type})")
        conn = self.conn

        image = conn.get_image(IMAGE)
        flavor = conn.get_flavor(FLAVOR)
        network = self._prepare_network()

        def create_server():
            logger.debug(f"Creating server {name}")
            # Boot a server, wait for it to boot
            ret = conn.create_server(name, image=image, flavor=flavor, network=network, wait=True, auto_ip=False)
            logger.debug(f"Server created {name}")
            return ret

        server = None
        try:
            server = create_server()
        except openstack.exceptions.HttpException as e:
            logger.debug(f"Got exception during server creation")
            if e.status_code == 403 and "Quota exceeded" in e.details:
                logger.debug(f"Not enough quota for resource creation - {e.details}")
                success = self._deleteVolatileServer()
                if success:
                    server = create_server()
                else:
                    raise
        conn.set_server_metadata(server["id"], metadata={"server_type": server_type})

        # get server object with updated metadata
        server = conn.get_server_by_id(server["id"])
        return server

    def _prepare_network(self):
        conn = self.conn
        network = conn.get_network(NETWORK)
        if network is None:
            network = conn.create_network(NETWORK)
        subnet = conn.get_subnet(SUBNET)
        if subnet is None:
            conn.create_subnet(network_name_or_id=NETWORK, cidr=CIDR, subnet_name=SUBNET)
        return network

    def deleteServer(self, name) -> bool:
        logger.debug(f"Deleting server {name}")
        ret = self.conn.delete_server(name, wait=True)
        if ret:
            logger.debug("Delete succeeded")
        else:
            logger.debug("Server for delete does not exist")
        return ret

    def _deleteVolatileServer(self) -> bool:
        logger.debug("Trying to delete one of volatile servers")
        volatile_servers = [x for x in self.getServers() if ServerTypes(extractServerType(x)) is ServerTypes.volatile]
        volatile_servers_count = len(volatile_servers)
        logger.debug(f"Currently we have {volatile_servers_count} volatile servers")
        if volatile_servers_count > 0:
            logger.debug("Going to delete one of them")
            server_for_delete = volatile_servers[-1]
            self.deleteServer(server_for_delete["id"])
            return True
        else:
            return False


client = OpenStackClient()
