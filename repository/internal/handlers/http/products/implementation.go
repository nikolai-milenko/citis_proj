package products

import (
	"context"
	"repository/internal/models/usecase/products/product"
)

type productsManager interface {
	AddProducts(ctx context.Context, products []product.Product) error
	GetUrls(ctx context.Context) ([]string, error)
}

type Implementation struct {
	manager productsManager
}

func NewImplementation(manager productsManager) *Implementation {
	return &Implementation{
		manager: manager,
	}
}
