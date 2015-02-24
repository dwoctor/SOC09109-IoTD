package SOC09109-IoTD

import (
    "fmt"
    "net"
	"encoding/json"
)

const (
    CONN_HOST = "localhost"
    CONN_PORT = "1000"
    CONN_TYPE = "tcp"
)

type WifiDevice struct {
	Name string `json:"name"`
	Type string `json:"type"`
	Ip string `json:"ip"`
	Mac string `json:"mac"`
}

func main() {
    // Listen for incoming connections.
    l, err := net.Listen(CONN_TYPE, CONN_HOST + ":" + CONN_PORT)
    if err != nil {
    	panic(err)
    }
    // Close the listener when the application closes.
    defer l.Close()
    for {
        // Listen for an incoming connection.
        conn, err := l.Accept()
        if err != nil {
        	panic(err)
        }
        // Handle connections in a new goroutine.
        go handleRequest(conn)
    }
}

// Handles incoming requests.
func handleRequest(conn net.Conn) {
	// Make a buffer to hold incoming data.
	buf := make([]byte, 1024)
	// Read the incoming connection into the buffer.
	reqLen, err := conn.Read(buf)
	if err != nil {
		panic(err)
	}
	
	ip, err := externalIP()
	if err != nil {
		panic(err)
	}
	thisDevice := WifiDevice { Name:"pi", Type:"Wifi", Ip:ip }
	thisDeviceJsonized, err := json.Marshal(thisDevice)
	if err != nil {
		panic(err)
	}
	// Send a response back to person contacting us.
	//conn.Write([]byte("Message received."))
	conn.Write(thisDeviceJsonized)
	// Close the connection when you're done with it.
	conn.Close()
}

func externalIP() (string, error) {
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