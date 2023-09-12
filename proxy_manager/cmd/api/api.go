package main

import "github.com/gin-gonic/gin"

func (s *Server) setRouters() {
	s.GET("/ping", s.ping)
	s.GET("/getProxy", s.getProxy)
	s.GET("/checkProxy", s.checkProxy)
	s.POST("/addProxy", s.addProxy)
}

func (s *Server) send(ctx *gin.Context, message string, status int) {
	ctx.JSON(200, gin.H{
		"message": message,
	})
}

func (s *Server) ping(ctx *gin.Context) {
	s.send(ctx, "pong", 200)
}

func (s *Server) getProxy(ctx *gin.Context) {
	s.send(ctx, "getProxy", 200)
}

func (s *Server) checkProxy(ctx *gin.Context) {
	s.send(ctx, "checkProxy", 200)
}

func (s *Server) addProxy(ctx *gin.Context) {
	s.send(ctx, "addProxy", 200)
}
