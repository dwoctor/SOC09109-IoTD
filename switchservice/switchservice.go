package switchservice

import "github.com/stianeikeland/go-rpio"

func Start(cinf chan string, cerr chan error) {
	cinf <- "Starting Switch Service."
	if err := rpio.Open(); err != nil {
		cerr <- err
	}
	defer rpio.Close()
	switch_pin := rpio.Pin(22)
	switch_pin.Input()
	switch_pin.PullUp()
	led_pin := rpio.Pin(17)
	led_pin.Output()
	cinf <- "Switch Service Running."
	for {
		if switch_pin.Read() != 0 {
			for switch_pin.Read() != 0 {
			}
			led_pin.Toggle()
		}
	}
}
