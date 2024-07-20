package blacklist

import (
	"context"
	"errors"
	"repository/internal/models/errs"
)

func (i *Implementation) AddHit(ctx context.Context, url string) error {
	_, err := i.storager.GetURLInfo(ctx, url)
	switch {
	case errors.Is(err, errs.ErrURLNotFound):
		err = i.storager.AddURL(ctx, url)
		if err != nil {
			return err
		}
	case err != nil:
		return err
	}

	err = i.storager.AddHit(ctx, url)
	if err != nil {
		return err
	}

	return nil
}
