package routines

import (
	"context"
	"proxy_manager/pkg/models"
	"proxy_manager/pkg/req"
	"proxy_manager/pkg/store"

	"github.com/rs/zerolog/log"
)

type GetProxiesTask struct {
	Task  *models.Task
	Proxy *models.Proxy
	req   *req.Request
	redis *store.Redis
}

func NewGetProxyTask(ctx context.Context, redis *store.Redis) *GetProxiesTask {
	request := req.New(ctx, "http://localhost:3000", new(models.Proxy))
	task := &GetProxiesTask{
		Task:  models.NewTask("get_new_proxies", "5s"),
		req:   request,
		redis: redis,
	}
	task.Task.SetFunc(task.Run)
	return task
}

func (t *GetProxiesTask) Run() {
	proxy, err := t.req.Get()
	if err != nil {
		log.Err(err).Str("url", t.req.BaseUrl).Msg("Failed to get proxy")
		return
	}
	t.Proxy = proxy.(*models.Proxy)
	log.Info().Msgf("Got proxy: %s", t.Proxy.String())

	log.Info().Msg("Creating identity")
	identity := models.NewIdentity(t.Proxy, 0)
	log.Info().Msgf("Identity: %s", identity.String())

	log.Info().Msg("Storing identity in redis")
	err = t.redis.Set(identity)
	if err != nil {
		log.Err(err).Msg("Failed to store identity in redis")
		return
	}
}
