import socket
import threading
import queue

class CantinaServer:
    def __init__(self):
        self.clientes_conectados = {}
        self.fila_pedidos = queue.Queue()
        self.mutex = threading.Lock()

    def iniciar_servidor(self, host, porta):
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind((host, porta))
        self.servidor.listen(5)
        print(f"Servidor iniciado em {host}:{porta}")

        while True:
            cliente, endereco = self.servidor.accept()
            threading.Thread(target=self.lidar_cliente, args=(cliente,)).start()

    def lidar_cliente(self, cliente):
        matricula, senha = cliente.recv(1024).decode().split(',')
        if self.autenticar_cliente(matricula, senha):
            self.clientes_conectados[matricula] = cliente
            cliente.send("Autenticado com sucesso!".encode())
            self.enviar_cardapio(matricula)
            self.lidar_pedidos(matricula)
        else:
            cliente.send("Autenticação falhou!".encode())

    def autenticar_cliente(self, matricula, senha):
        # Lógica de autenticação aqui
        return True

    def enviar_cardapio(self, matricula):
        cardapio = "Cardápio:\n1. Produto 1\n2. Produto 2\n3. Produto 3\n"
        self.clientes_conectados[matricula].send(cardapio.encode())

    def lidar_pedidos(self, matricula):
        while True:
            pedido = self.clientes_conectados[matricula].recv(1024).decode()
            if pedido == "sair":
                break
            else:
                self.mutex.acquire()
                self.fila_pedidos.put((matricula, pedido))
                self.mutex.release()

    def iniciar_atendimento(self):
        while True:
            if not self.fila_pedidos.empty():
                pedido = self.fila_pedidos.get()
                matricula, pedido_cliente = pedido
                self.enviar_pedido_atendimento(matricula, pedido_cliente)

    def enviar_pedido_atendimento(self, matricula, pedido):
        atendente = input("Atendente: ")
        self.clientes_conectados[matricula].send(f"Atendente: {atendente}, Pedido: {pedido} concluído!".encode())


if __name__ == "__main__":
    servidor = CantinaServer()
    threading.Thread(target=servidor.iniciar_servidor, args=('localhost', 12345)).start()
    threading.Thread(target=servidor.iniciar_atendimento).start()
