from dataclasses import dataclass

PERGUNTAS = [
    {"id": "reutiliza_senha",         "texto": "Você usa a mesma senha em múltiplos serviços ou contas?"},
    {"id": "usa_2fa",                  "texto": "Você utiliza autenticação em dois fatores (2FA) nas suas contas importantes?"},
    {"id": "atualiza_software",        "texto": "Você mantém seus aplicativos e sistema operacional sempre atualizados?"},
    {"id": "clica_links_suspeitos",    "texto": "Você clica em links recebidos por e-mail ou mensagem sem verificar a origem?"},
    {"id": "usa_wifi_publico",         "texto": "Você acessa serviços bancários ou dados sensíveis em redes Wi-Fi públicas?"},
    {"id": "compartilha_dados",        "texto": "Você preenche formulários online sem verificar se o site possui HTTPS?"},
    {"id": "tem_antivirus",            "texto": "Você possui antivírus instalado e atualizado no seu dispositivo principal?"},
    {"id": "faz_backup",               "texto": "Você realiza backups regulares dos seus dados importantes?"},
    {"id": "senha_fraca",              "texto": "Você usa senhas simples como datas de nascimento, nomes ou sequências numéricas?"},
    {"id": "baixa_apps_desconhecidos", "texto": "Você instala aplicativos de fontes desconhecidas ou fora das lojas oficiais?"},
]

# Resposta que representa o hábito SEGURO para cada pergunta
RESPOSTA_SEGURA_SIM: dict[str, bool] = {
    "reutiliza_senha":         False,
    "usa_2fa":                  True,
    "atualiza_software":        True,
    "clica_links_suspeitos":   False,
    "usa_wifi_publico":        False,
    "compartilha_dados":       False,
    "tem_antivirus":            True,
    "faz_backup":               True,
    "senha_fraca":             False,
    "baixa_apps_desconhecidos": False,
}

# Fato inicial adicionado ao estado quando a resposta é insegura
FATOS_INSEGUROS: dict[str, str] = {
    "reutiliza_senha":         "habito_reutiliza_senha",
    "usa_2fa":                  "habito_sem_2fa",
    "atualiza_software":        "habito_sem_atualizacoes",
    "clica_links_suspeitos":   "habito_clica_links",
    "usa_wifi_publico":        "habito_wifi_publico",
    "compartilha_dados":       "habito_dados_sem_https",
    "tem_antivirus":            "habito_sem_antivirus",
    "faz_backup":               "habito_sem_backup",
    "senha_fraca":             "habito_senha_fraca",
    "baixa_apps_desconhecidos": "habito_apps_desconhecidos",
}


@dataclass
class Regra:
    nome: str
    premissas: list[str]
    conclusao: str
    pontuacao: int
    recomendacao: str
    descricao: str


