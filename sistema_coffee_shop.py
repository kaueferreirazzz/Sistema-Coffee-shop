"""
Sistema de Gerenciamento - Coffee Shops Tia Rosa
==================================================

Sistema desenvolvido em Python para modernizar a gestão da cafeteria
Coffee Shops Tia Rosa, atendendo às necessidades identificadas na
situação-problema: falta de organização no cadastro de produtos,
ausência de sistema de gestão interno, dificuldade na fidelização de
clientes e baixa familiaridade da equipe com tecnologia.

Funcionalidades:
    - Cadastro, listagem, edição e remoção de produtos
    - Cadastro e listagem de clientes (com pontos de fidelidade)
    - Criação de pedidos, cálculo automático de total e status
    - Aplicação de promoções/cupons de desconto
    - Relatório simples de vendas

Conceitos aplicados: classes, dicionários, listas, funções,
estruturas de controle e interface via linha de comando.
"""

from datetime import datetime


# ---------------------------------------------------------------------------
# CLASSES DO DOMÍNIO
# ---------------------------------------------------------------------------

class Produto:
    """Representa um item do cardápio da cafeteria."""

    def __init__(self, id_produto, nome, categoria, preco, estoque):
        self.id = id_produto
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
        self.estoque = estoque

    def __str__(self):
        return (f"[{self.id:03d}] {self.nome:<20} | {self.categoria:<10} "
                f"| R$ {self.preco:>6.2f} | Estoque: {self.estoque}")


class Cliente:
    """Representa um cliente cadastrado no programa de fidelidade."""

    def __init__(self, id_cliente, nome, telefone, email):
        self.id = id_cliente
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.pontos_fidelidade = 0

    def __str__(self):
        return (f"[{self.id:03d}] {self.nome:<20} | {self.telefone:<15} "
                f"| {self.email:<25} | Pontos: {self.pontos_fidelidade}")


class Pedido:
    """Representa um pedido feito por um cliente."""

    def __init__(self, id_pedido, cliente_id):
        self.id = id_pedido
        self.cliente_id = cliente_id
        self.itens = []          # lista de dicionários: {produto_id, quantidade, preco_unit}
        self.status = "Aberto"
        self.data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.desconto_percentual = 0

    def adicionar_item(self, produto, quantidade):
        self.itens.append({
            "produto_id": produto.id,
            "nome": produto.nome,
            "quantidade": quantidade,
            "preco_unit": produto.preco
        })

    def calcular_subtotal(self):
        return sum(item["quantidade"] * item["preco_unit"] for item in self.itens)

    def calcular_total(self):
        subtotal = self.calcular_subtotal()
        desconto = subtotal * (self.desconto_percentual / 100)
        return subtotal - desconto

    def __str__(self):
        linhas = [f"Pedido #{self.id:03d} | Cliente ID: {self.cliente_id} | "
                  f"Status: {self.status} | Data: {self.data_hora}"]
        for item in self.itens:
            linhas.append(f"    - {item['quantidade']}x {item['nome']} "
                           f"(R$ {item['preco_unit']:.2f} un.)")
        if self.desconto_percentual:
            linhas.append(f"    Desconto aplicado: {self.desconto_percentual}%")
        linhas.append(f"    TOTAL: R$ {self.calcular_total():.2f}")
        return "\n".join(linhas)


# ---------------------------------------------------------------------------
# SISTEMA (regras de negócio)
# ---------------------------------------------------------------------------

