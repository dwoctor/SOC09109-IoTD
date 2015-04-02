package stateservice

import (
	"encoding/json"
	"github.com/stianeikeland/go-rpio"
	"net"
)

const (
	CONN      = CONN_TYPE + ":" + CONN_HOST + ":" + CONN_PORT
	CONN_HOST = "localhost"
	CONN_PORT = "2222"
	CONN_TYPE = "tcp"
)

type GpioState struct {
	Pin   int  `json:"pin"`
	State bool `json:"state"`
}

func (this *GpioState) Execute() {
	if err := rpio.Open(); err != nil {
		panic(err)
	}
	defer rpio.Close()
	pin := rpio.Pin(this.Pin)
	pin.Output()
	this.State = pin.Read() != 0
}

func Start(cinf chan string, cerr chan error) {
	cinf <- "Starting State Service. (" + CONN + ")"
	listener, err := net.Listen(CONN_TYPE, CONN_HOST+":"+CONN_PORT)
	if err != nil {
		cerr <- err
	}
	defer listener.Close()
	cinf <- "State Service Running."
	for {
		conn, err := listener.Accept()
		if err != nil {
			cerr <- err
		}
		go handleRequest(conn, cerr)
	}
}

func handleRequest(conn net.Conn, cerr chan error) {
	buf := make([]byte, 1024)
	if _, err := conn.Read(buf); err != nil {
		cerr <- err
	}
	var state GpioState
	err := json.Unmarshal(buf, state)
	if err != nil {
		cerr <- err
	}
	state.Execute()
	json, err := json.Marshal(state)
	if err != nil {
		cerr <- err
	}
	conn.Write(json)
	conn.Close()
}
