from datetime import datetime, timezone

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for

from app.database import get_client
from app.inference import MotorInferencia
from app.knowledge_base import ARVORE_PERGUNTAS, QUESTAO_INICIAL, RESPOSTA_SEGURA_SIM, get_perguntas_map

bp = Blueprint("bp", __name__)

PERGUNTAS_MAP = get_perguntas_map()
_LABELS_RISCO = {"baixo": "Baixo Risco", "medio": "Risco Médio", "alto": "Alto Risco"}
_PAGINA_SIZE = 10

# Níveis da árvore para o grafo piramidal (ordem de exibição top→bottom)
_NIVEIS_ARVORE: list[list[str]] = [
    ["reutiliza_senha"],
    ["senha_fraca", "usa_gerenciador"],
    ["usa_2fa", "bloqueio_tela", "usa_2fa_app", "troca_senha_regularmente"],
    ["atualiza_software", "tem_antivirus", "baixa_apps_desconhecidos",
     "clica_links_suspeitos", "verifica_permissoes", "compartilha_dados",
     "usa_wifi_publico", "faz_backup"],
    ["usa_vpn", "criptografia_disco", "monitoramento_conta", "download_pirata",
     "verifica_desenvolvedor", "compartilha_dispositivo", "usa_filtro_email",
     "reconhece_phishing", "dados_nuvem", "revoga_acessos", "verifica_certificado_ssl",
     "usa_pagamento_seguro", "desconecta_wifi", "usa_vpn_privacidade",
     "testa_backup", "senhas_navegador"],
]


def _computar_tree_data(respostas: dict) -> dict:
    visited_nodes: dict[str, bool] = {}
    visited_edges: list[list[str]] = []
    atual = QUESTAO_INICIAL
    while atual and atual in ARVORE_PERGUNTAS:
        no = ARVORE_PERGUNTAS[atual]
        if atual not in respostas:
            break
        resp = bool(respostas[atual])
        visited_nodes[atual] = resp
        proximo = no.proxima_sim if resp else no.proxima_nao
        if proximo:
            visited_edges.append([atual, proximo])
        atual = proximo

    nodes = {}
    for nid, no in ARVORE_PERGUNTAS.items():
        visitado = nid in visited_nodes
        resp = visited_nodes.get(nid)
        nodes[nid] = {
            "texto": no.texto,
            "grupo": no.grupo,
            "visitado": visitado,
            "resposta": resp,
            "seguro": (resp == RESPOSTA_SEGURA_SIM[nid]) if visitado else None,
        }

    return {"nodes": nodes, "visited_edges": visited_edges}


def _converter_form(form) -> dict[str, bool]:
    ids_visitados = [
        pid.strip()
        for pid in form.get("perguntas_respondidas", "").split(",")
        if pid.strip()
    ]
    return {pid: form.get(f"pergunta_{pid}") == "sim" for pid in ids_visitados}


@bp.get("/")
def index():
    return render_template(
        "index.html",
        arvore=ARVORE_PERGUNTAS,
        questao_inicial=QUESTAO_INICIAL,
    )


@bp.post("/diagnostico")
def diagnostico():
    ids_visitados = [
        pid.strip()
        for pid in request.form.get("perguntas_respondidas", "").split(",")
        if pid.strip()
    ]
    faltando = [pid for pid in ids_visitados if f"pergunta_{pid}" not in request.form]
    if not ids_visitados or faltando:
        flash("Por favor, responda todas as perguntas antes de continuar.", "erro")
        return redirect(url_for("bp.index"))

    respostas = _converter_form(request.form)
    resultado = MotorInferencia(respostas).executar()

    vistas: set[str] = set()
    recomendacoes_unicas = []
    for r in resultado.recomendacoes:
        if r not in vistas:
            vistas.add(r)
            recomendacoes_unicas.append(r)

    row = {
        "nome": request.form.get("nome") or None,
        "respostas": respostas,
        "pontuacao": resultado.pontuacao,
        "nivel_risco": resultado.nivel_risco,
        "regras_disparadas": resultado.regras_disparadas,
        "conclusoes_derivadas": resultado.conclusoes_derivadas,
        "recomendacoes": recomendacoes_unicas,
        "falhas_detectadas": resultado.falhas_detectadas,
        "criado_em": datetime.now(timezone.utc).isoformat(),
    }

    try:
        resp = get_client().table("diagnosticos").insert(row).execute()
        diagnostico_id = resp.data[0]["id"]
    except Exception as exc:
        return render_template("erro.html", mensagem=str(exc), codigo=500), 500

    return redirect(url_for("bp.resultado", diagnostico_id=diagnostico_id))


@bp.get("/resultado/<uuid:diagnostico_id>")
def resultado(diagnostico_id):
    try:
        resp = (
            get_client()
            .table("diagnosticos")
            .select("*")
            .eq("id", str(diagnostico_id))
            .maybe_single()
            .execute()
        )
    except Exception as exc:
        return render_template("erro.html", mensagem=str(exc), codigo=500), 500

    if not resp.data:
        return render_template("erro.html", mensagem="Diagnóstico não encontrado.", codigo=404), 404

    diag = resp.data
    diag["label_risco"] = _LABELS_RISCO.get(diag["nivel_risco"], diag["nivel_risco"])

    respostas = diag.get("respostas", {})
    tree_data = _computar_tree_data(respostas)

    return render_template(
        "resultado.html",
        diagnostico=diag,
        perguntas_map=PERGUNTAS_MAP,
        tree_data=tree_data,
    )


@bp.get("/historico")
def historico():
    pagina = max(1, request.args.get("pagina", 1, type=int))
    nivel = request.args.get("nivel", "")

    skip = (pagina - 1) * _PAGINA_SIZE
    fim = skip + _PAGINA_SIZE - 1

    try:
        query = get_client().table("diagnosticos").select("id, nome, pontuacao, nivel_risco, criado_em")
        if nivel in ("baixo", "medio", "alto"):
            query = query.eq("nivel_risco", nivel)
        resp = query.order("criado_em", desc=True).range(skip, fim).execute()
    except Exception as exc:
        return render_template("erro.html", mensagem=str(exc), codigo=500), 500

    return render_template(
        "historico.html",
        diagnosticos=resp.data,
        pagina=pagina,
        nivel=nivel,
        tem_proxima=len(resp.data) == _PAGINA_SIZE,
    )


@bp.get("/health")
def health():
    return jsonify({"status": "ok"})
