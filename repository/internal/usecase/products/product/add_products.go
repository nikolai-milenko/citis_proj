package product

import (
	"context"
	product2 "repository/internal/models/usecase/products/product"
)

func (i *Implementation) AddProducts(ctx context.Context, products []product2.Product) error {
	for _, product := range products {
		ok, err := i.storager.ProductExists(ctx, product.URL)
		if err != nil {
			return err
		}

		if ok {
			continue
		}

		if err = i.storager.AddProduct(ctx, product); err != nil {
			return err
		}
	}

	return nil
}
