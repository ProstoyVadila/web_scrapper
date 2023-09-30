package models

import (
	"bytes"
	"crypto/md5"
	"fmt"
	"reflect"
)

type Identity struct {
	Proxy *Proxy
	// Headers Headers
	Resource *Resource
	Hash     string
	Expiry   int64
}

type Headers struct {
	Accept         string `json:"accept"`
	AcceptEncoding string `json:"accept-encoding"`
	AcceptLanguage string `json:"accept-language"`
	Device         string `json:"device"`
}

func NewIdentity(proxy *Proxy, expiry int64) *Identity {
	identity := &Identity{
		Proxy:  proxy,
		Expiry: expiry,
	}
	// identity.SetHeaders(headers)
	identity.setHash()
	return identity
}

func NewHeaders(headers string) *Headers {
	return &Headers{}
}

func (i *Identity) String() string {
	return fmt.Sprintf(
		"IP: %s, Port: %d, Hash: %s Expity: %d",
		i.Proxy.IP,
		i.Proxy.Port,
		i.Hash,
		i.Expiry,
	)
}

// Fields returns field names of the structure
func (i *Identity) Fields() []string {
	fields := make([]string, 0)
	r := reflect.ValueOf(i).Elem()
	for i := 0; i < r.NumField(); i++ {
		fields = append(fields, r.Type().Field(i).Name)
	}
	return fields
}

// Values returns field values of the structure
func (i *Identity) Values() []string {
	values := make([]string, 0)
	r := reflect.ValueOf(i).Elem()
	for i := 0; i < r.NumField(); i++ {
		values = append(values, r.Field(i).String())
	}
	return values
}

func (i *Identity) bytes() []byte {
	buf := bytes.Buffer{}
	for _, value := range i.Values() {
		buf.WriteString(value)
	}
	return buf.Bytes()
}

func (i *Identity) hash() string {
	hash := md5.Sum(i.bytes())
	return fmt.Sprintf("%x", hash)
}

func (i *Identity) setHash() {
	i.Hash = i.hash()
}
