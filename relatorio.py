from consultas import (
    missao_1_fila_critica,
    missao_2_backlog_categoria,
    missao_3_carga_setor,
    missao_4_estudantes_recorrentes
)

def gerar_relatorio():
    res_m1 = missao_1_fila_critica()
    res_m2 = missao_2_backlog_categoria()
    res_m3 = missao_3_carga_setor()
    res_m4 = missao_4_estudantes_recorrentes()

    print("========================================")
    print("CAMPUSFLOW — RELATÓRIO OPERACIONAL")
    print("========================================\n")

    print("BACKLOG POR CATEGORIA")
    for item in res_m2:
        print(f"{item['_id']}: {item['quantidade']}")
    print()

    print("CARGA POR SETOR")
    for item in res_m3:
        print(f"{item['_id']}")
        print(f"  Interações: {item['interacoes']}")
        print(f"  Tempo médio: {item['tempoMedio']:.1f} min (Maior duração: {item['maiorDuracao']} min)")
    print()

    print("ESTUDANTES RECORRENTES")
    for item in res_m4:
        protocolos_str = ", ".join(item['protocolos'])
        print(f"{item['nome']} (ID {item['_id']}): {item['quantidade']} solicitações [{protocolos_str}]")
    print()

    print("CASOS CRÍTICOS")
    for item in res_m1:
        nome_aluno = item['estudante']['nome']
        cat_nome = item['categoria']['nome']
        print(f"{item['protocolo']} | {nome_aluno} | {cat_nome} | Prioridade {item['prioridade']} | Status: {item['situacao']}")
    print("\n========================================\n")

    print("CONCLUSÕES TÉCNICAS")
    print("1. A categoria 'Aproveitamento de Disciplina' lidera o backlog acumulado com 3 solicitações pendentes (37.5% de todo o backlog da central).")
    print("2. A afirmação de que 'o problema é a Secretaria' é FALSA: embora receba mais interações (10 atendimentos), seu tempo médio é de apenas 9.7 min. O verdadeiro gargalo de tempo está na Coordenação, que possui um tempo médio de atendimento 4.8x maior (47.0 min) e a maior duração individual registrada (55 min).")
    print("3. Existe concentração de solicitações em poucos estudantes: Ana Ribeiro (3 solicitações) e Bruno Lima (2 solicitações) concentram juntos 41.7% (5 de 12) de todo o volume atendido pelo sistema.")
    print("========================================")

if __name__ == "__main__":
    gerar_relatorio()