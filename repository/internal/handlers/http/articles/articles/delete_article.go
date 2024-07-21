package articles

import (
	"encoding/json"
	"net/http"
	"repository/internal/models/handlers/articles/articles/delete_article"
)

func (i *Implementation) DeleteArticle(w http.ResponseWriter, r *http.Request) {
	var req delete_article.DeleteArticleRequest

	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		return
	}

	err = i.manager.DeleteArticleByURL(r.Context(), req.URL)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		_ = json.NewEncoder(w).Encode(delete_article.DeleteArticleResponse{Error: err.Error()})
	}

	w.WriteHeader(http.StatusOK)
}
