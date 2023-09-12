package main

import (
	"proxy_manager/internal/conf"

	"github.com/rs/zerolog/log"
)

func main() {
	config := conf.New()
	conf.InitLogger(config)

	log.Debug().Interface("config", config).Msg("Config")

	server := New(config)
	server.ListenAndServe()
}
