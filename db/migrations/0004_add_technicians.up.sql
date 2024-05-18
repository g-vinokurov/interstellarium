create table if not exists technicians (
    id      serial primary key,
    user_id integer not null references users (id) on delete cascade
);
