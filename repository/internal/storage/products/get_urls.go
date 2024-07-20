package products

import (
	"context"
	"errors"
	"fmt"
	"github.com/jackc/pgx/v5"
	product2 "repository/internal/models/storage/products/product"
)

func (i *Implementation) GetURLs(ctx context.Context) ([]string, error) {
	query := fmt.Sprintf("SELECT %s FROM %s", product2.ProductsURLField, product2.ProductsTableName)

	rows, err := i.conn.Query(ctx, query)
	if errors.Is(err, pgx.ErrNoRows) {
		return nil, nil
	}

	if err != nil || rows.Err() != nil {
		return nil, err
	}

	var urls []string
	for rows.Next() {
		var url string
		if err := rows.Scan(&url); err != nil {
			return nil, err
		}
		urls = append(urls, url)
	}

	return urls, nil
}
