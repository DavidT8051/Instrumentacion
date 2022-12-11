from machine import UART, Pin, ADC, PWM
import utime

uart = UART(0, 115200)
#uart.init(115200, bits=8, parity=None, stop=1)

termistor = ADC(0)

while True:
    dataAdc = str(termistor.read_u16()>>4) 
    uart.write(dataAdc)
    uart.write("\r\n")
    utime.sleep_ms(50)
    
