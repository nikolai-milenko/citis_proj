package articles

import (
	"encoding/json"
	"errors"
	"net/http"
	"repository/internal/models/errs"
	"repository/internal/models/handlers/articles/articles/add_article"
)

func (i *Implementation) AddArticle(w http.ResponseWriter, r *http.Request) {
	var req add_article.AddArticleRequest

	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		return
	}

	err = i.manager.AddArticle(r.Context(), req.Articles)
	if errors.Is(err, errs.ErrArticleAlreadyExists) {
		w.WriteHeader(http.StatusConflict)
		_ = json.NewEncoder(w).Encode(add_article.AddArticleResponse{Error: err.Error()})
		return
	}

	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
}
