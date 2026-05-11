from dataclasses import dataclass, field

from app.knowledge_base import (
    PERGUNTAS,
    RESPOSTA_SEGURA_SIM,
    FATOS_INSEGUROS,
    criar_base_de_regras,
)


@dataclass
class ResultadoInferencia:
    pontuacao: int
    nivel_risco: str
    regras_disparadas: list[str] = field(default_factory=list)
    conclusoes_derivadas: list[str] = field(default_factory=list)
    recomendacoes: list[str] = field(default_factory=list)
    falhas_detectadas: list[str] = field(default_factory=list)


class MotorInferencia:
    def __init__(self, respostas: dict[str, bool]):
        self.respostas = respostas

    def executar(self) -> ResultadoInferencia:
        # Inicializa o estado com os fatos derivados das respostas inseguras
        estado: set[str] = set()
        for pid, fato in FATOS_INSEGUROS.items():
            if self.respostas.get(pid) != RESPOSTA_SEGURA_SIM[pid]:
                estado.add(fato)

        regras = criar_base_de_regras()
        regras_disparadas: list[str] = []
        pontuacao = 0
        recomendacoes: list[str] = []

        # Forward chaining — itera até estabilizar
        mudou = True
        while mudou:
            mudou = False
            for regra in regras:
                if regra.nome not in regras_disparadas:
                    if all(p in estado for p in regra.premissas):
                        estado.add(regra.conclusao)
                        regras_disparadas.append(regra.nome)
                        pontuacao += regra.pontuacao
                        recomendacoes.append(regra.recomendacao)
                        mudou = True

        # Fatos derivados pelo motor (exclui hábitos iniciais)
        conclusoes = [f for f in estado if not f.startswith("habito_")]

        # IDs de perguntas com resposta insegura
        falhas = [
            p["id"]
            for p in PERGUNTAS
            if self.respostas.get(p["id"]) != RESPOSTA_SEGURA_SIM[p["id"]]
        ]

        if pontuacao <= 42:
            nivel_risco = "baixo"
        elif pontuacao <= 85:
            nivel_risco = "medio"
        else:
            nivel_risco = "alto"

        return ResultadoInferencia(
            pontuacao=pontuacao,
            nivel_risco=nivel_risco,
            regras_disparadas=regras_disparadas,
            conclusoes_derivadas=conclusoes,
            recomendacoes=recomendacoes,
            falhas_detectadas=falhas,
        )