package routines

import (
	"proxy_manager/internal/scheduler"
	"proxy_manager/pkg/models"
)

type Routine interface {
	Run(s *scheduler.Scheduler)
}

type GetProxiesTask struct {
	*models.Task
	Source string
}

func (g *GetProxiesTask) Run(s *scheduler.Scheduler) {
}
