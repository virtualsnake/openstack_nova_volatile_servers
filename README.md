## Prerequisite:
- Linux (tested on Ubuntu 18.04.6 LTS)
- Docker and Docker-compose installed

## How to run api server:

1) Source your openstack env file `rc.sh`. (Most likely, it will ask you to enter the user's password)
```bash
source /path/to/your/rc.sh
```

2) Call prepare_env.sh script in root of this project
```bash
./prepare_env.sh
```

3) Spin up docker-compose
```bash
docker-compose up
```

