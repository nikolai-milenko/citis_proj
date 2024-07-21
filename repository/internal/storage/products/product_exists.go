package products

import (
	"context"
	"errors"
	"fmt"
	"github.com/jackc/pgx/v5"
	product2 "repository/internal/models/storage/products/product"
)

func (i *Implementation) ProductExists(ctx context.Context, url string) (bool, error) {
	query := fmt.Sprintf("SELECT id FROM %s WHERE %s = $1", product2.ProductsTableName, product2.ProductsURLField)

	var id int

	err := i.conn.QueryRow(ctx, query, url).Scan(&id)
	if errors.Is(err, pgx.ErrNoRows) {
		return false, nil
	}

	if err != nil {
		return false, err
	}

	return true, nil
}
