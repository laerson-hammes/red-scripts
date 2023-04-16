# Lan Scan

Ao executar o script você pode passar por parâmetro o IP/range ao qual deseja enviar a requisição ARP.

## Examplo:

> python .\lan-scan.py -ipr "192.168.1.0/24"

Caso não seja especificado, o mesmo será solicitado.

## Observação

O módulo **scapy** não é completamente compatível com sistema operacional Windows, logo, pode ser que ocorra algum erro de compatibilidade.
