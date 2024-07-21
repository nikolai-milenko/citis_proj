package blacklist

import "repository/internal/models/storage"

type Row struct {
	URL  string `db:"url"`
	Hits uint64 `db:"hits"`
}

const TableName storage.TableName = "articles.blacklist"

const (
	URLField  storage.FieldName = "url"
	HitsField storage.FieldName = "hits"
)
