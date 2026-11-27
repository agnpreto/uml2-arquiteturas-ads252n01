CREATE TABLE IF NOT EXISTS alunos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    matricula VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS disciplinas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    vagas INTEGER NOT NULL DEFAULT 30
);

CREATE TABLE IF NOT EXISTS matriculas (
    id SERIAL PRIMARY KEY,
    aluno_id INTEGER REFERENCES alunos(id),
    disciplina_id INTEGER REFERENCES disciplinas(id),
    data_matricula TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (aluno_id, disciplina_id)
);

INSERT INTO alunos (nome, matricula) VALUES
('Aluno 1', '1'),
('Aluno 2', '2'),
('Aluno 3', '3')
ON CONFLICT (matricula) DO NOTHING;

INSERT INTO disciplinas (nome, codigo, vagas) VALUES
('Programação', '1', 30),
('Banco de Dados', '2', 30),
('Engenharia de Software', '3', 30),
('Arquitetura de Sistemas', '4', 1)
ON CONFLICT (codigo) DO NOTHING;