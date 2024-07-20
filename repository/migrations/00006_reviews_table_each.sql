-- +goose Up
-- +goose StatementBegin
CREATE TABLE IF NOT EXISTS reviews.review
(
    id          int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    rating      numeric(3, 1) NOT NULL,
    rating_text text          NOT NULL,
    product_id  INTEGER       NOT NULL,
    FOREIGN KEY (product_id) REFERENCES reviews.product (id) ON DELETE CASCADE
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE reviews.review;
-- +goose StatementEnd
