package conf

import (
	"log"

	"github.com/rs/zerolog"
	"github.com/spf13/viper"
)

type Config struct {
	GinMode       string `env:"GIN_MODE" envDefault:"debug" mapstructure:"GIN_MODE"`
	LogLevel      string `env:"LOG_LEVEL" envDefault:"debug" mapstructure:"LOG_LEVEL"`
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

func InitLogger(config *Config) {
	// logLevel, err := zerolog.ParseLevel(config.LogLevel)
	// if err != nil {
	// 	log.Fatal(err)
	// }
	zerolog.SetGlobalLevel(zerolog.DebugLevel)
}
