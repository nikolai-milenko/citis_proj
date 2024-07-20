-- +goose Up
-- +goose StatementBegin
CREATE TABLE articles.blacklist(
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url text NOT NULL,
    hits int NOT NULL DEFAULT 0,
    created_at timestamptz NOT NULL DEFAULT now()
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE articles.blacklist;
-- +goose StatementEnd
