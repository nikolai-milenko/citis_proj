package articles

import "context"

func (i *Implementation) DeleteArticleByURL(ctx context.Context, url string) error {
	err := i.storager.DeleteArticleByURL(ctx, url)
	if err != nil {
		return err
	}

	return nil
}
