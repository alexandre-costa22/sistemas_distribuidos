import socket
import pickle
import time
import atexit

# Dicionário para armazenar informações da sessão
sessao = {'autenticada': False}
sessoes = {}

host = '127.0.0.1'
port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

def processar_pedido(matricula, total_pedido):
    if matricula in usuarios and sessoes[matricula].autenticado:
        saldo_atual = usuarios[matricula][1]

        if saldo_atual >= total_pedido:
            usuarios[matricula][1] -= total_pedido
            return "Compra realizada"
        else:
            return "Saldo Insuficiente"
    else:
        return "Usuário não autenticado. Faça login para fazer um pedido."

def cadastrar(matricula, senha, saldo=0):
    opcao = 'cadastrar'
    data = {'opcao': opcao, 'matricula': matricula, 'senha': str(senha), 'saldo': saldo}
    return data

def autenticar(matricula, senha):
    opcao = 'autenticar'
    data = {'opcao': opcao, 'matricula': matricula, 'senha': senha}
    return data

def adicionar_saldo(matricula, valor):
    opcao = 'adicionar_saldo'
    data = {'opcao': opcao, 'matricula': matricula, 'valor': valor}
    return data

def fazer_pedido(matricula):
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

    # Enviando dados para o servidor
    client_socket.send(pickle.dumps(data))
    response = pickle.loads(client_socket.recv(1024))

    # Processando a resposta do servidor
    if response == b'OK':
        print("Operação concluída com sucesso.")
    else:
        try:
            response_str = response.decode()
            print(response_str)
        except Exception as e:
            print(f"Erro ao processar a resposta: {e}")

def main():
    global sessao

    while True:
        try:
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
                data = cadastrar(matricula, senha, saldo)

            # Inside the main function
            elif escolha == 2 and not sessao['autenticada']:
                matricula = input("Matrícula: ")
                senha = input("Senha: ")
                data = autenticar(matricula, senha)

    # Update the sessao dictionary with the new matricula
                sessao['matricula'] = matricula

            elif escolha == 3:
                matricula = input("Matrícula: ")
                valor = float(input("Valor a adicionar: "))
                data = adicionar_saldo(matricula, valor)

            elif escolha == 4:
                if sessao['autenticada']:
                    fazer_pedido(sessao['matricula'])
                else:
                    print("Por favor, faça o login para realizar seu pedido!")
                    continue  # Continue para evitar a execução das próximas linhas

            elif escolha == 5:
                break

            print(f"Enviando dados para o servidor: {data}")
            client_socket.send(pickle.dumps(data))
            response = client_socket.recv(1024)

            if response == b'OK':
                print("Operação concluída com sucesso.")
                if escolha == 2 and not sessao['autenticada']:
                    sessao['autenticada'] = True
            else:
                try:
                    response_dict = pickle.loads(response)
                    print(response_dict)
                except Exception as e:
                    print(f"Erro ao processar a resposta: {e}")

            if escolha in [2, 3]:
                response = pickle.loads(response)

                if escolha == 2:
                    if response['autenticado']:
                        sessao = {'autenticada': True, "matricula": matricula}
                        print("Usuário autenticado com sucesso.")
                    else:
                        print("Falha na autenticação.")
                elif escolha == 3:
                    print(f"Saldo atualizado com sucesso. Novo saldo: {response['novo_saldo']}")

                # Corrected fazer_pedido block
                elif data['opcao'] == 'fazer_pedido':
                    if data['matricula'] in sessoes: 
                        matricula = data['matricula']
                        total_pedido = data['total_pedido']
                        resposta_pedido = processar_pedido(matricula, total_pedido)
                        print(resposta_pedido)
                        client_socket.send(resposta_pedido.encode())
                    else:
                        print("Usuário não autenticado. Faça login para fazer um pedido.")


        except OSError as e:
            # Tratamento de erro para lidar com a desconexão inesperada
            print(f"Erro de conexão: {e}")
            break
        except Exception as e:
            print(f"Erro: {e}")

    # Agora, a conexão é fechada apenas após a conclusão da operação de fazer pedido
    atexit.register(client_socket.close)

if __name__ == "__main__":
    main()