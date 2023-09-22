package store

import (
	"context"
	"encoding/json"
	"proxy_manager/internal/config"
	"proxy_manager/pkg/models"
	"time"

	"github.com/go-co-op/gocron"
	redislock "github.com/go-co-op/gocron-redis-lock"
	"github.com/redis/go-redis/v9"
	"github.com/rs/zerolog/log"
)

type IdentityStore interface {
	Set(identity *models.Identity) error
	Get(key string) (*models.Identity, error)
}

type Redis struct {
	Client *redis.Client
	Locker *gocron.Locker
	ctx    context.Context
}

func NewRedis(ctx context.Context, conf *config.Config) *Redis {
	redisOptions := &redis.Options{
		Addr:     conf.RedisAddr(),
		Password: conf.RedisPassword,
	}
	redisClient := redis.NewClient(redisOptions)

	log.Debug().Msg("Configuring redis locker")
	locker, err := redislock.NewRedisLocker(redisClient, redislock.WithTries(10))
	if err != nil {
		log.Fatal().Err(err).Msg("Failed to create redis locker")
	}
	return &Redis{
		Client: redisClient,
		Locker: &locker,
		ctx:    ctx,
	}
}

func (r *Redis) Close() error {
	log.Info().Msg("Closing redis connection")
	return r.Client.Close()
}

func (r *Redis) Ping() error {
	log.Info().Msg("Pinging redis")
	_, err := r.Client.Ping(r.ctx).Result()
	return err
}

func (r *Redis) Set(identity *models.Identity) error {
	value, err := json.Marshal(identity)
	if err != nil {
		log.Err(err).Msg("Failed to marshal identity")
		return err
	}
	return r.Client.Set(r.ctx, identity.Hash, value, time.Duration(identity.Expiry)).Err()
}

func (r *Redis) Get(key string) (*models.Identity, error) {
	identity := new(models.Identity)
	value, err := r.Client.Get(r.ctx, key).Result()
	if err != nil {
		log.Err(err).Msg("Failed to get identity from redis")
		return nil, err
	}
	err = json.Unmarshal([]byte(value), &identity)
	if err != nil {
		log.Err(err).Msg("Failed to unmarshal identity")
		return nil, err
	}
	return identity, nil
}

func (r *Redis) Delete(key string) error {
	log.Info().Str("key", key).Msg("Deleting identity from redis")
	return r.Client.Del(r.ctx, key).Err()
}
