create EXTENSION if not exists "uuid-ossp";

create schema if not exists utils;

create table if not exists sites (
    id uuid primary key,
    domain text not null unique,
    created_at timestamp not null default now()
);

create table if not exists pages (
    id uuid primary key,
    site_id uuid not null references sites(id),
    url text not null unique,
    created_at timestamp not null default now(),
    updated_at timestamp not null default now(),
    status text not null default 'pending',
    is_pagination boolean not null default false,
    -- figure out about refreshing logic
    refresh_interval int not null default 0,
    refresh_at timestamp not null default now(),
    last_refresh timestamp not null default now(),
    xpaths json not null default '{}'::json,
    expired boolean not null default false
);

create table if not exists pagination_events (
    id uuid primary key,
    page_id uuid not null references pages(id),
    created_at timestamp not null default now(),
    status text not null default 'pending',
    html text,
    urls json not null default '{}'::json
);

create table if not exists page_events (
    id uuid primary key,
    page_id uuid not null references pages(id),
    pagination_event_id uuid references pagination_events(id),
    created_at timestamp not null default now(),
    status text not null default 'pending',
    html text,
    data json not null default '{}'::json
);

-- create table if not exists page_event_errors (
--     id uuid primary key,
--     page_event_id uuid not null references page_events(id),
--     created_at timestamp not null default now(),
--     message text not null
-- );

-- move user data to another database in the future
create table if not exists utils.users (
    id uuid primary key,
    full_name text not null,
    username text not null unique,
    email text not null unique,
    password text not null,
    created_at timestamp not null default now()
);

create index if not exists pages_site_id_idx on pages(site_id);
create index if not exists pagination_events_page_id_idx on pagination_events(page_id);
create index if not exists page_events_page_id_idx on page_events(page_id);
