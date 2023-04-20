#remember to pip install pyserial
import serial
import time
import logging
import configparser
import sqlite3

# Configure logging
logging.basicConfig(filename='mobile_money.log', level=logging.INFO, 
    format='%(asctime)s %(levelname)s %(message)s')

# Read configuration settings
config = configparser.ConfigParser()
config.read('config.ini')
serial_port = config.get('serial', 'port')
baud_rate = config.getint('serial', 'baud_rate')
timeout = config.getint('serial', 'timeout')
db_file = config.get('database', 'file')

# Open database connection
conn = sqlite3.connect(db_file)
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS transactions 
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     phone_number TEXT NOT NULL,
     amount INTEGER NOT NULL,
     timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
''')
conn.commit()

def send_fiat(mob_num, amnt_to_send):
    # send the USSD code to the mobile network
    ser.write(b'AT+CUSD=1,"*171#",15\r\n')
    time.sleep(0.5)

    # read the response from the mobile network
    response = ser.read(1024)
    if b'ERROR' in response:
        logging.error('Failed to send USSD code to mobile network')
        raise Exception('Failed to send USSD code to mobile network')
    logging.info(response)

    # select option airtime and bund
    ser.write(b'AT+CUSD=1,"3",15\r\n')
    time.sleep(0.5)

    # read the response from the mobile network
    response = ser.read(1024)
    if b'ERROR' in response:
        logging.error('Failed to select option airtime and bund')
        raise Exception('Failed to select option airtime and bund')
    logging.info(response)

    # select option airtime and bund
    ser.write(b'AT+CUSD=1,"1",15\r\n')
    time.sleep(0.5)

    # read the response from the mobile network
    response = ser.read(1024)
    if b'ERROR' in response:
        logging.error('Failed to select option airtime and bund')
        raise Exception('Failed to select option airtime and bund')
    logging.info(response)

    # Enter number
    command = 'AT+CUSD=1,"{}",15\r\n'.format(mob_num)
    ser.write(command.encode())
    time.sleep(0.5)

    # read the response from the mobile network
    response = ser.read(1024)
    if b'ERROR' in response:
        logging.error('Failed to enter phone number')
        raise Exception('Failed to enter phone number')
    logging.info(response)

    # repeat num
    ser.write(command.encode())
    time.sleep(0.5)
    response = ser.read(1024)
    if b'ERROR' in response:
        logging.error('Failed to repeat phone number')
        raise Exception('Failed to repeat phone number')
    logging.info(response)

    # amnt to send
    amnt = 'AT+CUSD=1,"{}",15\r\n'.format(amnt_to_send)
    ser.write(amnt.encode())
    time.sleep(0.5)
    response = ser.read(1024)
    if b'ERROR' in response:
        logging.error('Failed to enter amount')
        raise Exception('Failed to enter amount')
    logging.info(response)

    # pin
    ser.write(b'AT+CUSD=1,"0000",15\r\n')
    time.sleep(0.5)
    response = ser.read(1024)
    logging.info(response)

    if b'ERROR' in response:
        logging.error('Failed to enter PIN')
        raise Exception('Failed to enter PIN')
    return (mob_num, amnt_to_send)

def send_mobile_money():
    with open('phone_numbers.txt') as f:
        for line in f:
            try:
                phone_number, amount = line.strip().split(',')
                mob_num, amnt_to_send = send_fiat(phone_number, amount)
                c.execute('INSERT INTO transactions (phone_number, amount) VALUES (?, ?)', (mob_num, amnt_to_send))
                conn.commit()
            except Exception as e:
                logging.error(str(e))

def main():
    global ser
# configure the serial port
    ser = serial.Serial(serial_port, baud_rate, timeout=timeout)
    ser.flushInput()
    try:
        send_mobile_money()
    except Exception as e:
        logging.error(str(e))
    finally:
        ser.close()

if __name__ == '__main__':
    main()