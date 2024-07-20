package delete_article

type DeleteArticleRequest struct {
	URL string `json:"url"`
}

type DeleteArticleResponse struct {
	Error string `json:"error,omitempty"`
}
