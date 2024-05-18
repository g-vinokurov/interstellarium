create table if not exists users (
    id            serial primary key,
    email         varchar(255) not null unique,
    password_hash varchar(512) not null,
    name          varchar(255)
);