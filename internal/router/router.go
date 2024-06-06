package router

import (
	"openboard/internal/handler"

	"github.com/gorilla/mux"
)

func NewRouter() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/", handler.HomeHandler).Methods("GET")
	r.HandleFunc("/repo", handler.RepoHandler).Methods("GET")
	r.HandleFunc("/route/{routeId}", handler.RouteHandler).Methods("GET")
	r.HandleFunc("/creation", handler.CreationHandler).Methods("GET")
	return r
}
