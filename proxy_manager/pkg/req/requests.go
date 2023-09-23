package req

import (
	"context"

	"github.com/carlmjohnson/requests"
	"github.com/rs/zerolog/log"
)

type Requester interface {
	Get() (interface{}, error)
}

type Request struct {
	ctx     context.Context
	BaseUrl string
	Result  interface{}
}

func New(ctx context.Context, baseUrl string, respModel interface{}) *Request {
	return &Request{
		ctx:     ctx,
		BaseUrl: baseUrl,
		Result:  respModel,
	}
}

func (r *Request) doRequest() error {
	err := requests.URL(r.BaseUrl).CheckStatus(200).ToJSON(r.Result).Fetch(r.ctx)
	if err != nil {
		log.Err(err).Msg("Failed to fetch url")
		return err
	}
	return nil
}

func (r *Request) Get() (interface{}, error) {
	err := r.doRequest()
	if err != nil {
		return nil, err
	}
	return r.Result, nil
}
