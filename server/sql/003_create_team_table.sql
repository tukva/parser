CREATE TABLE tb_team (
    team_id serial PRIMARY KEY,
    name varchar(80) NOT NULL,
    created_on TIMESTAMP NOT NULL,
    name_site varchar(25) NOT NULL UNIQUE,
    real_team_id int,
    link_id int NOT NULL,
    FOREIGN KEY (real_team_id) REFERENCES tb_real_team (real_team_id) ON DELETE CASCADE,
    FOREIGN KEY (link_id) REFERENCES tb_link (link_id) ON DELETE CASCADE
)
