-- 
-- depends: 

CREATE SCHEMA "example";

CREATE TABLE "example"."cep" (
    id SERIAL,
    cep VARCHAR(8) NOT NULL UNIQUE,
    logradouro VARCHAR(250),
    bairro VARCHAR(150),
    cidade VARCHAR(100) NOT NULL,
    uf VARCHAR(2) NOT NULL,

    CONSTRAINT cep_pk PRIMARY KEY (id)
);