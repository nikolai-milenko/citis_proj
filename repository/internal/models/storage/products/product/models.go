package product

import "repository/internal/models/storage"

type Review struct {
	Review       string  `db:"rating"`
	ReviewRating float32 `db:"rating_text"`
}

type Product struct {
	URL     string  `db:"url"`
	Name    string  `db:"name"`
	Price   int     `db:"price"`
	Rating  float32 `db:"price"`
	Reviews []Review
}

const ProductsTableName storage.TableName = "reviews.product"

const (
	ProductsIDField     storage.FieldName = "id"
	ProductsURLField    storage.FieldName = "url"
	ProductsNameField   storage.FieldName = "name"
	ProductsPriceField  storage.FieldName = "price"
	ProductsRatingField storage.FieldName = "rating"
)

const ReviewsTableName storage.TableName = "reviews.review"

const (
	ReviewsRatingField storage.FieldName = "rating"
	ReviewsTextField   storage.FieldName = "rating_text"
	ReviewProductID                      = "product_id"
)
