import socket
import pickle

usuarios_cadastrados = []

def cadastrar_usuario(matricula, senha, saldo=0):
    usuario = {'matricula': matricula, 'senha': senha, 'saldo': saldo, 'autenticado': False}
    usuarios_cadastrados.append(usuario)
    return usuario

def processar_pedido(data, usuarios):
    opcao = data['opcao']
    matricula = data['matricula']

    if opcao == 'cadastrar':
        senha = data['senha']
        saldo = data.get('saldo', 0)
        usuarios[matricula] = cadastrar_usuario(matricula, senha, saldo)
        return {'mensagem': 'Usuário cadastrado com sucesso!'}

    elif opcao == 'autenticar':
        senha = data['senha']
        for usuario in usuarios_cadastrados:
            if matricula == usuario['matricula'] and usuario['senha'] == senha:
                usuarios[matricula]['autenticado'] = True
                return {'autenticado': True, 'novo_saldo': usuarios[matricula]['saldo']}
        return {'autenticado': False, 'erro': 'Matrícula ou senha incorretos.'}

    elif opcao == 'adicionar_saldo':
        valor = data['valor']
        usuarios[matricula]['saldo'] += valor
        return {'mensagem': 'Saldo adicionado com sucesso!', 'novo_saldo': usuarios[matricula]['saldo']}

    elif opcao == 'fazer_pedido':
        total_pedido = data['total_pedido']

        if usuarios[matricula]['saldo'] >= total_pedido:
            usuarios[matricula]['saldo'] -= total_pedido
            return {'mensagem': 'Pedido realizado com sucesso!', 'novo_saldo': usuarios[matricula]['saldo']}
        else:
            return {'mensagem': 'Saldo insuficiente para realizar o pedido. Pedido cancelado.', 'novo_saldo': usuarios[matricula]['saldo']}


def main():
    usuarios = {}
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Servidor ouvindo em {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexão estabelecida com {client_address}")

        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                data_dict = pickle.loads(data)
                response = processar_pedido(data_dict, usuarios)
                client_socket.send(pickle.dumps(response))

        except Exception as e:
            print(f"Erro na conexão: {e}")

        finally:
            client_socket.close()

if __name__ == "__main__":
    main()