def criar_base_de_regras() -> list[Regra]:
    """
    13 regras SE…ENTÃO.
    R01–R10: nível 1 — disparadas diretamente pelos hábitos inseguros.
    R11–R13: nível 2 — compostas, dependem de conclusões de R01–R10.

    Pontuação máxima possível: 128 pts (todos os hábitos inseguros).
      Nível 1 total : 78 pts
      Nível 2 total : 50 pts (R11=20, R12=16, R13=14)
    """
    return [
        Regra(
            nome="R01",
            premissas=["habito_reutiliza_senha"],
            conclusao="risco_credenciais",
            pontuacao=8,
            recomendacao="Use senhas únicas para cada serviço. Considere um gerenciador de senhas.",
            descricao="Reutilização de senhas em múltiplos serviços",
        ),
        Regra(
            nome="R02",
            premissas=["habito_sem_2fa"],
            conclusao="risco_sem_autenticacao_dupla",
            pontuacao=8,
            recomendacao="Ative a autenticação em dois fatores (2FA) em todas as contas que oferecem esse recurso.",
            descricao="Ausência de autenticação em dois fatores",
        ),
        Regra(
            nome="R03",
            premissas=["habito_sem_atualizacoes"],
            conclusao="risco_vulnerabilidades_conhecidas",
            pontuacao=6,
            recomendacao="Mantenha seu sistema operacional e aplicativos atualizados para corrigir falhas de segurança.",
            descricao="Software desatualizado com vulnerabilidades conhecidas",
        ),
        Regra(
            nome="R04",
            premissas=["habito_clica_links"],
            conclusao="risco_phishing",
            pontuacao=10,
            recomendacao="Nunca clique em links suspeitos. Verifique o remetente e acesse sites diretamente pelo navegador.",
            descricao="Comportamento de risco a ataques de phishing",
        ),
        Regra(
            nome="R05",
            premissas=["habito_wifi_publico"],
            conclusao="risco_interceptacao",
            pontuacao=8,
            recomendacao="Evite acessar dados sensíveis em redes Wi-Fi públicas. Use uma VPN quando necessário.",
            descricao="Acesso a dados sensíveis em redes públicas não seguras",
        ),
        Regra(
            nome="R06",
            premissas=["habito_dados_sem_https"],
            conclusao="risco_dados_expostos",
            pontuacao=8,
            recomendacao="Sempre verifique se o site possui HTTPS antes de inserir dados pessoais ou financeiros.",
            descricao="Envio de dados em sites sem criptografia HTTPS",
        ),
        Regra(
            nome="R07",
            premissas=["habito_sem_antivirus"],
            conclusao="risco_sem_protecao",
            pontuacao=6,
            recomendacao="Instale e mantenha atualizado um antivírus confiável no seu dispositivo.",
            descricao="Dispositivo sem proteção antivírus ativa",
        ),
        Regra(
            nome="R08",
            premissas=["habito_sem_backup"],
            conclusao="risco_perda_dados",
            pontuacao=6,
            recomendacao="Realize backups periódicos dos seus dados em local seguro (nuvem ou disco externo).",
            descricao="Ausência de backups regulares de dados importantes",
        ),
        Regra(
            nome="R09",
            premissas=["habito_senha_fraca"],
            conclusao="risco_senha_vulneravel",
            pontuacao=10,
            recomendacao="Crie senhas fortes com pelo menos 12 caracteres, combinando letras, números e símbolos.",
            descricao="Uso de senhas fracas ou previsíveis",
        ),
        Regra(
            nome="R10",
            premissas=["habito_apps_desconhecidos"],
            conclusao="risco_malware",
            pontuacao=8,
            recomendacao="Instale aplicativos apenas de lojas oficiais (App Store, Google Play) e fontes confiáveis.",
            descricao="Instalação de aplicativos de fontes não verificadas",
        ),
        # Regras compostas de Nível 2
        Regra(
            nome="R11",
            premissas=["risco_credenciais", "risco_senha_vulneravel"],
            conclusao="risco_conta_comprometida",
            pontuacao=20,
            recomendacao=(
                "Seu perfil indica alto risco de comprometimento de contas. "
                "Altere todas as senhas imediatamente e ative 2FA."
            ),
            descricao="Combinação crítica: senhas reutilizadas e fracas — alto risco de invasão de contas",
        ),
        Regra(
            nome="R12",
            premissas=["risco_phishing", "risco_dados_expostos"],
            conclusao="risco_engenharia_social",
            pontuacao=16,
            recomendacao=(
                "Você está vulnerável a engenharia social. "
                "Desconfie de mensagens urgentes pedindo dados pessoais ou financeiros."
            ),
            descricao="Combinação crítica: suscetibilidade a phishing e exposição de dados pessoais",
        ),
        Regra(
            nome="R13",
            premissas=["risco_interceptacao", "risco_sem_protecao"],
            conclusao="risco_dispositivo_comprometido",
            pontuacao=14,
            recomendacao=(
                "Seu dispositivo está exposto a interceptação de dados. "
                "Instale proteção e evite redes públicas para acessos sensíveis."
            ),
            descricao="Combinação crítica: uso de redes inseguras sem proteção antivírus",
        ),
    ]