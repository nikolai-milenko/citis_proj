package articles

import (
	"context"
	"repository/internal/models/handlers/articles/articles/add_article"
)

func (i *Implementation) AddArticle(ctx context.Context, articles []add_article.Article) error {
	for _, article := range articles {
		_, err := i.storager.GetArticleByURL(ctx, article.URL)
		if err == nil {
			continue
		}

		err = i.storager.AddArticle(ctx, article.URL, article.Description, article.Text)
		if err != nil {
			return err
		}

	}

	return nil
}
