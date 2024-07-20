package blacklist

import (
	"context"
	"errors"
	"repository/internal/models/errs"
	usecase_models "repository/internal/models/usecase/articles/blacklist"
)

func (i *Implementation) GetURLInfo(ctx context.Context, url string) (usecase_models.URL, error) {
	found, err := i.storager.GetURLInfo(ctx, url)
	if err != nil && !errors.Is(err, errs.ErrURLNotFound) {
		return usecase_models.URL{}, err
	}

	return found, nil
}
