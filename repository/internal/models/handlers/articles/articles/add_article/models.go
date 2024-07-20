package add_article

type AddArticleRequest struct {
	Articles []Article `json:"articles"`
}

type AddArticleResponse struct {
	Error string `json:"error,omitempty"`
}

type Article struct {
	URL         string `json:"url"`
	Text        string `json:"text"`
	Description string `json:"description"`
}
