package routines

import (
	"context"
	"proxy_manager/pkg/models"
	"proxy_manager/pkg/store"
)

type Routine interface {
	Run()
}

func GetAll(ctx context.Context, redis *store.Redis) []*models.Task {
	return []*models.Task{
		NewGetProxyTask(ctx, redis).Task,
		NewCheckProxyTask(redis).Task,
	}
}
