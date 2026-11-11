import json
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["campusflow_a12"]
solicitacoes = db["solicitacoes"]

def missao_1_fila_critica():
    """
    Missão 1: Localiza solicitações ABERTA ou EM_ANALISE com prioridade >= 4.
    Projeção: protocolo, estudante.nome, categoria.nome, situacao, prioridade.
    Ordenação: prioridade DESC, criadoEm ASC.
    """
    filtro = {
        "situacao": {"$in": ["ABERTA", "EM_ANALISE"]},
        "prioridade": {"$gte": 4}
    }
    projecao = {
        "_id": 0,
        "protocolo": 1,
        "estudante.nome": 1,
        "categoria.nome": 1,
        "situacao": 1,
        "prioridade": 1
    }
    ordenacao = [("prioridade", -1), ("criadoEm", 1)]
    
    cursor = solicitacoes.find(filtro, projecao).sort(ordenacao)
    return list(cursor)


def missao_2_backlog_categoria():
    """
    Missão 2: Agrupa solicitações não concluídas por categoria.
    Pipeline: $match, $group, $sort.
    """
    pipeline = [
        {"$match": {"situacao": {"$ne": "CONCLUIDA"}}},
        {
            "$group": {
                "_id": "$categoria.nome",
                "quantidade": {"$sum": 1}
            }
        },
        {"$sort": {"quantidade": -1}}
    ]
    return list(solicitacoes.aggregate(pipeline))


def missao_3_carga_setor():
    """
    Missão 3: Desconstrói o array de atendimentos e calcula estatísticas por setor.
    Pipeline: $unwind, $group, $sort.
    """
    pipeline = [
        {"$unwind": "$atendimentos"},
        {
            "$group": {
                "_id": "$atendimentos.setor",
                "interacoes": {"$sum": 1},
                "tempoMedio": {"$avg": "$atendimentos.duracaoMin"},
                "maiorDuracao": {"$max": "$atendimentos.duracaoMin"}
            }
        },
        {"$sort": {"interacoes": -1}}
    ]
    return list(solicitacoes.aggregate(pipeline))


def missao_4_estudantes_recorrentes():
    """
    Missão 4: Identifica estudantes com mais de uma solicitação cadastrada.
    Pipeline: $group, $match, $sort.
    """
    pipeline = [
        {
            "$group": {
                "_id": "$estudante.id",
                "nome": {"$first": "$estudante.nome"},
                "quantidade": {"$sum": 1},
                "protocolos": {"$push": "$protocolo"}
            }
        },
        {"$match": {"quantidade": {"$gt": 1}}},
        {"$sort": {"quantidade": -1}}
    ]
    return list(solicitacoes.aggregate(pipeline))


if __name__ == "__main__":
    print("=== MISSÃO 1: FILA CRÍTICA ===")
    print(json.dumps(missao_1_fila_critica(), indent=4, ensure_ascii=False))

    print("\n=== MISSÃO 2: BACKLOG POR CATEGORIA ===")
    print(json.dumps(missao_2_backlog_categoria(), indent=4, ensure_ascii=False))

    print("\n=== MISSÃO 3: CARGA POR SETOR ===")
    print(json.dumps(missao_3_carga_setor(), indent=4, ensure_ascii=False))

    print("\n=== MISSÃO 4: ESTUDANTES RECORRENTES ===")
    print(json.dumps(missao_4_estudantes_recorrentes(), indent=4, ensure_ascii=False))