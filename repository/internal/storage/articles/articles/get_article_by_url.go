package articles

import (
	"context"
	"errors"
	"fmt"
	"github.com/jackc/pgx/v5"
	"repository/internal/models/errs"
	articles2 "repository/internal/models/storage/articles/articles"
	"repository/internal/models/usecase/articles/articles"
)

func (i *Implementation) GetArticleByURL(ctx context.Context, url string) (articles.Article, error) {
	query := fmt.Sprintf("SELECT %s, %s, %s FROM %s WHERE %s = $1", articles2.TextField, articles2.DescriptionField, articles2.URLField, articles2.TableName, articles2.URLField)

	var result articles.Article

	err := i.conn.QueryRow(ctx, query, url).Scan(&result.Text, &result.Description, &result.URL)
	if errors.Is(err, pgx.ErrNoRows) {
		return articles.Article{}, errs.ErrArticleNotFound
	}

	if err != nil {
		return articles.Article{}, err
	}

	return result, nil
}
