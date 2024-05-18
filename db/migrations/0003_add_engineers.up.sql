create table if not exists engineers (
    id      serial primary key,
    user_id integer not null references users (id) on delete cascade
);
