package articles

import (
	"context"
	"repository/internal/models/handlers/articles/articles/add_article"
)

type articlesManager interface {
	AddArticle(ctx context.Context, articles []add_article.Article) error
	DeleteArticleByURL(ctx context.Context, url string) error
}

type Implementation struct {
	manager articlesManager
}

func NewImplementation(manager articlesManager) *Implementation {
	return &Implementation{manager: manager}
}
