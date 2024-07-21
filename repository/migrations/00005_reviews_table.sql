-- +goose Up
-- +goose StatementBegin
CREATE TABLE IF NOT EXISTS reviews.product
(
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    url        text                                NOT NULL,
    name       VARCHAR(255)                        NOT NULL,
    price      int                                 NOT NULL,
    rating     NUMERIC(3, 1)                       NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE reviews.product;
-- +goose StatementEnd
