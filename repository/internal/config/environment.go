package config

import (
	"os"

	"github.com/joho/godotenv"

	"repository/internal/models/errs"
)

const dbKeyURL string = "DBURL"

const dbHostKey string = "PGHOST"

// GetPostgresConfig читает данные для подключения к БД из окружения.
func getDBURL() (string, error) {
	err := godotenv.Load()
	if err != nil {
		return "", errs.ErrNoEnvFile
	}

	dbURL := os.Getenv(dbKeyURL)

	if dbURL == "" {
		return "", errs.ErrDBURLNotSet
	}

	return dbURL, nil
}
