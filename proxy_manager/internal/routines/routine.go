package routines

import "proxy_manager/pkg/models"

type Routine interface {
	Run()
}

type GetProxiesTask struct {
	*models.Task
	Source string
}

func (g *GetProxiesTask) Run() {
}
