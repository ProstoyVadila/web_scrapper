package routines

import (
	"context"
	"proxy_manager/pkg/models"
	"proxy_manager/pkg/req"
	"proxy_manager/pkg/store"

	"github.com/rs/zerolog/log"
)

type Routine interface {
	Run()
}

type ProxiesTask struct {
	Task  *models.TemplateTask
	Proxy *models.Proxy
	Req   *req.Request
	redis *store.Redis
}

func NewProxyTask(ctx context.Context, redis *store.Redis) *ProxiesTask {
	request := req.New(ctx, "http://localhost:3000", new(models.Proxy))
	proxyTask := &ProxiesTask{
		Task:  models.NewTask("get_new_proxies", "2s"),
		Req:   request,
		redis: redis,
	}
	proxyTask.SetFunc()
	return proxyTask
}

func (p *ProxiesTask) Run() {
	proxy, err := p.Req.Get()
	if err != nil {
		log.Err(err).Str("url", p.Req.BaseUrl).Msg("Failed to get proxy")
		return
	}
	p.Proxy = proxy.(*models.Proxy)
	log.Info().Msgf("Got proxy: %s", p.Proxy.String())

	log.Info().Msg("Creating identity")
	identity := models.NewIdentity(p.Proxy, 0)
	log.Info().Msgf("Identity: %s", identity.String())

	log.Info().Msg("Storing identity in redis")
	err = p.redis.Set(identity)
	if err != nil {
		log.Err(err).Msg("Failed to store identity in redis")
		return
	}
}

func (p *ProxiesTask) SetFunc() {
	p.Task.Func = p.Run
}
