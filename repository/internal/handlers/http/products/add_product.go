package products

import (
	"encoding/json"
	"log"
	"net/http"
	"repository/internal/models/handlers/products/product"
	product2 "repository/internal/models/usecase/products/product"
)

func (i *Implementation) AddProducts(w http.ResponseWriter, r *http.Request) {
	var req product.AddProductsRequest

	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		log.Print(err)
		return
	}

	var convertedProducts []product2.Product
	for _, item := range req.Products {
		converted, err := ProductToDomain(item)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			json.NewEncoder(w).Encode(product.AddProductsResponse{Error: err.Error()})
			log.Print(err)
			return
		}

		convertedProducts = append(convertedProducts, converted)
	}

	err = i.manager.AddProducts(r.Context(), convertedProducts)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		json.NewEncoder(w).Encode(&product.AddProductsResponse{Error: err.Error()})
		log.Print(err)
		return
	}

	w.WriteHeader(http.StatusOK)
}
