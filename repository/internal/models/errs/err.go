package errs

import "errors"

var (
	ErrNoEnvFile            = errors.New("файл с переменными окружения не найден")
	ErrDBURLNotSet          = errors.New("URL для подключения к БД не установлен")
	ErrURLNotFound          = errors.New("url не найден")
	ErrFileNotFound         = errors.New("файл конфигурации не найден")
	ErrArticleAlreadyExists = errors.New("статья уже существует")
	ErrArticleNotFound      = errors.New("статья не найдена")
)
