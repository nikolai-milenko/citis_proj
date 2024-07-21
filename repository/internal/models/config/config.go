package config

type Config struct {
	HTTP     HTTP
	Postgres Postgres
}

type HTTP struct {
	Addr string
}

type Postgres struct {
	URL string
}
