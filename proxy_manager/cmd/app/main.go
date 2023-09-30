package main

import (
	"context"
	"os"
	"proxy_manager/internal/config"

	"proxy_manager/internal/routines"
	"proxy_manager/internal/scheduler"
	"proxy_manager/pkg/store"

	"github.com/rs/zerolog/log"
)

var ctx = context.Background()

func init() {
	config.InitLogger(os.Getenv("LOG_LEVEL"))
}

func main() {
	log.Info().Msg("Starting proxy manager")

	log.Info().Msg("Loading config")
	conf := config.New()

	log.Info().Msg("Connecting to redis")
	redis := store.NewRedis(ctx, conf)

	log.Info().Msg("Starting cron scheduler")
	s := scheduler.New(conf, redis, ctx)

	log.Info().Msg("Adding tasks")
	tasks := routines.GetAll(ctx, redis)
	s.AddTasks(tasks)

	s.Start()
}
