package models

import (
	"encoding/json"
	"reflect"

	"github.com/rs/zerolog/log"
)

type Identity struct {
	Headers  Headers
	Addr     string
	Password string
	Hash     string
	Expiry   int64
}

type Headers struct {
	Accept         string `json:"accept"`
	AcceptEncoding string `json:"accept-encoding"`
	AcceptLanguage string `json:"accept-language"`
	Device         string `json:"device"`
}

func NewIdentity(addr, password, headers, hash string) *Identity {
	identity := &Identity{
		Addr:     addr,
		Password: password,
		Hash:     hash,
	}
	identity.SetHeaders(headers)
	return identity
}

func NewHeaders(headers string) *Headers {
	return &Headers{}
}

func (i *Identity) SetHeaders(headers string) {
	err := json.Unmarshal([]byte(headers), &i.Headers)
	if err != nil {
		log.Err(err).Msg("Failed to unmarshal headers")
	}
}

func (i *Identity) Fields() []string {
	values := make([]string, 0)
	r := reflect.ValueOf(i).Elem()
	for i := 0; i < r.NumField(); i++ {
		values = append(values, r.Field(i).String())
	}
	return values
}
