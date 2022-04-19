# https://makecode.microbit.org/
cmd = ""

def on_data_received():
    global cmd
    cmd = serial.read_until(serial.delimiters(Delimiters.HASH))
    if cmd == "0":
        basic.show_string("LED ON")
    elif cmd == "1":
        basic.show_string("LED OFF")
    elif cmd == "2":
        basic.show_string("FAN ON")
    elif cmd == "3":
        basic.show_string("FAN OFF")
serial.on_data_received(serial.delimiters(Delimiters.HASH), on_data_received)

def on_forever():
    pass
basic.forever(on_forever)