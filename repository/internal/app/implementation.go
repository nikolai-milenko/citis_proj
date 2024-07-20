package app

import (
	"context"
	"errors"
	"github.com/jackc/pgx/v5/pgxpool"
	"log"
	"net/http"
	articles3 "repository/internal/handlers/http/articles/articles"
	blacklist3 "repository/internal/handlers/http/articles/blacklist"
	products2 "repository/internal/handlers/http/products"
	"repository/internal/models/config"
	"repository/internal/storage/articles/articles"
	"repository/internal/storage/articles/blacklist"
	"repository/internal/storage/products"
	articles2 "repository/internal/usecase/articles/articles"
	blacklist2 "repository/internal/usecase/articles/blacklist"
	"repository/internal/usecase/products/product"
)

type Implementation struct {
	srv *http.Server
}

func NewImplementation(cfg config.Config) (*Implementation, error) {
	ctx := context.TODO()

	conn, err := startDBConn(ctx, cfg.Postgres)
	if err != nil {
		return nil, err
	}

	mux := http.NewServeMux()

	blacklistStorage := blacklist.NewImplementation(conn)
	blacklistManager := blacklist2.NewImplementation(blacklistStorage)
	blacklistHandler := blacklist3.NewImplementation(blacklistManager)

	articlesStorage := articles.NewImplementation(conn)
	articlesManager := articles2.NewImplementation(articlesStorage)
	articlesHandler := articles3.NewImplementation(articlesManager)

	productsStorage := products.NewImplementation(conn)
	productsManager := product.NewImplementation(productsStorage)
	productsHandler := products2.NewImplementation(productsManager)

	mux.HandleFunc("POST /addhit/", blacklistHandler.AddHit)
	mux.HandleFunc("POST /geturl/", blacklistHandler.GetURLInfo)
	mux.HandleFunc("POST /addarticles/", articlesHandler.AddArticle)
	mux.HandleFunc("POST /deletearticle/", articlesHandler.DeleteArticle)

	mux.HandleFunc("POST /addproducts/", productsHandler.AddProducts)
	mux.HandleFunc("GET /geturls/", productsHandler.GetUrls)

	srv := &http.Server{
		Addr:    cfg.HTTP.Addr,
		Handler: mux,
	}

	return &Implementation{
		srv: srv,
	}, nil
}

func startDBConn(ctx context.Context, cfg config.Postgres) (*pgxpool.Pool, error) {
	pgxCfg, err := pgxpool.ParseConfig(cfg.URL)
	if err != nil {
		return nil, err
	}

	pool, err := pgxpool.NewWithConfig(ctx, pgxCfg)
	if err != nil {
		return nil, err
	}

	err = pool.Ping(ctx)
	if err != nil {
		return nil, err
	}

	return pool, nil
}

func (s *Implementation) Run() error {
	go func() {
		err := s.srv.ListenAndServe()
		if err != nil && !errors.Is(err, http.ErrServerClosed) {
			log.Fatal(err)
		}
	}()

	return nil
}

func (s *Implementation) Stop(ctx context.Context) error {
	return s.srv.Shutdown(ctx)
}