class SistemaCoffeeShop:
    """Classe central que concentra o cadastro e as regras de negócio."""

    def __init__(self, nome_loja="Coffee Shops Tia Rosa"):
        self.nome_loja = nome_loja
        self.produtos = {}       # {id: Produto}
        self.clientes = {}       # {id: Cliente}
        self.pedidos = []        # lista de Pedido
        self.promocoes = {}      # {codigo: percentual_desconto}
        self._proximo_id_produto = 1
        self._proximo_id_cliente = 1
        self._proximo_id_pedido = 1

    # ---------------- PRODUTOS ----------------
    def cadastrar_produto(self, nome, categoria, preco, estoque):
        produto = Produto(self._proximo_id_produto, nome, categoria, preco, estoque)
        self.produtos[produto.id] = produto
        self._proximo_id_produto += 1
        return produto

    def listar_produtos(self):
        return list(self.produtos.values())

    def buscar_produto(self, id_produto):
        return self.produtos.get(id_produto)

    def atualizar_estoque(self, id_produto, quantidade):
        produto = self.buscar_produto(id_produto)
        if produto:
            produto.estoque += quantidade
            return True
        return False

    def remover_produto(self, id_produto):
        return self.produtos.pop(id_produto, None) is not None

    # ---------------- CLIENTES ----------------
    def cadastrar_cliente(self, nome, telefone, email):
        cliente = Cliente(self._proximo_id_cliente, nome, telefone, email)
        self.clientes[cliente.id] = cliente
        self._proximo_id_cliente += 1
        return cliente

    def listar_clientes(self):
        return list(self.clientes.values())

    def buscar_cliente(self, id_cliente):
        return self.clientes.get(id_cliente)

    # ---------------- PROMOÇÕES ----------------
    def cadastrar_promocao(self, codigo, percentual_desconto):
        self.promocoes[codigo.upper()] = percentual_desconto

    def listar_promocoes(self):
        return self.promocoes

    # ---------------- PEDIDOS ----------------
    def criar_pedido(self, id_cliente, itens_desejados, codigo_promocao=None):
        """
        itens_desejados: lista de tuplas (id_produto, quantidade)
        Retorna (pedido, erros) -> erros é lista de mensagens (vazia se tudo ok)
        """
        cliente = self.buscar_cliente(id_cliente)
        erros = []
        if not cliente:
            erros.append("Cliente não encontrado.")
            return None, erros

        pedido = Pedido(self._proximo_id_pedido, id_cliente)

        for id_produto, quantidade in itens_desejados:
            produto = self.buscar_produto(id_produto)
            if not produto:
                erros.append(f"Produto ID {id_produto} não encontrado.")
                continue
            if produto.estoque < quantidade:
                erros.append(f"Estoque insuficiente para '{produto.nome}' "
                              f"(disponível: {produto.estoque}).")
                continue
            pedido.adicionar_item(produto, quantidade)
            produto.estoque -= quantidade

        if not pedido.itens:
            erros.append("Nenhum item válido foi adicionado ao pedido.")
            return None, erros

        if codigo_promocao:
            desconto = self.promocoes.get(codigo_promocao.upper())
            if desconto:
                pedido.desconto_percentual = desconto
            else:
                erros.append("Código de promoção inválido (pedido criado sem desconto).")

        pedido.status = "Confirmado"
        self.pedidos.append(pedido)
        self._proximo_id_pedido += 1

        # regra simples de fidelidade: 1 ponto a cada R$10 gastos
        cliente.pontos_fidelidade += int(pedido.calcular_total() // 10)

        return pedido, erros

    def listar_pedidos(self):
        return self.pedidos

    def cancelar_pedido(self, id_pedido):
        for pedido in self.pedidos:
            if pedido.id == id_pedido and pedido.status != "Cancelado":
                # devolve itens ao estoque
                for item in pedido.itens:
                    produto = self.buscar_produto(item["produto_id"])
                    if produto:
                        produto.estoque += item["quantidade"]
                pedido.status = "Cancelado"
                return True
        return False

    # ---------------- RELATÓRIOS ----------------
    def relatorio_vendas(self):
        pedidos_validos = [p for p in self.pedidos if p.status != "Cancelado"]
        total_vendido = sum(p.calcular_total() for p in pedidos_validos)
        qtd_pedidos = len(pedidos_validos)

        contagem_produtos = {}
        for pedido in pedidos_validos:
            for item in pedido.itens:
                contagem_produtos[item["nome"]] = (
                    contagem_produtos.get(item["nome"], 0) + item["quantidade"]
                )

        produto_mais_vendido = None
        if contagem_produtos:
            produto_mais_vendido = max(contagem_produtos, key=contagem_produtos.get)

        return {
            "total_vendido": total_vendido,
            "quantidade_pedidos": qtd_pedidos,
            "produto_mais_vendido": produto_mais_vendido,
            "contagem_produtos": contagem_produtos,
        }


# ---------------------------------------------------------------------------
# DADOS INICIAIS (para não começar o sistema vazio)
# ---------------------------------------------------------------------------

def carregar_dados_iniciais(sistema):
    sistema.cadastrar_produto("Café Expresso", "Bebida", 6.50, 50)
    sistema.cadastrar_produto("Cappuccino", "Bebida", 9.00, 40)
    sistema.cadastrar_produto("Pão de Queijo", "Salgado", 5.00, 30)
    sistema.cadastrar_produto("Bolo de Cenoura", "Doce", 7.50, 20)
    sistema.cadastrar_produto("Croissant", "Salgado", 8.00, 25)

    sistema.cadastrar_cliente("Ana Souza", "(61) 99999-0001", "ana@email.com")
    sistema.cadastrar_cliente("Bruno Lima", "(61) 99999-0002", "bruno@email.com")

    sistema.cadastrar_promocao("TIAROSA10", 10)
    sistema.cadastrar_promocao("FIDELIDADE15", 15)


# ---------------------------------------------------------------------------
# INTERFACE DE LINHA DE COMANDO (MENU)
# ---------------------------------------------------------------------------

def ler_float(mensagem):
    while True:
        try:
            return float(input(mensagem).replace(",", "."))
        except ValueError:
            print(">> Valor inválido. Digite um número (ex: 9.90).")


def ler_int(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print(">> Valor inválido. Digite um número inteiro.")


def menu_produtos(sistema):
    while True:
        print("\n--- MENU PRODUTOS ---")
        print("1. Cadastrar produto")
        print("2. Listar produtos")
        print("3. Atualizar estoque")
        print("4. Remover produto")
        print("0. Voltar")
        opcao = input("Escolha: ")

        if opcao == "1":
            nome = input("Nome do produto: ")
            categoria = input("Categoria (Bebida/Salgado/Doce): ")
            preco = ler_float("Preço (R$): ")
            estoque = ler_int("Estoque inicial: ")
            produto = sistema.cadastrar_produto(nome, categoria, preco, estoque)
            print(f">> Produto cadastrado com sucesso! ID: {produto.id}")

        elif opcao == "2":
            print("\n-- Cardápio atual --")
            for produto in sistema.listar_produtos():
                print(produto)

        elif opcao == "3":
            id_produto = ler_int("ID do produto: ")
            quantidade = ler_int("Quantidade a adicionar (use negativo para remover): ")
            if sistema.atualizar_estoque(id_produto, quantidade):
                print(">> Estoque atualizado com sucesso!")
            else:
                print(">> Produto não encontrado.")

        elif opcao == "4":
            id_produto = ler_int("ID do produto a remover: ")
            if sistema.remover_produto(id_produto):
                print(">> Produto removido.")
            else:
                print(">> Produto não encontrado.")

        elif opcao == "0":
            break
        else:
            print(">> Opção inválida.")


def menu_clientes(sistema):
    while True:
        print("\n--- MENU CLIENTES ---")
        print("1. Cadastrar cliente")
        print("2. Listar clientes")
        print("0. Voltar")
        opcao = input("Escolha: ")

        if opcao == "1":
            nome = input("Nome do cliente: ")
            telefone = input("Telefone: ")
            email = input("E-mail: ")
            cliente = sistema.cadastrar_cliente(nome, telefone, email)
            print(f">> Cliente cadastrado com sucesso! ID: {cliente.id}")

        elif opcao == "2":
            print("\n-- Clientes cadastrados --")
            for cliente in sistema.listar_clientes():
                print(cliente)

        elif opcao == "0":
            break
        else:
            print(">> Opção inválida.")


def menu_pedidos(sistema):
    while True:
        print("\n--- MENU PEDIDOS ---")
        print("1. Criar novo pedido")
        print("2. Listar pedidos")
        print("3. Cancelar pedido")
        print("0. Voltar")
        opcao = input("Escolha: ")

        if opcao == "1":
            id_cliente = ler_int("ID do cliente: ")
            itens = []
            print("Digite os itens do pedido (ID do produto 0 para finalizar):")
            while True:
                id_produto = ler_int("  ID do produto (0 para encerrar): ")
                if id_produto == 0:
                    break
                quantidade = ler_int("  Quantidade: ")
                itens.append((id_produto, quantidade))
            codigo_promocao = input("Código de promoção (ENTER para nenhum): ").strip()
            pedido, erros = sistema.criar_pedido(
                id_cliente, itens, codigo_promocao if codigo_promocao else None
            )
            for erro in erros:
                print(f">> Aviso: {erro}")
            if pedido:
                print("\n>> Pedido criado com sucesso!")
                print(pedido)

        elif opcao == "2":
            print("\n-- Pedidos registrados --")
            for pedido in sistema.listar_pedidos():
                print(pedido)
                print("-" * 40)

        elif opcao == "3":
            id_pedido = ler_int("ID do pedido a cancelar: ")
            if sistema.cancelar_pedido(id_pedido):
                print(">> Pedido cancelado e itens devolvidos ao estoque.")
            else:
                print(">> Pedido não encontrado ou já cancelado.")

        elif opcao == "0":
            break
        else:
            print(">> Opção inválida.")


def menu_relatorios(sistema):
    relatorio = sistema.relatorio_vendas()
    print("\n--- RELATÓRIO DE VENDAS ---")
    print(f"Total vendido: R$ {relatorio['total_vendido']:.2f}")
    print(f"Quantidade de pedidos válidos: {relatorio['quantidade_pedidos']}")
    if relatorio["produto_mais_vendido"]:
        print(f"Produto mais vendido: {relatorio['produto_mais_vendido']}")
    print("\nQuantidade vendida por produto:")
    for nome, qtd in relatorio["contagem_produtos"].items():
        print(f"  - {nome}: {qtd} unidade(s)")


def menu_principal():
    sistema = SistemaCoffeeShop()
    carregar_dados_iniciais(sistema)

    print(f"=== Bem-vindo ao Sistema {sistema.nome_loja} ===")

    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1. Produtos")
        print("2. Clientes")
        print("3. Pedidos")
        print("4. Relatório de vendas")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_produtos(sistema)
        elif opcao == "2":
            menu_clientes(sistema)
        elif opcao == "3":
            menu_pedidos(sistema)
        elif opcao == "4":
            menu_relatorios(sistema)
        elif opcao == "0":
            print("Obrigado por usar o sistema. Até logo!")
            break
        else:
            print(">> Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()
