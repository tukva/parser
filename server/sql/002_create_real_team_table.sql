CREATE TABLE tb_real_team (
    real_team_id serial PRIMARY KEY,
    name varchar(80) NOT NULL UNIQUE,
    created_on TIMESTAMP NOT NULL
)
