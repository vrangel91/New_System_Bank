# Menu do Usuário
import textwrap


def menu():
    menu = """\n
    ================= MENU =================
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova Conta
    [5]\tNovo usuário
    [6]\tListar Contas
    [7]\tSair    
    
    """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f'Depósito: R$ {valor}\n'
        print('Saldo: R$ {:.2f}'.format(saldo))
    else:
        print('@@@ Operação falhou! Deposito deve ser maior que R$ 0,00 Reais. @@@')
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print('@@@ Operação falhou! Você não tem saldo suficiente. @@@ ')

    elif excedeu_limite:
        print('@@@ Operação falhou! O valor do saque excede o limite. @@@ ')

    elif excedeu_saques:
        print('@@@ Operação falhou! Saque não autorizado! Limite de 3 saques atingido. @@@ ')

    elif valor > 0:
        saldo -= valor
        extrato += f'Saque: \t\tR$ {valor:.2f}\n'
        numero_saques += 1
        print('=== Saque realizado com sucesso! ===')
    else:
        print('\n@@@ Operação falhou! O valor informado é inválido @@@')

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n============ EXTRATO ============")
    print('Não foram existe movimentações realizadas. ' if not extrato else extrato)
    print('\nSaldo: R$ {:.2f}'.format(saldo))
    print("==================================")

    return saldo, extrato


def criar_usuario(usuarios):
    cpf = input('Informe o CPF (somente números): ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('\n@@@ Já existe usuário com esse CPF! @@@')
        return

    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ')
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print('=== Usuário criado com sucesso! ===')


def filtrar_usuario(cpf, usuarios):
    usuarios_filtados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtados[0] if usuarios_filtados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe o CPF do usuário: ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('\n=== Conta criada com sucesso! ===')
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print('\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@')


def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print('=' * 100)
        print(linha)


def main():
    limites_saques = 3
    agencia = '0001'

    saldo = 0
    limite = 500
    extrato = ''
    numero_saques = 0
    usuarios = []
    contas = []
    numero_conta = 0


    # Loop
    while True:
        opcao = menu()

        #  Escolhendo a opção depositar
        if opcao == '1':
            valor = float(input('Informe o valor do depósito: R$ '))
            saldo, extrato = depositar(saldo, valor, extrato)

        #  Escolhendo a opção sacar
        elif opcao == '2':
            valor = float(input('Informe o valor do saque: R$ '))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=limites_saques
            )

        # Mostrando extrato da conta
        elif opcao == '3':
            exibir_extrato(saldo, extrato=extrato)

        # Saindo do programa
        elif opcao == '4':
            criar_usuario(usuarios)

        elif opcao == '5':
            numero_conta = len(contas) + 1
            conta = criar_conta(agencia, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == '6':
            listar_contas(contas)

        elif opcao == '7':
            break
        # Mensagem caso digite uma opção inválida
        else:
            print('Operação inválida, por favor selecione novamente a operação desejada.')


main()