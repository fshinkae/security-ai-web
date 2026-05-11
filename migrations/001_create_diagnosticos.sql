CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS diagnosticos (
    id                  UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome                TEXT,
    respostas           JSONB       NOT NULL,
    pontuacao           INTEGER     NOT NULL,
    nivel_risco         TEXT        NOT NULL CHECK (nivel_risco IN ('baixo', 'medio', 'alto')),
    regras_disparadas   TEXT[]      NOT NULL DEFAULT '{}',
    conclusoes_derivadas TEXT[]     NOT NULL DEFAULT '{}',
    recomendacoes       TEXT[]      NOT NULL DEFAULT '{}',
    falhas_detectadas   TEXT[]      NOT NULL DEFAULT '{}',
    criado_em           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_diagnosticos_nivel_risco ON diagnosticos (nivel_risco);
CREATE INDEX IF NOT EXISTS idx_diagnosticos_criado_em   ON diagnosticos (criado_em DESC);