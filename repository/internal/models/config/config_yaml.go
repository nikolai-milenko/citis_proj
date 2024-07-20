package config

type ConfigYAML struct {
	HTTP         HTTPYAML     `yaml:"http"`
	PostgresYAML PostgresYAML `yaml:"postgres"`
}

type HTTPYAML struct {
	Addr string `yaml:"addr"`
}

type PostgresYAML struct {
	URL string `yaml:"-"`
}
