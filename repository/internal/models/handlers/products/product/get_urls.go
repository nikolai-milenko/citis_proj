package product

type GetURLsResponse struct {
	Urls  []string `json:"urls"`
	Error string   `json:"error,omitempty"`
}
