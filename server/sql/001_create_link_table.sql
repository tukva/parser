CREATE TABLE tb_link (
    link_id serial PRIMARY KEY,
    name_site varchar(25) NOT NULL,
    link varchar(100) NOT NULL UNIQUE,
    created_on TIMESTAMP NOT NULL
)
