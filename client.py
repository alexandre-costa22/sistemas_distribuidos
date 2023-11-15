import socket
import json

class ClienteTerminal:
    def __init__(self):
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_cliente.connect(('localhost', 12345))
        self.matricula = None
        self.senha = None
        self.quantia = 0

    def criar_usuario(self):
        matricula = input("Digite sua matrícula: ")
        senha = input("Digite sua senha: ")

        add_fundos = input("Deseja adicionar fundos? S/N ")
        if add_fundos.upper() == 'S':
            self.quantia = int(input("Quantas reais deseja depositar? "))

        user_info = {"matricula": matricula, "senha": senha, "saldo": self.quantia, "escolha": "cadastro"}
        self.socket_cliente.send(json.dumps(user_info).encode())
        resposta_cadastro = self.socket_cliente.recv(1024).decode()
        print(resposta_cadastro)

    def autenticar_usuario(self):
        matricula = input("Matrícula: ")
        senha = input("Senha: ")
        dados_cliente = {"matricula": matricula, "senha": senha, "escolha": "login"}
        self.socket_cliente.send(json.dumps(dados_cliente).encode())
        resposta_autenticacao = self.socket_cliente.recv(1024).decode().strip()
        print(resposta_autenticacao)

        if "Cadastro realizado com sucesso!" in resposta_autenticacao or "Autenticado com sucesso!" in resposta_autenticacao:
            print("Autenticação bem-sucedida!\n")
            cardapio = self.socket_cliente.recv(1024).decode()
            print(cardapio)
        else:
            print(resposta_autenticacao)
            print("Falha na autenticação. Matrícula ou senha incorretas.\n")

    def exibir_cardapio(self):
        cardapio = self.socket_cliente.recv(1024).decode()
        print(cardapio)

    def fazer_pedido(self, pedido):
        self.socket_cliente.send(pedido.encode())
        resposta = self.socket_cliente.recv(1024).decode()
        print(resposta)

if __name__ == "__main__":
    cliente = ClienteTerminal()

    while True:
        print("Se não tiver cadastro, digite 1. Se sim, digite 2: ")
        escolha = input()

        if escolha == '1':
            cliente.criar_usuario()

        elif escolha == '2':
            cliente.autenticar_usuario()
            cardapio = cliente.socket_cliente.recv(1024).decode()
            print(cardapio)
            break

    while True:
        pedido = input("Faça seu pedido (ou 'sair' para encerrar): ")
        if pedido.lower() == 'sair':
            break
        else:
            cliente.fazer_pedido(pedido)
