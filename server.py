import socket
import threading
import queue
import json

class CantinaServer:
    def __init__(self):
        self.clientes_conectados = {}
        self.fila_pedidos = queue.Queue()
        self.mutex = threading.Lock()
        self.cadastro = []

    def iniciar_servidor(self, host, porta):
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind((host, porta))
        self.servidor.listen(5)
        print(f"Servidor iniciado em {host}:{porta}")

        while True:
            cliente, endereco = self.servidor.accept()
            threading.Thread(target=self.lidar_cliente, args=(cliente,)).start()

    def lidar_cliente(self, cliente):
        dados_cliente = cliente.recv(1024).decode()

        try:
            dados_cliente = json.loads(dados_cliente)

            if "escolha" in dados_cliente:
                if dados_cliente["escolha"] == "cadastro":
                    dados_cliente["escolha"] == "login"
                    sucesso_cadastro = self.add_cadastro(dados_cliente, cliente)
                    if sucesso_cadastro:
                        cliente.send("Cadastro realizado com sucesso!\n".encode())
                    else:
                        cliente.send("Erro ao cadastrar usuário.\n".encode())
                elif dados_cliente["escolha"] == "login":
                    matricula = dados_cliente["matricula"]
                    senha = dados_cliente["senha"]
                    if self.autenticar_cliente(matricula, senha):
                        saldo = self.obter_saldo(matricula)
                        if saldo is not None:
                            cliente.send(f"Autenticado com sucesso!\n".encode())
                            self.enviar_cardapio(cliente, matricula)  # Esta linha já está no lugar certo
                            self.lidar_pedidos(cliente, matricula)
                        else:
                            cliente.send("Erro ao obter saldo.\n".encode())
                    else:
                        cliente.send("Falha na autenticação. Matrícula ou senha incorretas.\n".encode())

        except json.JSONDecodeError:
            cliente.send("Erro ao processar dados do cliente.\n".encode())

    def add_cadastro(self, novo_cliente, cliente):
        self.mutex.acquire()

        novo_cadastro = {
            "matricula": novo_cliente["matricula"],
            "senha": novo_cliente["senha"],
            "saldo": novo_cliente["saldo"],
            "escolha": novo_cliente["escolha"]
        }

        self.cadastro.append(novo_cadastro)
        self.clientes_conectados[novo_cliente["matricula"]] = cliente
        self.mutex.release()

        cliente.send("Cadastro realizado com sucesso!\n".encode())

        return True

    def autenticar_cliente(self, matricula, senha):
        self.mutex.acquire()
        for cliente in self.cadastro:
            if cliente["matricula"].strip() == matricula.strip() and cliente["senha"].strip() == senha.strip():
                self.mutex.release()
                return True
        self.mutex.release()
        return False

    def obter_saldo(self, matricula):
        self.mutex.acquire()
        for cliente in self.cadastro:
            if cliente["matricula"].strip() == matricula.strip():
                saldo = cliente["saldo"]
                self.mutex.release()
                return saldo
        self.mutex.release()
        return None

    def lidar_pedidos(self, cliente, matricula):
        self.enviar_cardapio(cliente, matricula)
        while True:
            pedido = cliente.recv(1024).decode()
            if pedido == "sair":
                break
            else:
                self.mutex.acquire()
                self.fila_pedidos.put((matricula, pedido))
                self.mutex.release()

    def enviar_cardapio(self, cliente, matricula):
        cardapio = "Cardápio:\n1. Café 1\n2. Cappuccino"
        cliente.send(cardapio.encode())

    def exibir_cadastro(self):
        self.mutex.acquire()
        print("\nLista de Usuários Cadastrados:")
        for cliente in self.cadastro:
            print(cliente)
        self.mutex.release()

if __name__ == "__main__":
    servidor = CantinaServer()
    threading.Thread(target=servidor.iniciar_servidor, args=('localhost', 12345)).start()

    while True:
        comando = input("\nComandos disponíveis: 'lista' para exibir usuários cadastrados, 'sair' para encerrar: ")

        if comando.lower() == 'lista':
            servidor.exibir_cadastro()
        elif comando.lower() == 'sair':
            break
        else:
            print("Comando inválido. Tente novamente.")
