package scheduler

import (
	"context"
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
	localStore map[string]*models.Task
	Ctx        context.Context
}

func New(conf *config.Config, store *store.Redis, ctx context.Context) *Scheduler {
	cron := gocron.NewScheduler(time.UTC)
	cron.WithDistributedLocker(*store.Locker)
	return &Scheduler{
		Cron:       cron,
		Store:      store,
		Config:     conf,
		localStore: make(map[string]*models.Task),
		Ctx:        ctx,
	}
}

func (s *Scheduler) Start() {
	go s.onExit()
	log.Debug().Msg("On cron start")
	s.Cron.StartBlocking()
}

func (s *Scheduler) Stop() {
	s.Store.Close()
	s.Cron.Stop()
}

func (s *Scheduler) setTask(t *models.Task) {
	log.Info().Msgf("Setting task: %s", t.Name)
	s.Cron.Every(t.Interval).Name(t.Name).Do(func() { t.Func() })
}

func (s *Scheduler) AddTask(t *models.Task) {
	s.setTask(t)
	s.localStore[t.Name] = t
}

func (s *Scheduler) AddTasks(tasks []*models.Task) {
	for _, t := range tasks {
		s.AddTask(t)
	}
}

func (s *Scheduler) RemoveTask(name string) {
	s.Cron.RemoveByTag(name)
	delete(s.localStore, name)
}

func (s *Scheduler) onExit() {
	exitSignal := make(chan os.Signal, 1)
	signal.Notify(exitSignal, os.Interrupt, syscall.SIGTERM)

	<-exitSignal
	log.Info().Msg("Shutting down proxy manager")
	s.Stop()
	os.Exit(0)
}
