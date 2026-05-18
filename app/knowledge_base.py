from dataclasses import dataclass


@dataclass
class QuestionNode:
    id: str
    grupo: str
    texto: str
    resposta_segura: bool
    fato_inseguro: str
    proxima_sim: str | None
    proxima_nao: str | None


# Árvore binária pura — sem convergências, 5 níveis, 31 nós:
#
#                          reutiliza_senha
#                         /               \
#                   senha_fraca       usa_gerenciador
#                   /       \           /           \
#               usa_2fa  bloqueio   usa_2fa_app  troca_senha
#               /   \     /   \      /    \        /     \
#           atualiz antiv baixa clica verif comp  wifi  backup
#           /  \   / \   / \   / \   / \   / \   / \   / \
#         vpn cript mon pir dev comp fil rec nuvem rev ssl pag des vpnp test sens
#
ARVORE_PERGUNTAS: dict[str, QuestionNode] = {
    n.id: n for n in [
        # ── NÍVEL 0 — raiz ────────────────────────────────────────────────────
        QuestionNode(
            id="reutiliza_senha",
            grupo="Senhas",
            texto="Você usa a mesma senha em múltiplos serviços ou contas?",
            resposta_segura=False,
            fato_inseguro="habito_reutiliza_senha",
            proxima_sim="senha_fraca",
            proxima_nao="usa_gerenciador",
        ),
        # ── NÍVEL 1 ───────────────────────────────────────────────────────────
        QuestionNode(
            id="senha_fraca",
            grupo="Senhas",
            texto="Essas senhas contêm dados pessoais como nome ou data de nascimento?",
            resposta_segura=False,
            fato_inseguro="habito_senha_fraca",
            proxima_sim="usa_2fa",
            proxima_nao="bloqueio_tela",
        ),
        QuestionNode(
            id="usa_gerenciador",
            grupo="Senhas",
            texto="Você usa um gerenciador de senhas para criar e armazenar senhas únicas?",
            resposta_segura=True,
            fato_inseguro="habito_sem_gerenciador",
            proxima_sim="usa_2fa_app",
            proxima_nao="troca_senha_regularmente",
        ),
        # ── NÍVEL 2 ───────────────────────────────────────────────────────────
        QuestionNode(
            id="usa_2fa",
            grupo="Autenticação",
            texto="Você utiliza autenticação em dois fatores (2FA) nas suas contas importantes?",
            resposta_segura=True,
            fato_inseguro="habito_sem_2fa",
            proxima_sim="atualiza_software",
            proxima_nao="tem_antivirus",
        ),
        QuestionNode(
            id="bloqueio_tela",
            grupo="Dispositivo",
            texto="Seu dispositivo principal tem senha, PIN ou biometria de bloqueio de tela ativado?",
            resposta_segura=True,
            fato_inseguro="habito_sem_bloqueio_tela",
            proxima_sim="baixa_apps_desconhecidos",
            proxima_nao="clica_links_suspeitos",
        ),
        QuestionNode(
            id="usa_2fa_app",
            grupo="Autenticação",
            texto="Seu 2FA usa aplicativo autenticador (Google Authenticator, Authy) em vez de apenas SMS?",
            resposta_segura=True,
            fato_inseguro="habito_2fa_sms",
            proxima_sim="verifica_permissoes",
            proxima_nao="compartilha_dados",
        ),
        QuestionNode(
            id="troca_senha_regularmente",
            grupo="Senhas",
            texto="Você troca suas senhas regularmente (a cada 3 a 6 meses)?",
            resposta_segura=True,
            fato_inseguro="habito_troca_irregular",
            proxima_sim="usa_wifi_publico",
            proxima_nao="faz_backup",
        ),
        # ── NÍVEL 3 ───────────────────────────────────────────────────────────
        QuestionNode(
            id="atualiza_software",
            grupo="Dispositivo",
            texto="Você mantém seus aplicativos e sistema operacional sempre atualizados?",
            resposta_segura=True,
            fato_inseguro="habito_sem_atualizacoes",
            proxima_sim="usa_vpn",
            proxima_nao="criptografia_disco",
        ),
        QuestionNode(
            id="tem_antivirus",
            grupo="Dispositivo",
            texto="Você possui antivírus instalado e atualizado no seu dispositivo principal?",
            resposta_segura=True,
            fato_inseguro="habito_sem_antivirus",
            proxima_sim="monitoramento_conta",
            proxima_nao="download_pirata",
        ),
        QuestionNode(
            id="baixa_apps_desconhecidos",
            grupo="Dispositivo",
            texto="Você instala aplicativos de fontes desconhecidas ou fora das lojas oficiais?",
            resposta_segura=False,
            fato_inseguro="habito_apps_desconhecidos",
            proxima_sim="verifica_desenvolvedor",
            proxima_nao="compartilha_dispositivo",
        ),
        QuestionNode(
            id="clica_links_suspeitos",
            grupo="Comportamento Online",
            texto="Você clica em links recebidos por e-mail ou mensagem sem verificar a origem?",
            resposta_segura=False,
            fato_inseguro="habito_clica_links",
            proxima_sim="usa_filtro_email",
            proxima_nao="reconhece_phishing",
        ),
        QuestionNode(
            id="verifica_permissoes",
            grupo="Dispositivo",
            texto="Antes de instalar um aplicativo, você verifica as permissões que ele solicita?",
            resposta_segura=True,
            fato_inseguro="habito_nao_verifica_permissoes",
            proxima_sim="dados_nuvem",
            proxima_nao="revoga_acessos",
        ),
        QuestionNode(
            id="compartilha_dados",
            grupo="Comportamento Online",
            texto="Você preenche formulários online sem verificar se o site possui HTTPS?",
            resposta_segura=False,
            fato_inseguro="habito_dados_sem_https",
            proxima_sim="verifica_certificado_ssl",
            proxima_nao="usa_pagamento_seguro",
        ),
        QuestionNode(
            id="usa_wifi_publico",
            grupo="Rede",
            texto="Você acessa serviços bancários ou dados sensíveis em redes Wi-Fi públicas?",
            resposta_segura=False,
            fato_inseguro="habito_wifi_publico",
            proxima_sim="desconecta_wifi",
            proxima_nao="usa_vpn_privacidade",
        ),
        QuestionNode(
            id="faz_backup",
            grupo="Dados",
            texto="Você realiza backups regulares dos seus dados importantes?",
            resposta_segura=True,
            fato_inseguro="habito_sem_backup",
            proxima_sim="testa_backup",
            proxima_nao="senhas_navegador",
        ),
        # ── NÍVEL 4 — folhas ─────────────────────────────────────────────────
        QuestionNode(
            id="usa_vpn",
            grupo="Rede",
            texto="Você usa VPN ao acessar redes não confiáveis ou para proteger sua privacidade?",
            resposta_segura=True,
            fato_inseguro="habito_sem_vpn",
            proxima_sim=None,
            proxima_nao=None,
        ),
        QuestionNode(
            id="criptografia_disco",
            grupo="Dispositivo",
            texto="Seu dispositivo principal possui criptografia de disco habilitada (BitLocker, FileVault)?",
            resposta_segura=True,
            fato_inseguro="habito_sem_criptografia",
            proxima_sim=None,
            proxima_nao=None,
        ),
        QuestionNode(
            id="monitoramento_conta",
            grupo="Comportamento Online",
            texto="Você verifica periodicamente acessos suspeitos e atividades incomuns nas suas contas?",
            resposta_segura=True,
            fato_inseguro="habito_sem_monitoramento",
            proxima_sim=None,
            proxima_nao=None,
        ),
        QuestionNode(
            id="download_pirata",
            grupo="Dispositivo",
            texto="Você baixa softwares, filmes ou músicas de sites piratas ou redes de torrent?",
            resposta_segura=False,
            fato_inseguro="habito_pirataria",
            proxima_sim=None,
            proxima_nao=None,
        ),
        QuestionNode(
            id="verifica_desenvolvedor",
            grupo="Dispositivo",
            texto="Você pesquisa a reputação do desenvolvedor antes de instalar aplicativos de fontes externas?",
            resposta_segura=True,
            fato_inseguro="habito_nao_verifica_dev",
            proxima_sim=None,
            proxima_nao=None,
        ),
        QuestionNode(
            id="compartilha_dispositivo",
            grupo="Dispositivo",
            texto="Você compartilha seu dispositivo principal com outras pessoas sem perfis ou restrições de acesso?",
            resposta_segura=False,
            fato_inseguro="habito_compartilha_dispositivo",
            proxima_sim=None,
            proxima_nao=None,
        ),
        QuestionNode(
            id="usa_filtro_email",
            grupo="Comportamento Online",
            texto="Você utiliza filtros de spam ou soluções de segurança configuradas no seu e-mail?",
            resposta_segura=True,
            fato_inseguro="habito_sem_filtro_email",
            proxima_sim=None,
            proxima_nao=None,
        ),
        QuestionNode(
            id="reconhece_phishing",
            grupo="Comportamento Online",
            texto="Você consegue identificar sinais de phishing, como domínios falsos ou solicitações urgentes?",
            resposta_segura=True,
            fato_inseguro="habito_nao_reconhece_phishing",
            proxima_sim=None,
            proxima_nao=None,
        ),
        QuestionNode(
            id="dados_nuvem",
            grupo="Dados",
            texto="Seus arquivos na nuvem (Google Drive, Dropbox) estão protegidos com senhas fortes e 2FA?",
            resposta_segura=True,
            fato_inseguro="habito_nuvem_insegura",
            proxima_sim=None,
            proxima_nao=None,
        ),
        QuestionNode(
            id="revoga_acessos",
            grupo="Comportamento Online",
            texto="Você periodicamente revisa e revoga acessos de aplicativos antigos às suas contas?",
            resposta_segura=True,
            fato_inseguro="habito_nao_revoga_acessos",
            proxima_sim=None,
            proxima_nao=None,
        ),
        QuestionNode(
            id="verifica_certificado_ssl",
            grupo="Comportamento Online",
            texto="Você sabe como identificar um certificado SSL inválido ou um site fraudulento?",
            resposta_segura=True,
            fato_inseguro="habito_ignora_ssl",
            proxima_sim=None,
            proxima_nao=None,
        ),
        QuestionNode(
            id="usa_pagamento_seguro",
            grupo="Dados",
            texto="Para compras online, você utiliza cartão virtual, PayPal ou outros métodos de pagamento seguros?",
            resposta_segura=True,
            fato_inseguro="habito_pagamento_inseguro",
            proxima_sim=None,
            proxima_nao=None,
        ),
        QuestionNode(
            id="desconecta_wifi",
            grupo="Rede",
            texto="Após usar uma rede Wi-Fi pública, você desconecta manualmente e remove a rede salva?",
            resposta_segura=True,
            fato_inseguro="habito_nao_desconecta_wifi",
            proxima_sim=None,
            proxima_nao=None,
        ),
        QuestionNode(
            id="usa_vpn_privacidade",
            grupo="Rede",
            texto="Você utiliza VPN para proteger sua privacidade ao navegar na internet?",
            resposta_segura=True,
            fato_inseguro="habito_sem_vpn_privacidade",
            proxima_sim=None,
            proxima_nao=None,
        ),
        QuestionNode(
            id="testa_backup",
            grupo="Dados",
            texto="Você testa periodicamente se seus backups podem ser restaurados com sucesso?",
            resposta_segura=True,
            fato_inseguro="habito_nao_testa_backup",
            proxima_sim=None,
            proxima_nao=None,
        ),
        QuestionNode(
            id="senhas_navegador",
            grupo="Senhas",
            texto="Você salva senhas diretamente no navegador sem usar um gerenciador de senhas dedicado?",
            resposta_segura=False,
            fato_inseguro="habito_senhas_no_navegador",
            proxima_sim=None,
            proxima_nao=None,
        ),
    ]
}

