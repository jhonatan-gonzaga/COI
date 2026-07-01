"""Demonstracao do fluxo Cliente-Profissional usando as classes do projeto."""

from models.avaliacao import Avaliacao
from models.cliente import Cliente
from models.endereco import Endereco
from models.especialidade import Especialidade
from models.profissional_autonomo import ProfissionalAutonomo
from models.servico import Servico


cliente = Cliente(
    nome="Maria Oliveira",
    telefone="(92) 99999-1111",
    email="maria@email.com",
    senha="123456",
    id=1,
)

profissional = ProfissionalAutonomo(
    nome="Joao Santos",
    telefone="(92) 98888-2222",
    email="joao@email.com",
    senha="abcdef",
    id=2,
)

especialidade = Especialidade(
    nome="Pedreiro",
    descricao="Servicos de alvenaria, reformas e construcao.",
)
profissional.adicionar_especialidade(especialidade.nome)

endereco = Endereco(
    rua="Rua das Palmeiras",
    numero="120",
    bairro="Centro",
)

servico = Servico(
    id=101,
    descricao="Construir uma parede divisoria e fazer o acabamento.",
    data_prevista="2026-07-05",
    valor=850.00,
    status="AGUARDANDO",
    cliente=cliente,
    profissional=profissional,
    endereco=endereco,
)

print("\n1. Cliente encontra um profissional")
print("-" * 60)
print(cliente)
print(profissional)
print(f"Especialidades: {', '.join(profissional.especialidades)}")

print("\n2. Cliente solicita/contrata o servico")
print("-" * 60)
print(cliente.solicitar_servico(servico.descricao))
print(f"Profissional contratado: {servico.profissional.nome}")
print(f"Endereco: {servico.endereco.formatar()}")
print(f"Data prevista: {servico.data_prevista}")
print(f"Valor combinado: R$ {servico.calcular_valor_final():.2f}")
print(f"Status do servico: {servico.status}")

print("\n3. Profissional aceita o pedido")
print("-" * 60)
servico.alterar_status("EM_ANDAMENTO")
print(f"{profissional.nome} aceitou o servico de {cliente.nome}.")
print(f"Status do servico: {servico.status}")

print("\n4. Servico e executado e concluido")
print("-" * 60)
servico.concluir()
servico.alterar_status("CONCLUIDO")
print(f"Servico finalizado: {servico.descricao}")
print(f"Valor final: R$ {servico.calcular_valor_final():.2f}")
print(f"Status do servico: {servico.status}")

print("\n5. Cliente avalia o profissional")
print("-" * 60)
avaliacao = Avaliacao(
    nota=5,
    comentario="Servico bem feito, dentro do prazo e com otimo acabamento.",
)
dados_avaliacao = cliente.avaliar_servico(
    nota=avaliacao.nota,
    comentario=avaliacao.comentario,
)

print(f"Nota registrada: {avaliacao.nota}/5")
print(f"Comentario: {avaliacao.comentario}")
print(f"Avaliacao valida: {'Sim' if avaliacao.validar_nota() else 'Nao'}")
print(f"Dados retornados pelo cliente: {dados_avaliacao}")

print("\n6. Resumo do fluxo")
print("-" * 60)
print(f"Cliente: {cliente.nome}")
print(f"Profissional: {profissional.nome}")
print(f"Servico: {servico.descricao}")
print(f"Status final: {servico.status}")
