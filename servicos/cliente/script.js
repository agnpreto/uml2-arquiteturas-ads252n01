
const socket = io("http://localhost:3000");

const entrada = document.getElementById("entrada");
const areaChat = document.getElementById("areaChat");

const campoNome = document.getElementById("nome");
const btnEntrar = document.getElementById("btnEntrar");

const formMensagem = document.getElementById("formMensagem");
const campoMensagem = document.getElementById("mensagem");
const listaMensagens = document.getElementById("mensagens");

let nomeUsuario = "";

function adicionarAviso(texto) {
    const aviso = document.createElement("p");
    aviso.classList.add("aviso");
    aviso.textContent = texto;

    listaMensagens.appendChild(aviso);
    listaMensagens.scrollTop = listaMensagens.scrollHeight;
}

function adicionarMensagem(nome, mensagem) {
    const novaMensagem = document.createElement("p");
    novaMensagem.classList.add("mensagem");
    novaMensagem.textContent = `${nome}: ${mensagem}`;

    listaMensagens.appendChild(novaMensagem);
    listaMensagens.scrollTop = listaMensagens.scrollHeight;
}

btnEntrar.addEventListener("click", () => {
    const nome = campoNome.value.trim();

    if (nome === "") {
        alert("Digite seu nome para entrar no chat.");
        return;
    }

    nomeUsuario = nome;

    socket.emit("entrar-chat", nomeUsuario);

    entrada.classList.add("oculto");
    areaChat.classList.remove("oculto");

    adicionarAviso(`Você entrou no chat como ${nomeUsuario}.`);

    campoMensagem.focus();
});

formMensagem.addEventListener("submit", (evento) => {
    evento.preventDefault();

    const mensagem = campoMensagem.value.trim();

    if (mensagem === "") {
        return;
    }

    socket.emit("enviar-mensagem", mensagem);

    campoMensagem.value = "";
    campoMensagem.focus();
});

socket.on("receber-mensagem", (dados) => {
    adicionarMensagem(dados.nome, dados.mensagem);
});

socket.on("usuario-entrou", (nome) => {
    adicionarAviso(`${nome} entrou no chat.`);
});

socket.on("usuario-saiu", (nome) => {
    adicionarAviso(`${nome} saiu do chat.`);
});

socket.on("connect_error", () => {
    adicionarAviso("Não foi possível conectar ao servidor.");
});
