package main

import (
	"fmt"

	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	r.GET("/ping", func(c *gin.Context) {
		fmt.Println("ping")
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})
	r.Run(":8080")
}
