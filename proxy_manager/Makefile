
run:
	@LOG_LEVEL=debug go run ./cmd/app

build:
	@go build -o bin/main ./cmd/app

tests:
	@go test -v -cover ./...

mock:
	bun mock/proxy.js

.PHONY: run build tests mock
