package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"repository/internal/app"
	"repository/internal/config"
	"syscall"
)

func main() {
	parsedFlags := parseFlags()

	cfg, err := config.ParseConfigYAML(parsedFlags.cfgPath)
	if err != nil {
		log.Fatal(err)
	}

	sig := make(chan os.Signal, 1)

	signal.Notify(sig, os.Interrupt, os.Kill, syscall.SIGTERM)

	application, err := app.NewImplementation(cfg)
	if err != nil {
		log.Fatal(err)
	}

	err = application.Run()
	if err != nil {
		log.Fatal(err)
	}

	<-sig

	application.Stop(context.TODO())
}
