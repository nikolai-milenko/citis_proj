package get_url_info

type GetURLInfoRequest struct {
	URL string `json:"url"`
}

type GetURLInfoResponse struct {
	Hits  uint64 `json:"hits"`
	Error string `json:"error,omitempty"`
}
