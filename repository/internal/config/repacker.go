package config

import "repository/internal/models/config"

func ToCfg(cfg config.ConfigYAML) config.Config {
	return config.Config{
		HTTP:     HTTPYAMLToCfg(cfg.HTTP),
		Postgres: PostgresYAMLToCfg(cfg.PostgresYAML),
	}
}

func PostgresYAMLToCfg(cfg config.PostgresYAML) config.Postgres {
	return config.Postgres(cfg)
}

func HTTPYAMLToCfg(cfg config.HTTPYAML) config.HTTP {
	return config.HTTP(cfg)
}
