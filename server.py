import socket
import pickle
import threading
import time

# Dicionário para armazenar dados dos usuários (matrícula: [senha, saldo])
usuarios = {}

# Dicionário para armazenar informações de sessão (matrícula: sessao)
sessoes = {}

# Classe para representar a sessão do usuário
class Sessao:
    def __init__(self, matricula):
        self.matricula = matricula
        self.autenticado = False

def cadastrar_usuario(matricula, senha, saldo):
    usuarios[matricula] = [senha, saldo]

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

def adicionar_saldo(matricula, valor):
    usuarios[matricula][1] += valor

def autenticar_usuario(matricula, senha):
    if matricula in usuarios and usuarios[matricula][0] == senha:
        return True
    return False

def fazer_pedido(matricula):
    if matricula in sessoes and sessoes[matricula].autenticado:
        return True
    return False

def lidar_com_cliente(client_socket, addr):
    print(f"Conexão de {addr}")

    data = client_socket.recv(1024)
    print(f"Dados recebidos do cliente: {data}")

    data = pickle.loads(data)
    print(f"Dados desserializados: {data}")

    if data['opcao'] == 'cadastrar':
        matricula = data['matricula']
        senha = data['senha']
        saldo = data.get('saldo')
        cadastrar_usuario(matricula, senha, saldo)

    elif data['opcao'] == 'autenticar':
        matricula = data['matricula']
        senha = data['senha']
        resultado = autenticar_usuario(matricula, senha)
        resposta = {'autenticado': resultado}
        
        if resultado:
            # Cria uma nova sessão para o usuário autenticado
            sessoes[matricula] = Sessao(matricula)
            sessoes[matricula].autenticado = True

        print(f"Enviando resposta para o cliente: {resposta}")
        client_socket.send(pickle.dumps(resposta))

    elif data['opcao'] == 'adicionar_saldo':
        matricula = data['matricula']
        valor = data['valor']
        adicionar_saldo(matricula, valor)

    elif data['opcao'] == 'fazer_pedido':
        if data[matricula] in sessoes: 
            matricula = data['matricula']
            total_pedido = data['total_pedido']
            resposta_pedido = processar_pedido(matricula, total_pedido)
            print(resposta_pedido)
            client_socket.send(resposta_pedido.encode())
        else:
            print("Usuário não autenticado. Faça login para fazer um pedido.")

    # Aguarda um curto período antes de fechar o socket
    time.sleep(0.1)
    
    # Envia um sinal de confirmação para o cliente
    client_socket.send(b'OK')
    client_socket.close()

def receber_entradas():
    while True:
        entrada = input("Digite 'listar' para exibir os usuários: ")
        if entrada.lower() == 'listar':
            lista_usuarios = listar_usuarios()
            print(f"Listando usuários no servidor: {lista_usuarios}")

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Servidor ouvindo em {host}:{port}")

    # Inicia a thread para receber entradas do servidor
    thread_entradas = threading.Thread(target=receber_entradas, daemon=True)
    thread_entradas.start()

    while True:
        client_socket, addr = server_socket.accept()

        # Inicia uma nova thread para lidar com a conexão do cliente
        thread_cliente = threading.Thread(target=lidar_com_cliente, args=(client_socket, addr))
        thread_cliente.start()
