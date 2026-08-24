# Coffee Shops Tia Rosa — Sistema de Gerenciamento em Python

Sistema desenvolvido em Python para modernizar a gestão da cafeteria **Coffee Shops Tia Rosa**, atendendo às necessidades identificadas na situação-problema da atividade: falta de organização no cadastro de produtos, ausência de sistema de gestão interno, dificuldade na fidelização de clientes e baixa familiaridade da equipe com tecnologia.

## Objetivo

Desenvolver uma solução em Python que simule funcionalidades de um sistema de gerenciamento/atendimento para a cafeteria, como cadastro de produtos, pedidos e clientes.

## Funcionalidades

- **Produtos**: cadastro, listagem, atualização de estoque e remoção de itens do cardápio.
- **Clientes**: cadastro, listagem e pontuação automática em programa de fidelidade (1 ponto a cada R$10 gastos).
- **Pedidos**: criação com múltiplos itens, verificação automática de estoque, cálculo de total, aplicação de cupons de desconto e cancelamento (com devolução ao estoque).
- **Relatórios**: total vendido, quantidade de pedidos e produto mais vendido.

## Conceitos aplicados

Classes, dicionários, listas, funções, estruturas de repetição e condicionais, tratamento de erros (`try/except`).

## Como executar

Pré-requisito: Python 3 instalado.

```bash
python sistema_coffee_shop.py
```

O sistema abre um menu interativo no terminal — basta seguir as opções numeradas.

## 📁 Estrutura do código

| Componente | Descrição |
|---|---|
| `Produto` | Classe que representa um item do cardápio (id, nome, categoria, preço, estoque) |
| `Cliente` | Classe que representa um cliente cadastrado (id, nome, telefone, e-mail, pontos) |
| `Pedido` | Classe que representa um pedido (itens, status, data, desconto) |
| `SistemaCoffeeShop` | Classe central com as regras de negócio (cadastro, busca, criação de pedidos, relatórios) |
| Funções de menu | Interface de linha de comando para interação com o usuário |

## 📄 Relatório

A explicação completa do código, prints da execução e conclusões estão no arquivo `Relatorio_Coffee_Shops_Tia_Rosa.docx` deste repositório.
