package routines

import (
	"proxy_manager/pkg/models"
	"proxy_manager/pkg/store"

	"github.com/rs/zerolog/log"
)

type CheckProxyTask struct {
	Task  *models.Task
	Proxy *models.Proxy
	redis *store.Redis
}

func NewCheckProxyTask(redis *store.Redis) *CheckProxyTask {
	task := &CheckProxyTask{
		Task:  models.NewTask("check_proxy", "5s"),
		redis: redis,
	}
	task.Task.SetFunc(task.Run)
	return task
}

func (t *CheckProxyTask) Run() {
	// proxy, err := p.redis.Get()
	// if err != nil {
	// 	log.Err(err).Msg("Failed to get proxy from redis")
	// 	return
	// }
	// p.Proxy = proxy
	// log.Info().Msgf("Got proxy: %s", p.Proxy.String())

	// log.Info().Msg("Creating identity")
	// identity := models.NewIdentity(p.Proxy, 0)
	// log.Info().Msgf("Identity: %s", identity.String())

	// log.Info().Msg("Storing identity in redis")
	// err = p.redis.Set(identity)
	// if err != nil {
	// 	log.Err(err).Msg("Failed to store identity in redis")
	// 	return
	// }
	identities, err := t.redis.GetRandom(10)
	if err != nil {
		log.Err(err).Msg("Failed to get random identity from redis")
		return
	}
	for _, identity := range identities {
		log.Info().Msgf("Checking random identity: %s", identity.String())
	}
	// request := req.New(context.Background(), identity.Resource.Url, new(models.Proxy))
	// proxy, err := request.Get()
	// if err != nil {
	// 	log.Err(err).Msg("Failed to get proxy")
	// 	return
	// }
	// log.Info().Msgf("Got proxy: %s", proxy.(*models.Proxy).String())
}
