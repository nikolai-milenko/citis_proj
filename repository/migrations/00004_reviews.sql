-- +goose Up
-- +goose StatementBegin
CREATE SCHEMA reviews;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP SCHEMA reviews;
-- +goose StatementEnd
