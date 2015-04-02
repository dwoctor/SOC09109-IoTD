package handshakeservice

import (
	"encoding/json"
	"errors"
	"net"
)

const (
	CONN              = CONN_TYPE + ":" + CONN_HOST + ":" + CONN_PORT
	CONN_HOST         = "localhost"
	CONN_PORT         = "1111"
	CONN_TYPE         = "tcp"
	DEVICE_NAME       = "pi"
	DEVICE_TYPE       = "wifi"
	DEVICE_CAPABILITY = "gpio"
)

type DeviceInfo struct {
	Name       string `json:"name"`
	Type       string `json:"type"`
	Capability string `json:"capability"`
	Ip         string `json:"ip"`
	Mac        string `json:"mac"`
}

var DEVICE_JSON []byte

func Start(cinf chan string, cerr chan error) {
	cinf <- "Starting Handshake Service. (" + CONN + ")"
	listener, err := net.Listen(CONN_TYPE, CONN_HOST+":"+CONN_PORT)
	if err != nil {
		cerr <- err
	}
	defer listener.Close()
	ip, err := getIp()
	if err != nil {
		cerr <- err
	}
	info := DeviceInfo{Name: DEVICE_NAME, Type: DEVICE_TYPE, Capability: DEVICE_CAPABILITY, Ip: ip}
	json, err := json.Marshal(info)
	if err != nil {
		cerr <- err
	}
	DEVICE_JSON = json
	cinf <- "Handshake Service Running."
	for {
		conn, err := listener.Accept()
		if err != nil {
			cerr <- err
		}
		go handleRequest(conn, cerr)
	}
}

func handleRequest(conn net.Conn, cerr chan error) {
	conn.Write(DEVICE_JSON)
	conn.Close()
}

func getIp() (string, error) {
	ifaces, err := net.Interfaces()
	if err != nil {
		return "", err
	}
	for _, iface := range ifaces {
		if iface.Flags&net.FlagUp == 0 {
			continue // interface down
		}
		if iface.Flags&net.FlagLoopback != 0 {
			continue // loopback interface
		}
		addrs, err := iface.Addrs()
		if err != nil {
			return "", err
		}
		for _, addr := range addrs {
			var ip net.IP
			switch v := addr.(type) {
			case *net.IPNet:
				ip = v.IP
			case *net.IPAddr:
				ip = v.IP
			}
			if ip == nil || ip.IsLoopback() {
				continue
			}
			ip = ip.To4()
			if ip == nil {
				continue // not an ipv4 address
			}
			return ip.String(), nil
		}
	}
	return "", errors.New("are you connected to the network?")
}
