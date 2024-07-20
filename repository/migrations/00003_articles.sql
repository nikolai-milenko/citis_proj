-- +goose Up
-- +goose StatementBegin
CREATE TABLE articles.articles (
    id bigint primary key GENERATED ALWAYS AS IDENTITY,
    url text not null,
    text text not null,
    description text not null,
    created_at timestamp not null default now(),
    UNIQUE (url)
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE articles.articles;
-- +goose StatementEnd
