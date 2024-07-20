package blacklist

import (
	"encoding/json"
	"log"
	"net/http"
	"repository/internal/models/handlers/articles/blacklist/get_url_info"
)

func (i *Implementation) GetURLInfo(w http.ResponseWriter, r *http.Request) {
	var req get_url_info.GetURLInfoRequest

	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest) // TODO нормальный хендлер ошибок
		_ = json.NewEncoder(w).Encode(get_url_info.GetURLInfoResponse{Error: err.Error()})
		return
	}

	res, err := i.manager.GetURLInfo(r.Context(), req.URL)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError) // TODO нормальный хендлер ошибок
		_ = json.NewEncoder(w).Encode(get_url_info.GetURLInfoResponse{Error: err.Error()})
		return
	}

	//w.WriteHeader(http.StatusOK)
	encoder := json.NewEncoder(w)

	err = encoder.Encode(&get_url_info.GetURLInfoResponse{
		Hits: res.Hits,
	})
	if err != nil {
		log.Print(err)
	}
}
