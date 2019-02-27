.PHONY: build clean dev test

# 全局环境变量设置
export GINENV=development
export FANSPATH=$(shell pwd)
export FANSDOMINE=localhost
export FANSPROTOCOL=http
export FANSPORT=8899
export FANSURL=$(FANSPROTOCOL)://$(FANSDOMINE):$(FANSPORT)/
export FANSAPIURL=$(FANSPROTOCOL)://$(FANSDOMINE):$(FANSPORT)/api/v1/
export username=liker1
export follow=liker2
all: clean

build:
	swag init
	go build -v .

swag:
	swag init

test:
	go test -v -coverprofile=cover.out ./...
	go tool cover -func=cover.out
	# 执行可视化查看 go tool cover -html=cover.out
	go tool cover -html=cover.out

# 不同target下设置不同环境变量 必须单独一行
# dev: export GINENV=development
# dev: export FANSPATH=$(shell pwd)
dev: swag
	@#echo $$FANSPATH
	@#swag init
	go run main.go

clean:
	rm -rf main
	go clean -i .

# api.1 关注
ApiFollow:
	curl -X POST $(FANSAPIURL)follow -H "accept: application/json" \
	-H "Content-Type: application/json" \
	-d '{ \
		"username": "$(username)", \
		"follow": "$(follow)", \
		"ip": "127.0.0.1" \
	}'
