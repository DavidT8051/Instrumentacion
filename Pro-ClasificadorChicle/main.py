#Clasificador de chicles (NI Vision builder)
from machine import Pin, PWM, UART
import utime

uart = UART(0, 115200)
#uart.init(115200, bits=8, parity=None, stop=1)

def posicion(angulo):
    duty = int((12.346*angulo**2 + 7777.8*angulo + 700000))
    return duty
    
def recoleccion():
    servoDisco.duty_ns(posicion(190))
    
def camara():
    servoDisco.duty_ns(posicion(110))
    
def clasificacion():
    servoDisco.duty_ns(posicion(0))
    
switch_banda = {
    b'1': 182, #Verde Chico
    b'2': 155, #Verde Grande
    b'3': 127, #Morado Chico
    b'4': 90,  #Morado Grande 
    b'5': 45,  #Rojo Chico
    b'6': 5    #Rojo Grande
}

servoBanda = PWM(Pin(15))
servoBanda.freq(50)
servoDisco = PWM(Pin(14))
servoDisco.freq(50)

while True:
    #Movimiento de recoleccion
    recoleccion()
    utime.sleep(2)
    #Movimiento para escaneo
    camara()
    
    while uart.any()==0:
        #Espera de la data
        utime.sleep_ms(10)
        if uart.any()>0:
            data = uart.readline()
            #Movimiento de color
            servoBanda.duty_ns(posicion(switch_banda.get(data)))
            utime.sleep(3)
            #Movimiento para tirar
            clasificacion()
            break
    utime.sleep(2)

