Camada de Apresentação

Tela HTML simples servida pelo nginx (porta 8080).

O que faz: lista as disciplinas com vagas, permite matricular o aluno e mostra a mensagem de resposta.

Com quem conversa: somente com a API (camada de negócio), em http://localhost:5000. Nunca acessa o banco direto.

Arquivos:
- index.html: a página
- Dockerfile: empacota a página no nginx
