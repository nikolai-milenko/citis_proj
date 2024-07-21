package product

type Review struct {
	Review       string
	ReviewRating float32
}

type Product struct {
	URL     string
	Name    string
	Price   int
	Rating  float32
	Reviews []Review
}
