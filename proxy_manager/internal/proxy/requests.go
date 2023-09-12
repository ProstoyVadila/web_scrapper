package proxy

// import "github.com/carlmjohnson/requests"

func (p *Proxy) GetProxy() (Proxy, error) {
	// res := requests.Requests().Get("https://api.getproxylist.com/proxy")
	return Proxy{}, nil
}

func (p *Proxy) CheckProxy(Proxy) (bool, error) {
	return false, nil
}

func (p *Proxy) AddProxy(Proxy) error {
	return nil
}
