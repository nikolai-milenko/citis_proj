package products

import (
	"context"
	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgconn"
)

type connCommiter interface {
	Query(context.Context, string, ...interface{}) (pgx.Rows, error)
	QueryRow(context.Context, string, ...interface{}) pgx.Row
	Exec(context.Context, string, ...interface{}) (pgconn.CommandTag, error)
}

type Implementation struct {
	conn connCommiter
}

func NewImplementation(conn connCommiter) *Implementation {
	return &Implementation{
		conn: conn,
	}
}
