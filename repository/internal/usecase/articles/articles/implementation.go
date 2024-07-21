package articles

import (
	"context"
	"repository/internal/models/usecase/articles/articles"
)

type articlesStorager interface {
	AddArticle(ctx context.Context, url string, description string, text string) error
	DeleteArticleByURL(ctx context.Context, url string) error
	GetArticleByURL(ctx context.Context, url string) (articles.Article, error)
}

type Implementation struct {
	storager articlesStorager
}

func NewImplementation(storager articlesStorager) *Implementation {
	return &Implementation{storager: storager}
}
