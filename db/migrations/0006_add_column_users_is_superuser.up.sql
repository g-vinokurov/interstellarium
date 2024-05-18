alter table if exists users
    add column is_superuser boolean not null default false;
