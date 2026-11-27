# Logs do fluxo principal (matrícula em disciplina)

Logs copiados do terminal (docker compose logs api), com o sistema rodando em 3 camadas.

## Matrícula confirmada e recusada por falta de vagas

```
api_academico  | 172.18.0.1 - - [27/Nov/2026 00:49:15] "GET /disciplinas HTTP/1.1" 200 -
api_academico  | 172.18.0.1 - - [27/Nov/2026 00:50:57] "GET /disciplinas HTTP/1.1" 200 -
api_academico  | 172.18.0.1 - - [27/Nov/2026 01:01:34] "GET /disciplinas HTTP/1.1" 200 -
api_academico  | [NEGOCIO] Matricula confirmada: aluno=2 disciplina=1
api_academico  | 172.18.0.1 - - [27/Nov/2026 01:02:29] "POST /matricula HTTP/1.1" 200 -
api_academico  | 172.18.0.1 - - [27/Nov/2026 01:02:30] "GET /disciplinas HTTP/1.1" 200 -
api_academico  | [NEGOCIO] Matricula confirmada: aluno=3 disciplina=4
api_academico  | 172.18.0.1 - - [27/Nov/2026 01:02:39] "POST /matricula HTTP/1.1" 200 -
api_academico  | 172.18.0.1 - - [27/Nov/2026 01:02:40] "GET /disciplinas HTTP/1.1" 200 -
api_academico  | 172.18.0.1 - - [27/Nov/2026 01:03:25] "GET /matriculas/3 HTTP/1.1" 200 -
api_academico  | [NEGOCIO] Matricula recusada: aluno=3 disciplina=4 motivo=Não há vagas nesta disciplina.
api_academico  | 172.18.0.1 - - [27/Nov/2026 01:03:29] "POST /matricula HTTP/1.1" 409 -
api_academico  | 172.18.0.1 - - [27/Nov/2026 01:03:30] "GET /disciplinas HTTP/1.1" 200 -
api_academico  | [NEGOCIO] Matricula recusada: aluno=1 disciplina=4 motivo=Não há vagas nesta disciplina.
api_academico  | 172.18.0.1 - - [27/Nov/2026 01:04:06] "POST /matricula HTTP/1.1" 409 -
api_academico  | 172.18.0.1 - - [27/Nov/2026 01:04:06] "GET /disciplinas HTTP/1.1" 200 -
```

- Matricula confirmada: a regra de negócio aceitou (há vaga e o aluno não estava matriculado).
- Matricula recusada (HTTP 409): a disciplina 4 tinha 1 vaga, ocupada pelo aluno 3.
