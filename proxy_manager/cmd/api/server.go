package main

import (
	"fmt"
	"proxy_manager/internal/conf"

	"github.com/gin-gonic/gin"
	"github.com/rs/zerolog/log"
)

type Server struct {
	// store db.Store
	*gin.Engine
	Config *conf.Config
}

func New(config *conf.Config) *Server {
	server := &Server{
		Engine: gin.New(),
		Config: config,
	}

	server.setRouters()
	return server
}

func (s *Server) ListenAndServe() {
	log.Info().Msg("Starting server...")
	s.Run(s.apiUrl())
}

func (s *Server) apiUrl() string {
	return fmt.Sprintf(":%s", s.Config.ApiPort)
}
