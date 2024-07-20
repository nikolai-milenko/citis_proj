package products

import (
	"repository/internal/models/handlers/products/product"
	product2 "repository/internal/models/usecase/products/product"
	"strconv"
)

func ProductToDomain(product product.Product) (product2.Product, error) {
	var reviews []product2.Review

	for _, review := range product.Reviews {
		var (
			rating float64
			err    error
		)

		if len(review.ReviewRating) != 0 {
			rating, err = strconv.ParseFloat(review.ReviewRating, 32)
			if err != nil {
				return product2.Product{}, err
			}
		}

		reviews = append(reviews, product2.Review{
			Review:       review.Review,
			ReviewRating: float32(rating),
		})
	}

	var (
		price int
		err   error
	)

	if len(product.Price) != 0 {
		price, err = strconv.Atoi(product.Price)
		if err != nil {
			return product2.Product{}, err
		}
	}

	var (
		rating float64
	)

	if len(product.Rating) != 0 {
		rating, err = strconv.ParseFloat(product.Rating, 32)
		if err != nil {
			return product2.Product{}, err
		}
	}

	return product2.Product{
		URL:     product.URL,
		Name:    product.Name,
		Price:   price,
		Rating:  float32(rating),
		Reviews: reviews,
	}, nil
}
