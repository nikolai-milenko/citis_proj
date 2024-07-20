package blacklist

import (
	"encoding/json"
	"net/http"
	"repository/internal/models/handlers/articles/blacklist/add_hit"
)

func (i *Implementation) AddHit(w http.ResponseWriter, r *http.Request) {
	var req add_hit.AddHitRequest

	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest) // TODO нормальный хендлер ошибок
		_ = json.NewEncoder(w).Encode(add_hit.AddHitResponse{Error: err.Error()})
		return
	}

	err = i.manager.AddHit(r.Context(), req.URL)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError) // TODO нормальный хендлер ошибок
		_ = json.NewEncoder(w).Encode(add_hit.AddHitResponse{Error: err.Error()})
		return
	}

	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(add_hit.AddHitResponse{})
}
