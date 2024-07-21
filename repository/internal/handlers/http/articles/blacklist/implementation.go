package blacklist

import (
	"context"
	usecase_models "repository/internal/models/usecase/articles/blacklist"
)

type blacklistManager interface {
	AddHit(ctx context.Context, url string) error
	GetURLInfo(ctx context.Context, url string) (usecase_models.URL, error)
	//AddURL(ctx context.Context, url string) error
}

type Implementation struct {
	manager blacklistManager
}

func NewImplementation(manager blacklistManager) *Implementation {
	return &Implementation{manager: manager}
}
