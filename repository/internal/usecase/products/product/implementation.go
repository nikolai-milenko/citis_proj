package product

import (
	"context"
	"repository/internal/models/usecase/products/product"
)

type productsStorager interface {
	AddProduct(ctx context.Context, product product.Product) error
	GetURLs(ctx context.Context) ([]string, error)
	ProductExists(ctx context.Context, url string) (bool, error)
}

type Implementation struct {
	storager productsStorager
}

func NewImplementation(productsStorager productsStorager) *Implementation {
	return &Implementation{
		productsStorager,
	}
}
