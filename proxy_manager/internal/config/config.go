package config

import (
	"fmt"
	"log"

	"github.com/rs/zerolog"
	"github.com/spf13/viper"
)

type Config struct {
	RedisHost     string `env:"REDIS_HOST" envDefault:"redis" mapstructure:"REDIS_HOST"`
	RedisPassword string `env:"REDIS_PASSWORD" envDefault:"" mapstructure:"REDIS_PASSWORD"`
	RedisPort     string `env:"REDIS_PORT" envDefault:"6379" mapstructure:"REDIS_PORT"`
	ApiPort       string `env:"API_PORT" envDefault:"8080" mapstructure:"API_PORT"`
}

func New() (config *Config) {
	viper.AutomaticEnv()
	viper.SetConfigFile(".env")

	if err := viper.ReadInConfig(); err != nil {
		log.Fatal(err)
	}
	err := viper.Unmarshal(&config)
	if err != nil {
		log.Fatal(err)
	}
	return
}

func (c *Config) RedisAddr() string {
	return fmt.Sprintf("%s:%s", c.RedisHost, c.RedisPort)
}

func InitLogger(logLevel string) {
	if logLevel == "" {
		logLevel = "debug"
	}
	level, err := zerolog.ParseLevel(logLevel)
	if err != nil {
		log.Fatal(err)
	}
	zerolog.SetGlobalLevel(level)
}
