package scheduler

import (
	"os"
	"os/signal"
	"proxy_manager/internal/config"
	"proxy_manager/pkg/models"
	"proxy_manager/pkg/store"
	"syscall"
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
		Cron:       cron,
		Store:      store,
		Config:     conf,
		localStore: make(map[string]*models.Identity),
	}
}

func (s *Scheduler) Start() {
	go s.onExit()
	s.Cron.StartBlocking()
}

func (s *Scheduler) Stop() {
	s.Store.Close()
	s.Cron.Stop()
}

func (s *Scheduler) AddTask(t *models.Task) {
	s.Cron.Every(t.Interval).Name(t.Name).Do(t.Func)
}

func (s *Scheduler) AddTasks(tasks []*models.Task) {
	for _, t := range tasks {
		s.AddTask(t)
	}
}

func (s *Scheduler) RemoveTask(name string) {
	s.Cron.RemoveByTag(name)
}

func (s *Scheduler) onExit() {
	exitSignal := make(chan os.Signal, 1)
	signal.Notify(exitSignal, os.Interrupt, syscall.SIGTERM)

	<-exitSignal
	log.Info().Msg("Shutting down proxy manager")
	s.Stop()
	os.Exit(0)
}
