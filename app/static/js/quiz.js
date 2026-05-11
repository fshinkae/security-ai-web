(() => {
  const cards = Array.from(document.querySelectorAll(".quiz-card"));
  if (!cards.length) return;

  const total = cards.length;
  let atual = 0;

  const btnAnterior = document.getElementById("btn-anterior");
  const btnProxima  = document.getElementById("btn-proxima");
  const btnEnviar   = document.getElementById("btn-enviar");
  const barra       = document.getElementById("progresso-barra");
  const label       = document.getElementById("progresso-label");
  const pct         = document.getElementById("progresso-pct");
  const form        = document.getElementById("quiz-form");

  function atualizarProgresso(respondidas) {
    const perc = Math.round((respondidas / total) * 100);
    barra.style.width = perc + "%";
    pct.textContent   = perc + "%";
    label.textContent = `Pergunta ${atual + 1} de ${total}`;
  }

  function contarRespondidas() {
    return cards.filter((_, i) => {
      const name = cards[i].querySelector("input[type=radio]").name;
      return !!document.querySelector(`input[name="${name}"]:checked`);
    }).length;
  }

  function mostrar(index) {
    cards.forEach((c, i) => c.classList.toggle("hidden", i !== index));
    btnAnterior.disabled = index === 0;

    const isUltima = index === total - 1;
    btnProxima.classList.toggle("hidden", isUltima);
    btnEnviar.classList.toggle("hidden", !isUltima);

    atualizarProgresso(contarRespondidas());
  }

  // Estilo visual ao selecionar opção
  document.querySelectorAll(".opcao-label").forEach(label => {
    label.addEventListener("click", () => {
      const name = label.querySelector(".opcao-radio").name;
      document.querySelectorAll(`input[name="${name}"]`).forEach(radio => {
        const btn = radio.closest(".opcao-label").querySelector(".opcao-btn");
        btn.classList.remove("border-green-500", "bg-green-900/20", "border-red-500", "bg-red-900/20");
        btn.classList.add("border-gray-700", "bg-gray-800");
      });

      const radio = label.querySelector(".opcao-radio");
      const btn   = label.querySelector(".opcao-btn");
      if (radio.value === "sim") {
        btn.classList.replace("border-gray-700", "border-green-500");
        btn.classList.replace("bg-gray-800",    "bg-green-900/20");
      } else {
        btn.classList.replace("border-gray-700", "border-red-500");
        btn.classList.replace("bg-gray-800",    "bg-red-900/20");
      }

      atualizarProgresso(contarRespondidas());
    });
  });

  btnProxima.addEventListener("click", () => {
    const name = cards[atual].querySelector("input[type=radio]").name;
    if (!document.querySelector(`input[name="${name}"]:checked`)) {
      cards[atual].querySelector(".opcao-btn").parentElement
        .parentElement.classList.add("shake");
      setTimeout(() =>
        cards[atual].querySelectorAll(".opcao-btn").forEach(b =>
          b.closest(".opcao-label").classList.remove("shake")
        ), 400);
      return;
    }
    if (atual < total - 1) mostrar(++atual);
  });

  btnAnterior.addEventListener("click", () => {
    if (atual > 0) mostrar(--atual);
  });

  // Validação final antes do submit
  form.addEventListener("submit", e => {
    const naoRespondidas = cards.filter((_, i) => {
      const name = cards[i].querySelector("input[type=radio]").name;
      return !document.querySelector(`input[name="${name}"]:checked`);
    });

    if (naoRespondidas.length) {
      e.preventDefault();
      // Navega para a primeira pergunta sem resposta
      const index = cards.indexOf(naoRespondidas[0]);
      mostrar(index);
      atual = index;
    }
  });

  mostrar(0);
})();
