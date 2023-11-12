import socket

class ClienteTerminal:
    def __init__(self, matricula, senha):
        self.matricula = matricula
        self.senha = senha
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.connect(('localhost', 12345))

    def autenticar(self):
        mensagem = f"{self.matricula},{self.senha}"
        self.servidor.send(mensagem.encode())
        resposta = self.servidor.recv(1024).decode()
        print(resposta)

    def fazer_pedido(self, pedido):
        self.servidor.send(pedido.encode())
        resposta = self.servidor.recv(1024).decode()
        print(resposta)

    def sair(self):
        self.fazer_pedido("sair")

if __name__ == "__main__":
    matricula = input("Matrícula: ")
    senha = input("Senha: ")

    cliente = ClienteTerminal(matricula, senha)
    cliente.autenticar()

    while True:
        pedido = input("Faça seu pedido (ou 'sair' para encerrar): ")
        if pedido.lower() == 'sair':
            cliente.sair()
            break
        else:
            cliente.fazer_pedido(pedido)
