package main

import (
	"bytes"
	"context"
	"io"
	"io/ioutil"
	"log"
	"unsafe"

	"github.com/projectdiscovery/subfinder/v2/pkg/passive"
	"github.com/projectdiscovery/subfinder/v2/pkg/resolve"
	"github.com/projectdiscovery/subfinder/v2/pkg/runner"
)

func find_subdomain(url string) unsafe.Pointer {
	config := runner.ConfigFile{
		// Use the default list of resolvers by marshaling it to the config
		Resolvers: resolve.DefaultResolvers,
		// Use the default list of passive sources
		Sources: passive.DefaultSources,
		// Use the default list of all passive sources
		AllSources: passive.DefaultAllSources,
		// Use the default list of recursive sources
		Recursive: passive.DefaultRecursiveSources,
	}

	runnerInstance, err := runner.NewRunner(&runner.Options{
		Threads:            10, // Thread controls the number of threads to use for active enumerations
		Timeout:            30, // Timeout is the seconds to wait for sources to respond
		MaxEnumerationTime: 10, // MaxEnumerationTime is the maximum amount of time in mins to wait for enumeration
		YAMLConfig:         config,
	})
	if err != nil {
		log.Fatal(err)
	}

	buf := bytes.Buffer{}
	err = runnerInstance.EnumerateSingleDomain(context.Background(), url, []io.Writer{&buf})
	if err != nil {
		log.Fatal(err)
	}

	data, err := ioutil.ReadAll(&buf)
	if err != nil {
		log.Fatal(err)
	}
	result := []string{string(data)}
	return unsafe.Pointer(&result)
}

func main() {}
