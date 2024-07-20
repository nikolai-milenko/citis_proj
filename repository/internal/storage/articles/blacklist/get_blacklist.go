package blacklist

import (
	"context"
	"errors"
	"fmt"
	"github.com/jackc/pgx/v5"
	"repository/internal/models/errs"
	storage_models "repository/internal/models/storage/articles/blacklist"
	usecase_models "repository/internal/models/usecase/articles/blacklist"
)

func (i *Implementation) GetURLInfo(ctx context.Context, url string) (usecase_models.URL, error) {
	query := fmt.Sprintf("SELECT (%s), (%s) FROM %s WHERE (%s) = $1", storage_models.URLField, storage_models.HitsField, storage_models.TableName, storage_models.URLField)

	var foundURL storage_models.Row

	err := i.conn.QueryRow(ctx, query, url).Scan(&foundURL.URL, &foundURL.Hits)
	if errors.Is(err, pgx.ErrNoRows) {
		return usecase_models.URL{}, errs.ErrURLNotFound
	}

	if err != nil {
		return usecase_models.URL{}, err
	}

	return usecase_models.URL{
		URL:  foundURL.URL,
		Hits: foundURL.Hits,
	}, nil
}
