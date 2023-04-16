# Port Scan with Socket and Thread

Ao executar o script você pode passar por parâmetro o hostname / domain e a porta / um range de portas. 

## Examplo:

### --host:

> python .\port-scan.py --host "hostname.com"

O padrão, caso não seja especificado, é "127.0.0.1"

### --port

> python .\port-scan.py --port "80"

Informando um range de portas:

> python .\port-scan.py --port "22-443"

O padrão, caso não seja especificado, é "1-65535"
