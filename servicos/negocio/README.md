# Camada de Negócio

API em Python (Flask), porta 5000.

**O que faz:** aplica as regras de matrícula (a disciplina precisa ter vagas e o aluno não pode estar matriculado nela) e é a única camada que acessa o banco.

**Endpoints:**
- GET /disciplinas: lista as disciplinas e as vagas
- POST /matricula: matricula o aluno (recebe aluno_id e disciplina_id)
- GET /matriculas/<aluno_id>: lista as matrículas do aluno

**Arquivos:**
- app.py: inicia a API
- disciplinas.py: lista de disciplinas
- matricula.py: regras de matrícula
- db.py: conexão com o banco
- requirements.txt e Dockerfile
