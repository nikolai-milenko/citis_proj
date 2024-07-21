package product

import "context"

func (i *Implementation) GetUrls(ctx context.Context) ([]string, error) {
	urls, err := i.storager.GetURLs(ctx)
	if err != nil {
		return nil, err
	}

	return urls, nil
}
