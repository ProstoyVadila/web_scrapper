package proxy

type Proxy struct {
	Ip   string `json:"ip"`
	Port string `json:"port"`
}

type ProxyInfo struct {
	Proxy
	Protocol    string `json:"protocol"`
	Anonymity   string `json:"anonymity"`
	Country     string `json:"country"`
	FromService string `json:"from_service"`
}

type ProxyManager interface {
	GetProxy() (Proxy, error)
	CheckProxy(Proxy) (bool, error)
	AddProxy(Proxy) error
}

func New() ProxyManager {
	return &ProxyInfo{}
}
