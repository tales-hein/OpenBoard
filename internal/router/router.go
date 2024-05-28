package router

import (
	"openboard/internal/handler"

	"github.com/gorilla/mux"
)

func NewRouter() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/", handler.HomeHandler).Methods("GET")
	return r
}
