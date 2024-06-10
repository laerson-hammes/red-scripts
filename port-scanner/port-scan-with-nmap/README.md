# NMAP Port Scan

Para executar o script você precisa ter instalado em sua máquina o NMAP, o mesmo pode ser encontrado em <https://nmap.org/download.html>.
Após ter instalado o NMAP, execute o script. Você pode passar por parâmetro o hostname / domain e a porta / um range de portas. 

## Example:

### --host:

> python .\port-scan.py --host "hostname.com"

O padrão, caso não seja especificado, é "127.0.0.1"

### --port:

> python .\port-scan.py --port "80"

Informando um range de portas:

> python .\port-scan.py --port "22-443"

O padrão, caso não seja especificado, é "22-40043"

### --help ou -h para ajuda:

> python .\port-scan.py --help

> python .\port-scan.py -h
