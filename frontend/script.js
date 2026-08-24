
const API_URL = "/api/perguntar";

const chatScroll = document.getElementById("chatScroll");
const form = document.getElementById("composerForm");
const input = document.getElementById("perguntaInput");
const sendBtn = document.getElementById("sendBtn");
const suggestions = document.getElementById("suggestions");

function rolarParaFinal() {
  chatScroll.scrollTop = chatScroll.scrollHeight;
}

function adicionarMensagem(texto, autor) {
  const msg = document.createElement("div");
  msg.className = `msg msg--${autor}`;

  const bubble = document.createElement("div");
  bubble.className = "msg__bubble";
  bubble.textContent = texto;

  msg.appendChild(bubble);
  chatScroll.appendChild(msg);
  rolarParaFinal();
  return msg;
}

function adicionarCarregando() {
  const msg = document.createElement("div");
  msg.className = "msg msg--bot";
  msg.id = "msgCarregando";

  const bubble = document.createElement("div");
  bubble.className = "msg__bubble";
  bubble.innerHTML = '<span class="dots"><span></span><span></span><span></span></span>';

  msg.appendChild(bubble);
  chatScroll.appendChild(msg);
  rolarParaFinal();
}

function removerCarregando() {
  const el = document.getElementById("msgCarregando");
  if (el) el.remove();
}

function definirEnviando(enviando) {
  input.disabled = enviando;
  sendBtn.disabled = enviando;
  suggestions.querySelectorAll(".chip").forEach((chip) => (chip.disabled = enviando));
}

async function enviarPergunta(pergunta) {
  const textoLimpo = pergunta.trim();
  if (!textoLimpo) return;

  adicionarMensagem(textoLimpo, "user");
  input.value = "";
  definirEnviando(true);
  adicionarCarregando();

  try {
    const resposta = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pergunta: textoLimpo }),
    });

    const dados = await resposta.json();
    removerCarregando();

    if (!resposta.ok) {
      throw new Error(dados.erro || "Erro ao consultar o assistente.");
    }

    adicionarMensagem(dados.resposta, "bot");
  } catch (erro) {
    removerCarregando();
    const msg = adicionarMensagem(
      "Não consegui falar com o servidor agora. Verifique se o backend está rodando e tente de novo.",
      "bot"
    );
    msg.classList.add("msg--error");
    console.error(erro);
  } finally {
    definirEnviando(false);
    input.focus();
  }
}

form.addEventListener("submit", (evento) => {
  evento.preventDefault();
  enviarPergunta(input.value);
});

suggestions.addEventListener("click", (evento) => {
  const chip = evento.target.closest(".chip");
  if (!chip) return;
  enviarPergunta(chip.dataset.q);
});
