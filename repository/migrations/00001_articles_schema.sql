-- +goose Up
-- +goose StatementBegin
CREATE SCHEMA articles;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP SCHEMA articles CASCADE;
-- +goose StatementEnd
