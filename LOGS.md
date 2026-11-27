PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> git --version
git version 2.55.0.windows.2
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> git config --global user.name
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> git config --global user.email
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> git config --global user.name "Remulo A. Fernandes"
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> git config --global user.name "Remulo A. Fernandes"
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> git config --global user.email "reminh961@gmail.com"
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> git config --global --list
core.editor="C:\Users\remin\AppData\Local\Programs\Microsoft VS Code\bin\code" --wait
user.name=Remulo A. Fernandes
user.email=reminh961@gmail.com
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> gh --version
gh : O termo 'gh' não é reconhecido como nome de cmdlet, função, arquivo de script ou programa
operável. Verifique a grafia do nome ou, se um caminho tiver sido incluído, veja se o caminho
está correto e tente novamente.
No linha:1 caractere:1
+ gh --version
+ ~~
    + CategoryInfo          : ObjectNotFound: (gh:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
 
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> git ls-remote https://github.com/reminh961-lgtm/uml2-arquiteturas-ads252n01.git
ac74650158245b19ea8039a184cb96c79a73ca5a        HEAD
ac74650158245b19ea8039a184cb96c79a73ca5a        refs/heads/main
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> dir
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> pwd

Path                                              
----                                              
C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz


PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> git clone https://github.com/reminh961-lgtm/uml2-arquiteturas-ads252n01.git .
Cloning into '.'...
remote: Enumerating objects: 38, done.
remote: Counting objects: 100% (38/38), done.
remote: Compressing objects: 100% (31/31), done.
remote: Total 38 (delta 12), reused 13 (delta 2), pack-reused 0 (from 0)
Receiving objects: 100% (38/38), done.
Resolving deltas: 100% (12/12), done.
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> git log -5 --oneline
ac74650 (HEAD -> main, origin/main, origin/HEAD) Create README.md
bcb78dc Create README.md
ae5a1ed Add functional and non-functional requirements
6bc604e Update deadline and team member details in README
8111e4d Update README.md
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> cd servicos/servidor
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz\servicos\servidor> npm init -y
npm : O arquivo C:\Program Files\nodejs\npm.ps1 não pode ser carregado porque a execução de
scripts foi desabilitada neste sistema. Para obter mais informações, consulte
about_Execution_Policies em https://go.microsoft.com/fwlink/?LinkID=135170.
No linha:1 caractere:1
+ npm init -y
+ ~~~
    + CategoryInfo          : ErrodeSegurança: (:) [], PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz\servicos\servidor> npm.cmd init -y
Wrote to C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz\servicos\servidor\package.json:

{
  "name": "servidor",
  "version": "1.0.0",
  "description": "Este componente será responsável pelo gerenciamento da comunicação do sistema SmartChatz.",
  "main": "server.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "start": "node server.js"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "type": "commonjs"
}


PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz\servicos\servidor> npm.cmd install express socket.io

added 86 packages, and audited 87 packages in 9s

32 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz\servicos\servidor> node server.js
SmartChatz iniciado na porta 3000
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz\servicos\servidor>
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz\servicos\servidor> node server.js
SmartChatz iniciado na porta 3000
Um usuário se conectou: I3h0c8YEdGPHC4FUAAAA
Rem entrou no chat.
Rem saiu do chat.
Um usuário se conectou: bZI5jt5g3f1PgDttAAAB
Rem entrou no chat.
Rem: Oi! teste, teste...
Um usuário se conectou: aycAezES2qtN7HkRAAAC
Eduardo entrou no chat.
Eduardo: Ola Rem
Rem: oi
Eduardo saiu do chat.
Rem saiu do chat.
Um usuário se conectou: xEPhcBYVur-K5_jmAAAD
Um usuário saiu do chat.
Um usuário se conectou: IAtidWPdwLwTMkm4AAAE
Um usuário saiu do chat.

PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> cd ../..
PS C:\Users\remin\OneDrive> git status
fatal: not a git repository (or any of the parent directories): .git
PS C:\Users\remin\OneDrive> cd "C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz"
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> git status
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        servicos/cliente/index.html
        servicos/cliente/script.js
        servicos/cliente/style.css
        servicos/servidor/package-lock.json
        servicos/servidor/package.json
        servicos/servidor/server.js

nothing added to commit but untracked files present (use "git add" to track)
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> git add servicos/cliente/index.html servicos/cliente/script.js servicos/cliente/style.css servicos/servidor/package-lock.json servicos/servidor/package.json servicos/servidor/server.js

warning: in the working copy of 'servicos/servidor/package-lock.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'servicos/servidor/package.json', LF will be replaced by CRLF the next time Git touches it
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> git status
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   servicos/cliente/index.html
        new file:   servicos/cliente/script.js
        new file:   servicos/cliente/style.css
        new file:   servicos/servidor/package-lock.json
        new file:   servicos/servidor/package.json
        new file:   servicos/servidor/server.js

PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> git commit -m "Implementa chat em tempo real com cliente e servidor"
[main fa1cb03] Implementa chat em tempo real com cliente e servidor
 6 files changed, 1418 insertions(+)
 create mode 100644 servicos/cliente/index.html
 create mode 100644 servicos/cliente/script.js
 create mode 100644 servicos/cliente/style.css
 create mode 100644 servicos/servidor/package-lock.json
 create mode 100644 servicos/servidor/package.json
 create mode 100644 servicos/servidor/server.js
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz> git push origin main
info: please complete authentication in your browser...
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Delta compression using up to 12 threads
Compressing objects: 100% (11/11), done.
Writing objects: 100% (11/11), 12.28 KiB | 2.05 MiB/s, done.
Total 11 (delta 1), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/reminh961-lgtm/uml2-arquiteturas-ads252n01.git
   ac74650..fa1cb03  main -> main
PS C:\Users\remin\OneDrive\Área de Trabalho\SmartChatz>

 
