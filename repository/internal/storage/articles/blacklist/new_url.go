package blacklist

import (
	"context"
	"fmt"
	storage_models "repository/internal/models/storage/articles/blacklist"
)

func (i *Implementation) AddURL(ctx context.Context, url string) error {
	query := fmt.Sprintf("INSERT INTO %s (%s) VALUES ($1)", storage_models.TableName, storage_models.URLField)

	_, err := i.conn.Exec(ctx, query, url)
	if err != nil {
		return err
	}

	return nil
}
