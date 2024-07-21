// Package config предоставляет функции для парсинга конфигурационного файла.
package config

import (
	"os"
	config_models "repository/internal/models/config"

	"github.com/spf13/viper"

	"repository/internal/models/errs"
)

// ParseConfigYAML читает и парсит конфигурационный файл по заданному пути.
func ParseConfigYAML(cfgPath string) (config_models.Config, error) {
	if !fileExists(cfgPath) {
		return config_models.Config{}, errs.ErrFileNotFound
	}

	viper.SetConfigFile(cfgPath)

	if err := viper.ReadInConfig(); err != nil {
		return config_models.Config{}, err
	}

	var cfgYAML config_models.ConfigYAML

	if err := viper.Unmarshal(&cfgYAML); err != nil {
		return config_models.Config{}, err
	}

	dbURL, err := getDBURL()
	if err != nil {
		return config_models.Config{}, err
	}

	cfgYAML.PostgresYAML.URL = dbURL

	transformedCfg := ToCfg(cfgYAML)

	return transformedCfg, nil
}

// fileExists проверяет, существует ли файл по заданному пути.
func fileExists(filename string) bool {
	_, err := os.Stat(filename)

	return !os.IsNotExist(err)
}
