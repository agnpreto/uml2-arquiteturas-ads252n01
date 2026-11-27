
@echo off
title SmartChatz - Inicializacao

echo =====================================
echo       SMARTCHATZ - CHAT EM TEMPO REAL
echo =====================================
echo.

cd /d "%~dp0servicos\servidor"

if not exist node_modules (
    echo Instalando dependencias...
    call npm.cmd install
)

echo.
echo Iniciando o servidor SmartChatz...
echo.

start "Servidor SmartChatz" cmd /k "node server.js"

timeout /t 3 /nobreak > nul

start http://localhost:3000

echo.
echo SmartChatz iniciado!
echo Para encerrar, feche a janela do servidor.
