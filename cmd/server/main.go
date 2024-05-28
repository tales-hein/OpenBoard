package main

import (
	"log"
	"myapp/internal/config"
	"myapp/internal/router"
	"net/http"
)

func main() {
	cfg, err := config.LoadConfig()
	if err != nil {
		log.Fatalf("Could not load configuration: %v", err)
	}

	r := router.NewRouter()

	log.Printf("Starting server on port %s", cfg.Port)
	if err := http.ListenAndServe(":"+cfg.Port, r); err != nil {
		log.Fatalf("Could not start server: %v", err)
	}
}
