package blacklist

import (
	"context"
	usecase_models "repository/internal/models/usecase/articles/blacklist"
)

type blacklistStorager interface {
	AddHit(ctx context.Context, url string) error
	GetURLInfo(ctx context.Context, url string) (usecase_models.URL, error)
	AddURL(ctx context.Context, url string) error
}

type Implementation struct {
	storager blacklistStorager
}

func NewImplementation(storager blacklistStorager) *Implementation {
	return &Implementation{storager: storager}
}