QUESTAO_INICIAL = "reutiliza_senha"

RESPOSTA_SEGURA_SIM: dict[str, bool] = {
    nid: n.resposta_segura for nid, n in ARVORE_PERGUNTAS.items()
}

FATOS_INSEGUROS: dict[str, str] = {
    nid: n.fato_inseguro for nid, n in ARVORE_PERGUNTAS.items()
}


def get_perguntas_map() -> dict[str, str]:
    return {nid: n.texto for nid, n in ARVORE_PERGUNTAS.items()}


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
    40 regras SE…ENTÃO em 2 níveis.
    Nível 1 (R01–R36): disparadas diretamente por hábitos inseguros individuais.
    Nível 2 (R37–R40): compostas, combinam conclusões co-ocorrentes no mesmo caminho.

    Regras compostas válidas por caminho da árvore binária:
      R37 — risco_dispositivo_infectado: path ...→usa_2fa(NÃO)→antivirus(NÃO)→download_pirata(SIM)
      R38 — risco_credenciais_multiplas: path reutiliza(NÃO)→gerenciador(NÃO)→troca(NÃO)→backup(NÃO)→senhas_nav(SIM)
      R39 — risco_comprometimento_total: path reutiliza(SIM)→fraca(SIM)→2fa(SIM)→atualiz(NÃO)→cript(NÃO)
      R40 — risco_fraude_online: path reutiliza(NÃO)→gerenciador(SIM)→2fa_app(NÃO)→comp_dados(SIM)→ssl(NÃO)
    """
    return [
        # ── Nível 1: hábitos individuais (R01–R36) ───────────────────────────
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
        Regra(
            nome="R11",
            premissas=["habito_sem_gerenciador"],
            conclusao="risco_gestao_senha_precaria",
            pontuacao=6,
            recomendacao="Adote um gerenciador de senhas (Bitwarden, 1Password) para criar e armazenar senhas únicas.",
            descricao="Ausência de gerenciador de senhas",
        ),
        Regra(
            nome="R12",
            premissas=["habito_troca_irregular"],
            conclusao="risco_senha_obsoleta",
            pontuacao=5,
            recomendacao="Troque suas senhas a cada 3-6 meses, especialmente após notícias de vazamentos de dados.",
            descricao="Senhas não trocadas regularmente",
        ),
        Regra(
            nome="R13",
            premissas=["habito_2fa_sms"],
            conclusao="risco_2fa_fraco",
            pontuacao=4,
            recomendacao="2FA por SMS é vulnerável a ataques de SIM swap. Prefira apps autenticadores como Google Authenticator.",
            descricao="Uso de 2FA apenas por SMS (método mais fraco)",
        ),
        Regra(
            nome="R14",
            premissas=["habito_sem_bloqueio_tela"],
            conclusao="risco_acesso_fisico",
            pontuacao=8,
            recomendacao="Ative o bloqueio de tela com PIN, senha ou biometria. Sem isso, qualquer pessoa com acesso físico tem acesso a tudo.",
            descricao="Dispositivo sem bloqueio de tela",
        ),
        Regra(
            nome="R15",
            premissas=["habito_nao_verifica_permissoes"],
            conclusao="risco_privacidade_apps",
            pontuacao=6,
            recomendacao="Revise sempre as permissões solicitadas por apps. Recuse câmera, microfone e localização quando não forem necessários.",
            descricao="Instalação de apps sem verificar permissões",
        ),
        Regra(
            nome="R16",
            premissas=["habito_sem_vpn"],
            conclusao="risco_sem_vpn",
            pontuacao=6,
            recomendacao="Use uma VPN (ProtonVPN, Mullvad) ao navegar em redes públicas ou não confiáveis para criptografar seu tráfego.",
            descricao="Navegação em redes não confiáveis sem VPN",
        ),
        Regra(
            nome="R17",
            premissas=["habito_sem_criptografia"],
            conclusao="risco_sem_criptografia",
            pontuacao=5,
            recomendacao="Ative a criptografia de disco no seu dispositivo: BitLocker (Windows), FileVault (Mac) ou similar.",
            descricao="Dispositivo sem criptografia de disco",
        ),
        Regra(
            nome="R18",
            premissas=["habito_sem_monitoramento"],
            conclusao="risco_sem_monitoramento",
            pontuacao=4,
            recomendacao="Verifique regularmente o histórico de acessos e atividades nas suas contas. Ative alertas de login.",
            descricao="Falta de monitoramento de atividades suspeitas nas contas",
        ),
        Regra(
            nome="R19",
            premissas=["habito_pirataria"],
            conclusao="risco_pirataria",
            pontuacao=8,
            recomendacao="Evite downloads piratas: são vetores comuns de malware, ransomware e trojans. Use alternativas gratuitas legítimas.",
            descricao="Download de softwares ou conteúdos piratas",
        ),
        Regra(
            nome="R20",
            premissas=["habito_nao_verifica_dev"],
            conclusao="risco_app_sem_verificacao",
            pontuacao=5,
            recomendacao="Pesquise o desenvolvedor e leia avaliações antes de instalar qualquer app fora das lojas oficiais.",
            descricao="Instalação de apps sem verificar a reputação do desenvolvedor",
        ),
        Regra(
            nome="R21",
            premissas=["habito_compartilha_dispositivo"],
            conclusao="risco_acesso_fisico_compartilhado",
            pontuacao=6,
            recomendacao="Crie perfis de usuário separados no seu dispositivo para quem compartilha, limitando acesso aos seus dados.",
            descricao="Compartilhamento de dispositivo sem restrições de acesso",
        ),
        Regra(
            nome="R22",
            premissas=["habito_sem_filtro_email"],
            conclusao="risco_email_desprotegido",
            pontuacao=5,
            recomendacao="Configure filtros de spam e considere um serviço de e-mail com proteção avançada (Proton Mail, Gmail com 2FA).",
            descricao="E-mail sem filtros de segurança configurados",
        ),
        Regra(
            nome="R23",
            premissas=["habito_nao_reconhece_phishing"],
            conclusao="risco_vulneravel_engenharia_social",
            pontuacao=8,
            recomendacao="Aprenda a identificar phishing: verifique o domínio do remetente, desconfie de urgência e nunca forneça senhas por e-mail.",
            descricao="Dificuldade em identificar ataques de phishing e engenharia social",
        ),
        Regra(
            nome="R24",
            premissas=["habito_nuvem_insegura"],
            conclusao="risco_dados_nuvem_expostos",
            pontuacao=6,
            recomendacao="Proteja seus arquivos na nuvem com senhas fortes, 2FA e verifique periodicamente quem tem acesso.",
            descricao="Dados na nuvem sem proteção adequada",
        ),
        Regra(
            nome="R25",
            premissas=["habito_nao_revoga_acessos"],
            conclusao="risco_acessos_obsoletos",
            pontuacao=4,
            recomendacao="Revise e revogue acessos de apps antigos em Configurações > Segurança de cada conta (Google, Facebook, etc.).",
            descricao="Acessos de aplicativos antigos não revogados",
        ),
        Regra(
            nome="R26",
            premissas=["habito_ignora_ssl"],
            conclusao="risco_fraude_ssl",
            pontuacao=5,
            recomendacao="Aprenda a verificar certificados SSL: cadeado verde, domínio correto e validade. Sites falsos costumam ter erros de certificado.",
            descricao="Incapacidade de identificar certificados SSL inválidos ou sites fraudulentos",
        ),
        Regra(
            nome="R27",
            premissas=["habito_pagamento_inseguro"],
            conclusao="risco_fraude_financeira",
            pontuacao=7,
            recomendacao="Use cartão virtual para compras online (disponível em apps bancários). Prefira PayPal ou Pix em vez de dados de cartão direto.",
            descricao="Uso de métodos de pagamento inseguros em compras online",
        ),
        Regra(
            nome="R28",
            premissas=["habito_nao_desconecta_wifi"],
            conclusao="risco_sessao_wifi_aberta",
            pontuacao=4,
            recomendacao="Sempre desconecte de redes Wi-Fi públicas ao terminar e remova-as da lista de redes salvas.",
            descricao="Sessões em redes Wi-Fi públicas não encerradas adequadamente",
        ),
        Regra(
            nome="R29",
            premissas=["habito_sem_vpn_privacidade"],
            conclusao="risco_privacidade_rede",
            pontuacao=5,
            recomendacao="Considere usar uma VPN para proteger sua privacidade e evitar rastreamento pelo provedor de internet.",
            descricao="Navegação sem proteção de privacidade de rede",
        ),
        Regra(
            nome="R30",
            premissas=["habito_nao_testa_backup"],
            conclusao="risco_backup_inutilizavel",
            pontuacao=3,
            recomendacao="Teste seus backups periodicamente: restaure um arquivo de teste para confirmar que a recuperação funciona.",
            descricao="Backups não testados podem falhar quando mais necessário",
        ),
        Regra(
            nome="R31",
            premissas=["habito_senhas_no_navegador"],
            conclusao="risco_senhas_expostas_navegador",
            pontuacao=7,
            recomendacao="Evite salvar senhas no navegador sem proteção. Use um gerenciador dedicado como Bitwarden (gratuito) ou 1Password.",
            descricao="Senhas armazenadas no navegador sem proteção adicional",
        ),
        # ── Nível 2: regras compostas (válidas para co-ocorrência na árvore) ──
        Regra(
            nome="R32",
            premissas=["risco_credenciais", "risco_senha_vulneravel"],
            conclusao="risco_conta_comprometida",
            pontuacao=20,
            recomendacao=(
                "Combinação crítica: você reutiliza senhas fracas com dados pessoais. "
                "Altere todas as senhas imediatamente usando o Bitwarden (gratuito) e ative 2FA."
            ),
            descricao="Combinação crítica: senhas reutilizadas e fracas",
        ),
        Regra(
            nome="R33",
            premissas=["risco_sem_autenticacao_dupla", "risco_sem_protecao"],
            conclusao="risco_dispositivo_exposto",
            pontuacao=14,
            recomendacao=(
                "Sem 2FA e sem antivírus: seu dispositivo está criticamente exposto. "
                "Instale proteção antivírus e ative 2FA imediatamente."
            ),
            descricao="Combinação crítica: sem 2FA e sem antivírus",
        ),
        Regra(
            nome="R34",
            premissas=["risco_acesso_fisico", "risco_phishing"],
            conclusao="risco_comprometimento_total",
            pontuacao=16,
            recomendacao=(
                "Dispositivo sem bloqueio e suscetível a phishing: risco total de comprometimento. "
                "Ative bloqueio de tela e nunca clique em links sem verificar."
            ),
            descricao="Combinação crítica: dispositivo sem bloqueio + phishing",
        ),
        Regra(
            nome="R35",
            premissas=["risco_credenciais", "risco_malware"],
            conclusao="risco_infeccao_credenciais",
            pontuacao=12,
            recomendacao=(
                "Você reutiliza senhas e instala apps de fontes desconhecidas: "
                "um malware pode capturar todas as suas credenciais de uma vez."
            ),
            descricao="Combinação crítica: reutilização de senhas + apps desconhecidos",
        ),
        Regra(
            nome="R36",
            premissas=["risco_gestao_senha_precaria", "risco_interceptacao"],
            conclusao="risco_rede_sem_gestao",
            pontuacao=12,
            recomendacao=(
                "Sem gerenciador de senhas e usando Wi-Fi público: alto risco de interceptação de credenciais. "
                "Use Bitwarden e uma VPN (ProtonVPN) em redes abertas."
            ),
            descricao="Combinação crítica: sem gestão de senhas + rede pública",
        ),
        Regra(
            nome="R37",
            premissas=["risco_pirataria", "risco_sem_protecao"],
            conclusao="risco_dispositivo_infectado",
            pontuacao=14,
            recomendacao=(
                "Sem antivírus e baixando conteúdo pirata: seu dispositivo tem alto risco de infecção por malware ou ransomware. "
                "Instale um antivírus imediatamente e pare de baixar conteúdo de fontes não oficiais."
            ),
            descricao="Combinação crítica: sem antivírus + downloads piratas",
        ),
        Regra(
            nome="R38",
            premissas=["risco_gestao_senha_precaria", "risco_senhas_expostas_navegador"],
            conclusao="risco_credenciais_multiplas_expostas",
            pontuacao=12,
            recomendacao=(
                "Sem gerenciador de senhas e salvando senhas no navegador: múltiplas credenciais estão expostas. "
                "Adote o Bitwarden e remova todas as senhas salvas no navegador."
            ),
            descricao="Combinação crítica: sem gerenciador de senhas + senhas no navegador",
        ),
        Regra(
            nome="R39",
            premissas=["risco_conta_comprometida", "risco_sem_criptografia"],
            conclusao="risco_comprometimento_total_dados",
            pontuacao=16,
            recomendacao=(
                "Senhas fracas reutilizadas E dispositivo sem criptografia: um atacante com acesso físico "
                "leria todos os seus arquivos e credenciais. Ative BitLocker/FileVault e troque todas as senhas."
            ),
            descricao="Combinação crítica: conta comprometida + sem criptografia de disco",
        ),
        Regra(
            nome="R40",
            premissas=["risco_dados_expostos", "risco_fraude_ssl"],
            conclusao="risco_fraude_online",
            pontuacao=12,
            recomendacao=(
                "Você envia dados em sites sem HTTPS e não identifica certificados SSL falsos: "
                "alto risco de fraude online. Verifique sempre o cadeado e o domínio antes de qualquer transação."
            ),
            descricao="Combinação crítica: dados sem HTTPS + incapacidade de detectar SSL fraudulento",
        ),
    ]
