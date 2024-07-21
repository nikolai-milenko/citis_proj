package products

import (
	"encoding/json"
	"net/http"
	"repository/internal/models/handlers/products/product"
)

func (i *Implementation) GetUrls(w http.ResponseWriter, r *http.Request) {

	urls, err := i.manager.GetUrls(r.Context())
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		json.NewEncoder(w).Encode(product.GetURLsResponse{Error: err.Error()})
		return
	}

	json.NewEncoder(w).Encode(product.GetURLsResponse{
		Urls: urls,
	})
	w.WriteHeader(http.StatusOK)
}
