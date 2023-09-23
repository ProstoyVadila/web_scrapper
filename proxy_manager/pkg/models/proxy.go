package models

import "strconv"

type Proxy struct {
	IP   string `json:"ip"`
	Port int    `json:"port"`
}

func (p *Proxy) String() string {
	return p.IP + ":" + strconv.Itoa(p.Port)
}
