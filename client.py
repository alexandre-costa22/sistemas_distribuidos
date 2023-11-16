import socket
import pickle

def processar_pedido(matricula, total_pedido, usuarios):
    if matricula in usuarios and usuarios[matricula]['autenticado']:
        saldo_atual = usuarios[matricula]['saldo']

        if saldo_atual >= total_pedido:
            usuarios[matricula]['saldo'] -= total_pedido
            return "Compra realizada"
        else:
            return "Saldo Insuficiente"
    else:
        return "Usuário não autenticado. Faça login para fazer um pedido."

def cadastrar(matricula, senha, saldo=0):
    return {'opcao': 'cadastrar', 'matricula': matricula, 'senha': str(senha), 'saldo': saldo}

def autenticar(matricula, senha, usuarios):
    if matricula in usuarios and usuarios[matricula]['senha'] == senha:
        usuarios[matricula]['autenticado'] = True
        return {'opcao': 'autenticar', 'matricula': matricula, 'senha': senha, 'autenticado': True}
    else:
        return {'opcao': 'autenticar', 'matricula': matricula, 'senha': senha, 'autenticado': False}

def adicionar_saldo(matricula, valor, usuarios):
    if matricula in usuarios and usuarios[matricula]['autenticado']:
        usuarios[matricula]['saldo'] += valor
        return {'opcao': 'adicionar_saldo', 'matricula': matricula, 'valor': valor, 'novo_saldo': usuarios[matricula]['saldo']}
    else:
        return {'opcao': 'adicionar_saldo', 'matricula': matricula, 'valor': valor, 'erro': 'Usuário não autenticado'}

def fazer_pedido(matricula, usuarios):
    print("1. Capuccino")
    print("2. Mocaccino")
    print("3. Chocolate Quente")
    print("4. Chá Matte")
    print("5. Chá Gelado ")
    print("6. Salgado")
    print("7. Doces")
    total = float(0)
    
    while True:
        print("Digite SAIR para sair")
        pedido = input("Escolha seu pedido: ")
        if pedido == '1':
            total += 7
        elif pedido == '2':
            total += 8.50
        elif pedido == '3':
            total += 5.50
        elif pedido == '4':
            total += 8.50
        elif pedido == '5':
            total += 12
        elif pedido == '6':
            total += 15
        elif pedido.lower() == 'sair':
            print("SAINDO...")
            break
    
    print(f'O seu total deu {total}')
    opcao = 'fazer_pedido'
    data = {'opcao': opcao, 'matricula': matricula, 'total_pedido': total}

    print(f"Enviando dados para o servidor: {data}")
    client_socket.send(pickle.dumps(data))
    response = client_socket.recv(1024)

    try:
        response_dict = pickle.loads(response)

        if response_dict.get('novo_saldo') is not None:
            usuarios[matricula]['saldo'] = response_dict['novo_saldo']

        print(response_dict['mensagem'])

    except Exception as e:
        print(f"Erro ao processar a resposta: {e}")
    return data

def main():
    usuarios = {}

    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        while True:
            print("1. Cadastro")
            print("2. Autenticação")
            print("3. Adicionar Fundos")
            print("4. Fazer Pedidos")
            print("5. Sair")
            escolha = int(input("Escolha a opção: "))

            if escolha == 1:
                matricula = input("Matrícula: ")
                senha = input("Senha: ")
                saldo = float(input("Saldo (opcional): "))
                data = cadastrar(matricula, senha, saldo=saldo)

            elif escolha == 2:
                matricula = input("Matrícula: ")
                senha = input("Senha: ")
                data = autenticar(matricula, senha, usuarios)

            elif escolha == 3:
                matricula = input("Matrícula: ")
                valor = float(input("Valor a adicionar: "))
                data = adicionar_saldo(matricula, valor, usuarios)

            elif escolha == 4:
                if 'autenticado' in usuarios.get(matricula, {}) and usuarios[matricula]['autenticado']:
                    fazer_pedido(matricula, usuarios, client_socket)
                else:
                    print("Por favor, faça o login para realizar seu pedido!")
                    continue

            elif escolha == 5:
                break

            print(f"Enviando dados para o servidor: {data}")
            client_socket.send(pickle.dumps(data))
            response = client_socket.recv(1024)

            try:
                response_dict = pickle.loads(response)

                if response_dict.get('autenticado'):
                    usuarios[matricula] = {'autenticado': True, 'senha': senha, 'saldo': response_dict.get('novo_saldo')}
                    print("Usuário autenticado com sucesso.")
                elif 'erro' in response_dict:
                    print(response_dict['erro'])
                else:
                    print("Operação concluída com sucesso.")

            except Exception as e:
                print(f"Erro ao processar a resposta: {e}")

    except OSError as e:
        print(f"Erro de conexão: {e}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
