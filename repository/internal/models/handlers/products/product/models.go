package product

type AddProductsRequest struct {
	Products []Product `json:"products"`
}

type AddProductsResponse struct {
	Error string `json:"error"`
}

type Review struct {
	Review       string `json:"review"`
	ReviewRating string `json:"review_rating"`
}

type Product struct {
	URL     string   `json:"url"`
	Name    string   `json:"name"`
	Price   string   `json:"price"`
	Rating  string   `json:"rating"`
	Reviews []Review `json:"reviews"`
}
