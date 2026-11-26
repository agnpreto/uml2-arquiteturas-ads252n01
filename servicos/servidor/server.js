
const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const path = require("path");

const app = express();
app.use(express.static(path.join(__dirname, "../cliente")));
const servidor = http.createServer(app);

const io = new Server(servidor, {
    cors: {
        origin: "*"
    }
});

const PORTA = 3000;

io.on("connection", (socket) => {
    console.log("Um usuário se conectou:", socket.id);

    socket.on("entrar-chat", (nome) => {
        socket.data.nome = nome;

        console.log(`${nome} entrou no chat.`);

        socket.broadcast.emit("usuario-entrou", nome);
    });

    socket.on("enviar-mensagem", (mensagem) => {
        const nome = socket.data.nome || "Anônimo";

        console.log(`${nome}: ${mensagem}`);

        io.emit("receber-mensagem", {
            nome: nome,
            mensagem: mensagem
        });
    });

    socket.on("disconnect", () => {
        const nome = socket.data.nome || "Um usuário";

        console.log(`${nome} saiu do chat.`);

        socket.broadcast.emit("usuario-saiu", nome);
    });
});

servidor.listen(PORTA, () => {
    console.log(`SmartChatz iniciado na porta ${PORTA}`);
});
