from dataclasses import dataclass, field

from app.knowledge_base import (
    ARVORE_PERGUNTAS,
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
        estado: set[str] = set()
        for pid, fato in FATOS_INSEGUROS.items():
            if pid in self.respostas:
                if self.respostas[pid] != RESPOSTA_SEGURA_SIM[pid]:
                    estado.add(fato)

        regras = criar_base_de_regras()
        regras_disparadas: list[str] = []
        pontuacao = 0
        recomendacoes: list[str] = []

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

        conclusoes = [f for f in estado if not f.startswith("habito_")]

        falhas = [
            pid
            for pid in self.respostas
            if self.respostas[pid] != RESPOSTA_SEGURA_SIM.get(pid, not self.respostas[pid])
        ]

        if pontuacao <= 15:
            nivel_risco = "baixo"
        elif pontuacao <= 35:
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
