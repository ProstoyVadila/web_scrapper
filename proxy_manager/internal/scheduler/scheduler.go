package scheduler

import (
	"proxy_manager/internal/config"
	"proxy_manager/pkg/models"
	"proxy_manager/pkg/store"
	"time"

	"github.com/go-co-op/gocron"
	"github.com/rs/zerolog/log"
)

type Scheduler struct {
	Cron       *gocron.Scheduler
	Store      *store.Redis
	Config     *config.Config
	localStore map[string]*models.Identity
}

func New(conf *config.Config, store *store.Redis) *Scheduler {
	cron := gocron.NewScheduler(time.UTC)
	cron.WithDistributedLocker(*store.Locker)
	return &Scheduler{
		Cron:       gocron.NewScheduler(time.UTC),
		Store:      store,
		Config:     conf,
		localStore: make(map[string]*models.Identity),
	}
}

func (s *Scheduler) Start() {
	for {
		if err := s.Store.Ping(); err != nil {
			log.Error().Err(err).Msg("Failed to ping storage. Retrying in 5 seconds")
			time.Sleep(5 * time.Second)
			continue
		}
		break
	}
	s.Cron.StartAsync()
}
