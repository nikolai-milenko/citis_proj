package articles

import (
	"context"
	"fmt"
	storage_models "repository/internal/models/storage/articles/articles"
)

func (i *Implementation) DeleteArticleByURL(ctx context.Context, url string) error {
	query := fmt.Sprintf("DELETE FROM %s WHERE %s = $1", storage_models.TableName, storage_models.URLField)

	_, err := i.conn.Exec(ctx, query, url)
	if err != nil {
		return err
	}

	return nil
}
