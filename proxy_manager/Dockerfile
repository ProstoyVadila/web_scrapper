FROM golang:1.21.1-alpine3.17 AS builder
WORKDIR /app
COPY . .
RUN env GOOS=linux CGO_ENABLED=0 go build -ldflags "-w" -o main ./cmd/api

FROM alpine:latest 
WORKDIR /app
COPY --from=builder /app/main .
COPY .env .

CMD ["/app/main"]
