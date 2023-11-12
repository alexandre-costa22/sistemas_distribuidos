class Usuario:
    def __init__(self, matricula, senha, saldo=0):
        self.matricula = matricula
        self.senha = senha
        self.saldo = saldo

class SistemaAutenticacao:
    def __init__(self):
        self.usuarios = []

    def cadastrar_usuario(self, matricula, senha):
        novo_usuario = Usuario(matricula, senha)
        self.usuarios.append(novo_usuario)
        print(f"Usuário cadastrado com matrícula {matricula} e senha {senha}.")

    def autenticar(self, matricula, senha):
        for usuario in self.usuarios:
            if usuario.matricula == matricula and usuario.senha == senha:
                print(f"Autenticação bem-sucedida para o usuário {matricula}.")
                return usuario
        print("Matrícula ou senha incorretas. Autenticação falhou.")
        return None

#teste
if __name__ == "__main__":
    sistema = SistemaAutenticacao()

    sistema.cadastrar_usuario("12345", "senha123")
    sistema.cadastrar_usuario("67890", "outraSenha")

    matricula = input("Digite a matrícula: ")
    senha = input("Digite a senha: ")

    usuario_autenticado = sistema.autenticar(matricula, senha)

    if usuario_autenticado:
        print(f"Saldo atual do usuário {matricula}: {usuario_autenticado.saldo}")
