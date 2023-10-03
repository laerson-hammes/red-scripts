# MAC ADDRESS Changer

Script que altera o endereço MAC do Adaptador de Rede. Funciona para **Windows** e **Linux**.
Para a versão Windows, o usuário não precisa especificar nada, o script pega o MAC ADDRESS da placa de rede física e o altera, não sendo necessário reiniciar o adaptador. Já para a versão para Linux, o usuário precisa especificar o adaptador ao qual deseja alterar o MAC ADDRESS e após, reinicia-lo.
O adaptador de rede pode ser especificado a partir de Command-Line Interface - CLI usando a seguinte nomenclatura:

### -i ou --interface:

> python .\change-mac.py -i {interface_name}

> python .\change-mac.py --interface {interface_name}

Caso o adaptador não seja passado na hora da chamada do código, o mesmo será questiuonado em seguida.

### Reiniciando o adaptador de rede

> Windows: Restart-NetAdapter
> Linux: ...
