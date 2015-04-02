package main

import (
	"SOC09109-IoTD/commandservice"
	"SOC09109-IoTD/handshakeservice"
	"SOC09109-IoTD/stateservice"
	"SOC09109-IoTD/switchservice"
	"fmt"
)

func main() {
	fmt.Println("Starting Services.")
	cinf := make(chan string)
	cerr := make(chan error)
	go handshakeservice.Start(cinf, cerr)
	go stateservice.Start(cinf, cerr)
	go commandservice.Start(cinf, cerr)
	go switchservice.Start(cinf, cerr)
	for {
		select {
		case info := <-cinf:
			fmt.Println(info)
		case err := <-cerr:
			panic(err)
		}
	}
}
