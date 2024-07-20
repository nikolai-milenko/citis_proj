package main

import (
	"flag"
	"fmt"
)

type flags struct {
	cfgPath string
}

const (
	defaultCfgPath = "config/config.yaml"
	cfgArg         = "cfg"
)

func parseFlags() flags {
	var cfgPath string

	flag.StringVar(&cfgPath, cfgArg, defaultCfgPath, fmt.Sprintf("use --%s=PathToCfg", cfgArg))
	flag.Parse()

	return flags{
		cfgPath: cfgPath,
	}
}
