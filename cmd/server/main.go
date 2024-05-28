package main

import (
	"log"
	"net/http"
	"openboard/internal/config"
	"openboard/internal/router"
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
