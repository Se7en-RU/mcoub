create table coubs
(
    id         	bigserial  primary key,
    coub_id     varchar(20) not null unique,
    shazam_data        jsonb not null,
    created_at timestamp NOT NULL DEFAULT NOW()
);

create index coubs_coub_id_index
    on coubs (coub_id);