## Prerequisite:
- Linux (tested on Ubuntu 18.04.6 LTS)
- Docker and Docker-compose installed

## How to run api server

1) Source your openstack env file `rc.sh`. (Most likely, it will ask you to enter the user's password)
   ```bash
   source /path/to/your/rc.sh
   ```
   
2) Call prepare_env.sh script in root of this project
   ```bash
   ./prepare_env.sh
   ```

3) Run application
    
    * **Production mode**  
    nginx and uwsgi api server  
    endpoint port is  **80**
        
        ```bash
        docker-compose up
        ```
    * **Debug mode**  
    flask debug application  
    endpoint port is  **5000**
      ```bash
      ./build_image.sh && ./run_app.sh
      ```
 
4) *(Optional)* Run tests *(uses 5000 port)* 
    ```bash
    ./run_e2e_tests.sh
    ```

#### Api call examples:
List servers
```bash
curl http://localhost/servers
```

Create new normal server
```bash 
curl -X POST -d '{"server_name":"server1", "server_type":"normal"}' -H "Content-Type: application/json" http://localhost/servers
```
Create new volatile server (may be deleted in order to free resources for creating new servers)
```bash
curl -X POST -d '{"server_name":"server1", "server_type":"normal"}' -H "Content-Type: application/json" http://localhost/servers
```
Get server by name or id
```bash
curl -X GET http://localhost/servers/<server_name_or_id>
```
delete server by name or id
```bash
curl -X DELETE http://localhost/servers/<server_name_or_id>
```