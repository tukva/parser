CREATE TABLE tb_link (
    link_id serial PRIMARY KEY,
    site_name varchar(25) NOT NULL,
    link varchar(100) NOT NULL UNIQUE,
    created_on TIMESTAMP NOT NULL,
    attributes jsonb NOT NULL
)
