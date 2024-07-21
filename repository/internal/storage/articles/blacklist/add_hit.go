package blacklist

import (
	"context"
	"fmt"
	storage_models "repository/internal/models/storage/articles/blacklist"
)

func (i *Implementation) AddHit(ctx context.Context, url string) error {
	query := fmt.Sprintf("UPDATE %s SET %s = %s + 1 WHERE %s = $1", storage_models.TableName, storage_models.HitsField, storage_models.HitsField, storage_models.URLField)

	_, err := i.conn.Exec(ctx, query, url)
	if err != nil {
		return err
	}

	return err
}
