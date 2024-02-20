import serial
import sys
import time

BAUD_RATE=9600
MESSAGE_TYPE_HEARBEAT=0x01

def fletcher16(data): 
    sum1 = 0
    sum2 = 0
    for index in range(len(data)):
        sum1 = (sum1 + data[index]) % 255
        sum2 = (sum2 + sum1) % 255
    return bytes([sum2, sum1])


def send_packet(ser, message_type, data):
    packet = [0xBE, 0xEF, message_type]
    packet += data
    packet += fletcher16(packet)
    ser.write(bytes(packet))


if len(sys.argv) < 2:
    print("Invalid number of arguments: please specify serial port.")
    exit(-1)

port=sys.argv[1]
print("Using serial port: ", port)
print("Baud rate: ", BAUD_RATE)

serial_port = serial.Serial(port=port, baudrate=BAUD_RATE)

while True:
    send_packet(serial_port, MESSAGE_TYPE_HEARBEAT, [0, 0, 0, 0, 0, 0, 0, 0])
    time.sleep(1)

serial_port.close()