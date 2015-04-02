package commandservice

import (
	"encoding/json"
	"github.com/stianeikeland/go-rpio"
	"net"
)

const (
	CONN      = CONN_TYPE + ":" + CONN_HOST + ":" + CONN_PORT
	CONN_HOST = "localhost"
	CONN_PORT = "3333"
	CONN_TYPE = "tcp"
)

type GpioCommand struct {
	Pin   int  `json:"pin"`
	State bool `json:"state"`
}

func (this GpioCommand) Execute() {
	if err := rpio.Open(); err != nil {
		panic(err)
	}
	defer rpio.Close()
	pin := rpio.Pin(this.Pin)
	pin.Output()
	if this.State {
		pin.High()
	} else {
		pin.Low()
	}
}

func Start(cinf chan string, cerr chan error) {
	cinf <- "Starting Command Service. (" + CONN + ")"
	listener, err := net.Listen(CONN_TYPE, CONN_HOST+":"+CONN_PORT)
	if err != nil {
		cerr <- err
	}
	defer listener.Close()
	cinf <- "Command Service Running."
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
	var command GpioCommand
	if err := json.Unmarshal(buf, command); err != nil {
		cerr <- err
	}
	command.Execute()
	conn.Close()
}
