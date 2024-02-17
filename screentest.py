import RPi.GPIO as GPIO
import time

# Define GPIO pins
CLK = 20  # Clock pin
DIO = 16  # Data pin

# 7-segment display digit mapping
DIGIT_MAPPING = {
    0: 0b00111111,
    1: 0b00000110,
    2: 0b01011011,
    3: 0b01001111,
    4: 0b01100110,
    5: 0b01101101,
    6: 0b01111101,
    7: 0b00000111,
    8: 0b01111111,
    9: 0b01101111,
}


def tm1637_send_byte(data):
    for i in range(8):
        GPIO.output(CLK, GPIO.LOW)
        GPIO.output(DIO, (data & 0x01) == 0x01)
        data >>= 1
        GPIO.output(CLK, GPIO.HIGH)


def tm1637_start():
    GPIO.output(DIO, GPIO.LOW)
    GPIO.output(CLK, GPIO.LOW)
    GPIO.output(CLK, GPIO.HIGH)
    GPIO.output(DIO, GPIO.HIGH)


def tm1637_stop():
    GPIO.output(CLK, GPIO.LOW)
    GPIO.output(DIO, GPIO.LOW)
    GPIO.output(CLK, GPIO.HIGH)
    GPIO.output(DIO, GPIO.HIGH)


def tm1637_write_byte(addr, data):
    tm1637_start()
    tm1637_send_byte(addr)
    tm1637_send_byte(data)
    tm1637_stop()


def display_number(number):
    digits = [int(digit) for digit in str(number).zfill(4)]

    for i in range(4):
        tm1637_write_byte(i + 1, DIGIT_MAPPING[digits[i]])


if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(CLK, GPIO.OUT)
        GPIO.setup(DIO, GPIO.OUT)

        while True:
            # Display a number (change this to the desired number)
            display_number(1234)

            # Wait for a few seconds
            time.sleep(2)

            # Clear the display
            for i in range(4):
                tm1637_write_byte(i + 1, 0x00)

            # Wait for a few seconds
            time.sleep(2)

    except KeyboardInterrupt:
        print("Program stopped by the user.")
    finally:
        # Clean up GPIO on exit
        GPIO.cleanup()
