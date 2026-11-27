# Camada de Dados

Banco PostgreSQL.

**O que faz:** guarda alunos, disciplinas e matrículas.

**Tabelas:**
- alunos
- disciplinas (com o número de vagas)
- matriculas (liga aluno e disciplina; o mesmo aluno não repete a mesma disciplina)

**Arquivo:**
- init.sql: cria as tabelas e os dados de exemplo (3 alunos e 4 disciplinas) quando o banco sobe
