FROM golang:1.22

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY . .

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

RUN chmod +x ./migrations.sh

RUN go build -o main ./cmd/main.go ./cmd/flags.go

EXPOSE 8082

CMD ["/bin/bash", "-c", "./main --cfg=config/config.yaml"]
