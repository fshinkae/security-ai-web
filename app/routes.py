from datetime import datetime, timezone

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for

from app.database import get_client
from app.inference import MotorInferencia
from app.knowledge_base import PERGUNTAS, RESPOSTA_SEGURA_SIM

bp = Blueprint("bp", __name__)

IDS_PERGUNTAS = [p["id"] for p in PERGUNTAS]
PERGUNTAS_MAP = {p["id"]: p["texto"] for p in PERGUNTAS}

_LABELS_RISCO = {"baixo": "Baixo Risco", "medio": "Risco Médio", "alto": "Alto Risco"}
_PAGINA_SIZE = 10


def _converter_form(form) -> dict[str, bool]:
    return {pid: form.get(f"pergunta_{pid}") == "sim" for pid in IDS_PERGUNTAS}


@bp.get("/")
def index():
    return render_template("index.html", perguntas=PERGUNTAS)


@bp.post("/diagnostico")
def diagnostico():
    respostas = _converter_form(request.form)

    # Valida que todas as 10 respostas foram enviadas
    faltando = [pid for pid in IDS_PERGUNTAS if f"pergunta_{pid}" not in request.form]
    if faltando:
        flash("Por favor, responda todas as perguntas antes de continuar.", "erro")
        return redirect(url_for("bp.index"))

    resultado = MotorInferencia(respostas).executar()

    # Deduplica recomendações mantendo ordem
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

    return render_template("resultado.html", diagnostico=diag, perguntas_map=PERGUNTAS_MAP)


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
