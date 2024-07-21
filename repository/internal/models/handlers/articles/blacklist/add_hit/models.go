package add_hit

type AddHitRequest struct {
	URL string `json:"url"`
}

type AddHitResponse struct {
	Error string `json:"error,omitempty"`
}
