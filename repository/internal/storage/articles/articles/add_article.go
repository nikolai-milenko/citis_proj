package articles

import (
	"context"
	"fmt"
	storage_models "repository/internal/models/storage/articles/articles"
)

func (i *Implementation) AddArticle(ctx context.Context, url string, description string, text string) error {
	query := fmt.Sprintf("INSERT INTO %s (%s, %s, %s) VALUES ($1, $2, $3)", storage_models.TableName, storage_models.TextField, storage_models.URLField, storage_models.DescriptionField)

	_, err := i.conn.Exec(ctx, query, text, url, description)
	if err != nil {
		return err
	}

	return nil
}
