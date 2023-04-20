
import serial
import time

# configure the serial port
ser = serial.Serial('/dev/ttyS0', 115200, timeout=3)
ser.flushInput()

mob_num = "0241888080"
amnt_to_send = '10'
rec_buff = ''

def send_fiat(mob_num,amnt_to_send):
    # send the USSD code to the mobile network
    ser.write(b'AT+CUSD=1,"*171#",15\r\n')
    time.sleep(0.5)

    # read the response from the mobile network
    response = ser.read(1024)
    print(response)

    # # select option airtime and bund
    ser.write(b'AT+CUSD=1,"3",15\r\n')
    time.sleep(0.5)

    # # read the response from the mobile network
    response = ser.read(1024)
    print(response)

     # # select option airtime and bund
    ser.write(b'AT+CUSD=1,"1",15\r\n')
    time.sleep(0.5)

    # # read the response from the mobile network
    response = ser.read(1024)
    print(response)
    
    # # Enter number
    command = 'AT+CUSD=1,"{}",15\r\n'.format(mob_num)
    ser.write(command.encode())
    time.sleep(0.5)

    # # read the response from the mobile network
    response = ser.read(1024)
    print(response)

    # repeat num
    ser.write(command.encode())
    time.sleep(0.5)
    response = ser.read(1024)
    print(response)

    #amnt to send
    amnt = 'AT+CUSD=1,"{}",15\r\n'.format(amnt_to_send)
    ser.write(amnt.encode())
    time.sleep(0.5)
    response = ser.read(1024)
    print(response)

    # pin
    ser.write(b'AT+CUSD=1,"0000",15\r\n')
    
    time.sleep(0.5)
    response = ser.read(1024)
    print(response)

    # response = ser.read(1024)
    # print(response)

## what if there is an error in the process, what if there is a delay
send_fiat(mob_num,amnt_to_send)
