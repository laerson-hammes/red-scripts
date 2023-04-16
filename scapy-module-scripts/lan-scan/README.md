# Lan Scan

Ao executar o script você pode passar por parâmetro o IP/range ao qual deseja enviar a requisição ARP. Caso não seja especificado, o mesmo será solicitado.

## Examplo:

### -ipr:

> python .\lan-scan.py -ipr "192.168.1.0/24"

### --help ou -h para ajuda:

> python .\lan-scan.py --help

> python .\lan-scan.py -h

## Observação

O módulo **scapy** não é completamente compatível com sistema operacional Windows, logo, pode ser que ocorra algum erro de compatibilidade.
