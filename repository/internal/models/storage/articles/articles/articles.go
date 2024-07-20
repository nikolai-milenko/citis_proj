package articles

import "repository/internal/models/storage"

type Row struct {
	URL         string `db:"url"`
	Text        string `db:"text"`
	Description string `db:"description"`
}

const TableName storage.TableName = "articles.articles"

const (
	URLField         storage.FieldName = "url"
	TextField        storage.FieldName = "text"
	DescriptionField storage.FieldName = "description"
)
