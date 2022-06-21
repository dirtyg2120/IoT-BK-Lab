def run_timer():
    global timer_counter, timer_flag
    if timer_counter > 0:
        timer_counter = timer_counter - 1
    if timer_counter == 0:
        timer_flag = 1
def get_timer_flag():
    return timer_flag

def on_button_pressed_a():
    global is_button_pressed
    is_button_pressed = 1
input.on_button_pressed(Button.A, on_button_pressed_a)

def set_timer():
    global timer_flag, timer_counter
    if timer_counter == 0:
        timer_flag = 0
        timer_counter = SEND_INTERVAL / TIMER_CYCLE
def software_timer_init():
    global timer_counter, timer_flag
    timer_counter = 0
    timer_flag = 0

def on_data_received():
    global recv_data, ack_received_successful, serial_data_available
    recv_data = serial.read_until(serial.delimiters(Delimiters.HASH))
    if recv_data == "ACK":
        ack_received_successful = 1
    else:
        serial_data_available = 1
        if recv_data == "0":
            basic.show_number(0)
        elif recv_data == "1":
            basic.show_number(1)
        elif recv_data == "2":
            basic.show_number(2)
        elif recv_data == "3":
            basic.show_number(3)
serial.on_data_received(serial.delimiters(Delimiters.HASH), on_data_received)

counter_failure = 0
serial_data_available = 0
ack_received_successful = 0
recv_data = ""
is_button_pressed = 0
timer_flag = 0
timer_counter = 0
IDLE = 0
SEND_INTERVAL = 0
TIMER_CYCLE = 0
TIMER_CYCLE = 10
SEND_MAX = 5
SEND_INTERVAL = 100
SEND_DATA = 1
WAIT_ACK = 2
SEND_ACK = 3
ERROR_LOG = 4
state = IDLE

def on_forever():
    global serial_data_available, state, is_button_pressed, counter_failure
    if state == IDLE:
        if serial_data_available == 1:
            serial_data_available = 0
            state = SEND_ACK
        elif is_button_pressed == 1:
            is_button_pressed = 0
            state = SEND_DATA
    elif state == SEND_DATA:
        serial.write_string("!1:" + "TEMP" + ":" + ("" + str(input.temperature())) + "#")
        basic.show_number(counter_failure)
        set_timer()
        state = WAIT_ACK
    elif state == WAIT_ACK:
        if ack_received_successful == 1:
            state = IDLE
        elif get_timer_flag() == 1:
            counter_failure = counter_failure + 1
            if counter_failure >= SEND_MAX:
                counter_failure = 0
                state = ERROR_LOG
            else:
                state = SEND_DATA
    elif state == SEND_ACK:
        serial.write_string("!1:" + "ACK" + ":" + "1" + "#")
        state = IDLE
    elif state == ERROR_LOG:
        state = IDLE
    run_timer()
    basic.pause(TIMER_CYCLE)
basic.forever(on_forever)
