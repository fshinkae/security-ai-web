(() => {
  const container = document.getElementById("quiz-container");
  if (!container) return;

  const questaoInicial = container.dataset.questaoInicial;
  const allCards = Array.from(container.querySelectorAll(".quiz-card"));
  if (!allCards.length) return;

  // Mapa de id → card element
  const cardMap = {};
  allCards.forEach(c => { cardMap[c.dataset.id] = c; });

  const btnAnterior      = document.getElementById("btn-anterior");
  const btnProxima       = document.getElementById("btn-proxima");
  const btnEnviar        = document.getElementById("btn-enviar");
  const barraProgresso   = document.getElementById("progresso-barra");
  const labelProgresso   = document.getElementById("progresso-label");
  const labelGrupo       = document.getElementById("progresso-grupo");
  const inputRespondidas = document.getElementById("perguntas-respondidas");

  let idAtual   = questaoInicial;
  let historico = [];           // IDs na ordem em que foram exibidos

  // Caminho fixo de 5 perguntas na árvore de 5 níveis
  const MIN_PATH = 5;
  const MAX_PATH = 5;

  function respostaSelecionada(id) {
    const radios = document.querySelectorAll(`input[name="pergunta_${id}"]:checked`);
    return radios.length ? radios[0].value : null;
  }

  function atualizarProgresso() {
    const visitados = historico.length + 1;
    const estimado  = Math.max(visitados, MIN_PATH);
    const pct       = Math.min(Math.round(((visitados - 1) / estimado) * 100), 95);

    barraProgresso.style.width = pct + "%";
    labelProgresso.textContent = `Pergunta ${visitados}`;

    const card = cardMap[idAtual];
    if (card) labelGrupo.textContent = card.dataset.grupo || "";
  }

  function mostrar(id) {
    allCards.forEach(c => c.classList.add("hidden"));
    const card = cardMap[id];
    if (card) card.classList.remove("hidden");

    idAtual = id;

    const isUltima = !card || (!card.dataset.proximaSim && !card.dataset.proximaNao);
    btnProxima.classList.toggle("hidden", isUltima);
    btnEnviar.classList.toggle("hidden", !isUltima);
    btnAnterior.disabled = historico.length === 0;

    atualizarProgresso();
  }

  function avancar() {
    const resposta = respostaSelecionada(idAtual);
    if (!resposta) {
      const cardAtual = cardMap[idAtual];
      if (cardAtual) {
        cardAtual.querySelector(".bg-gray-900").classList.add("shake");
        setTimeout(() => cardAtual.querySelector(".bg-gray-900").classList.remove("shake"), 400);
      }
      return;
    }

    const card      = cardMap[idAtual];
    const proximaId = resposta === "sim" ? card.dataset.proximaSim : card.dataset.proximaNao;

    historico.push(idAtual);
    inputRespondidas.value = historico.join(",");

    if (proximaId) {
      mostrar(proximaId);
    } else {
      // Último nó — inclui o atual na lista e submete
      inputRespondidas.value = historico.join(",");
      document.getElementById("quiz-form").submit();
    }
  }

  function voltar() {
    if (historico.length === 0) return;
    const anterior = historico.pop();
    inputRespondidas.value = historico.join(",");
    mostrar(anterior);
  }

  // Estilo visual ao selecionar opção
  container.addEventListener("click", e => {
    const label = e.target.closest(".opcao-label");
    if (!label) return;

    const radio = label.querySelector(".opcao-radio");
    const name  = radio.name;

    document.querySelectorAll(`input[name="${name}"]`).forEach(r => {
      const btn = r.closest(".opcao-label").querySelector(".opcao-btn");
      btn.classList.remove("border-green-500", "bg-green-900/20", "border-red-500", "bg-red-900/20");
      btn.classList.add("border-gray-700", "bg-gray-800");
    });

    const btn = label.querySelector(".opcao-btn");
    if (radio.value === "sim") {
      btn.classList.replace("border-gray-700", "border-green-500");
      btn.classList.replace("bg-gray-800",    "bg-green-900/20");
    } else {
      btn.classList.replace("border-gray-700", "border-red-500");
      btn.classList.replace("bg-gray-800",    "bg-red-900/20");
    }
  });

  btnProxima.addEventListener("click", avancar);
  btnAnterior.addEventListener("click", voltar);

  // Validação final: garante que o card atual também está na lista ao submeter
  document.getElementById("quiz-form").addEventListener("submit", e => {
    const resposta = respostaSelecionada(idAtual);
    if (!resposta) {
      e.preventDefault();
      const cardAtual = cardMap[idAtual];
      if (cardAtual) {
        cardAtual.querySelector(".bg-gray-900").classList.add("shake");
        setTimeout(() => cardAtual.querySelector(".bg-gray-900").classList.remove("shake"), 400);
      }
      return;
    }
    // Inclui pergunta atual se ainda não estiver na lista
    const ids = inputRespondidas.value ? inputRespondidas.value.split(",") : [];
    if (!ids.includes(idAtual)) {
      ids.push(idAtual);
      inputRespondidas.value = ids.join(",");
    }
  });

  mostrar(questaoInicial);
})();
