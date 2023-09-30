package store

import (
	"context"
	"encoding/json"
	"math/rand"
	"proxy_manager/internal/config"
	"proxy_manager/pkg/models"
	"time"

	"github.com/go-co-op/gocron"
	redislock "github.com/go-co-op/gocron-redis-lock"
	"github.com/redis/go-redis/v9"
	"github.com/rs/zerolog/log"
)

const (
	minRetryDelayMilliSec = 50
	maxRetryDelayMilliSec = 250
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

	redis := &Redis{
		Client: redisClient,
		ctx:    ctx,
	}
	redis.setRedisLocker()
	return redis
}

func (r *Redis) setRedisLocker() {
	log.Info().Msg("Configuring redis locker")
	for {
		locker, err := redislock.NewRedisLocker(
			r.Client,
			redislock.WithTries(10),
			redislock.WithDriftFactor(0.03),
			redislock.WithRetryDelay(5*time.Second),
			// redislock.WithExpiry(10*time.Second),
			redislock.WithTimeoutFactor(0.5),
			redislock.WithRetryDelayFunc(r.RetryDelayFunc),
		)
		if err != nil {
			log.Err(err).Msg("Failed to create redis locker. Trying again in 5 seconds")
			time.Sleep(5 * time.Second)
			continue
		} else {
			r.Locker = &locker
			break
		}
	}
}

func (r *Redis) RetryDelayFunc(tries int) time.Duration {
	// TODO: add alerting
	delay := time.Duration(rand.Intn(maxRetryDelayMilliSec-minRetryDelayMilliSec)+minRetryDelayMilliSec) * time.Millisecond
	log.Info().Msgf("Retry to connect to Redis. Tries: %d. Delay: %s", tries, delay.String())
	return delay
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

// TODO: check if this is the best way to get all identities
func (r *Redis) GetAll() ([]*models.Identity, error) {
	log.Info().Msg("Getting all identities from redis")
	keys, err := r.Client.Keys(r.ctx, "*").Result()
	if err != nil {
		log.Err(err).Msg("Failed to get keys from redis")
		return nil, err
	}
	identities := make([]*models.Identity, 0)
	for _, key := range keys {
		identity, err := r.Get(key)
		if err != nil {
			log.Err(err).Msg("Failed to get identity from redis")
			return nil, err
		}
		identities = append(identities, identity)
	}
	return identities, nil
}

func (r *Redis) GetRotten() {

}

func (r *Redis) randomFromKeys(keys []string) string {
	return keys[rand.Intn(len(keys))]
}

// TODO: check if this is the best way to get random identity
func (r *Redis) GetRandom(numOfRecords int) ([]*models.Identity, error) {
	log.Info().Msg("Getting random identity from redis")
	keys, err := r.Client.Keys(r.ctx, "*").Result()
	if err != nil {
		log.Err(err).Msg("Failed to get keys from redis")
		return nil, err
	}
	if len(keys) == 0 {
		log.Warn().Msg("No keys found in redis")
		// TODO: return error
		return nil, nil
	}

	var identities []*models.Identity
	for i := 0; i < numOfRecords; i++ {
		key := r.randomFromKeys(keys)
		identity, err := r.Get(key)
		if err != nil {
			log.Err(err).Msg("Failed to get identity from redis")
			return nil, err
		}
		identities = append(identities, identity)
	}

	return identities, nil
}

func (r *Redis) Delete(key string) error {
	log.Info().Str("key", key).Msg("Deleting identity from redis")
	return r.Client.Del(r.ctx, key).Err()
}
