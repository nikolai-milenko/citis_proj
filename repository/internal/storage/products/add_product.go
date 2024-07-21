package products

import (
	"context"
	"fmt"
	product2 "repository/internal/models/storage/products/product"
	product "repository/internal/models/usecase/products/product"
)

func (i *Implementation) AddProduct(ctx context.Context, product product.Product) error {
	query := fmt.Sprintf("INSERT INTO %s(%s, %s, %s, %s) VALUES ($1, $2, $3, $4) RETURNING %s", product2.ProductsTableName, product2.ProductsURLField, product2.ProductsNameField, product2.ProductsPriceField, product2.ProductsRatingField, product2.ProductsIDField)

	var id int

	err := i.conn.QueryRow(ctx, query, product.URL, product.Name, product.Price, product.Rating).Scan(&id)
	if err != nil {
		return err
	}

	for _, review := range product.Reviews {
		err = i.addReviews(ctx, review, id)
		if err != nil {
			return err
		}
	}

	return nil
}

func (i *Implementation) addReviews(ctx context.Context, review product.Review, productID int) error {
	query := fmt.Sprintf("INSERT INTO %s(%s, %s, %s) VALUES ($1, $2, $3)", product2.ReviewsTableName, product2.ReviewsRatingField, product2.ReviewsTextField, product2.ReviewProductID)

	_, err := i.conn.Exec(ctx, query, review.ReviewRating, review.Review, productID)
	if err != nil {
		return err
	}

	return nil
}
