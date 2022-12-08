#Escaner
"""
*************GPIOS****************
GPIO0 --> IN1 M1(VL53LDK) --> 1
GPIO1 --> IN2 M1(VL53LDK) --> 2
GPIO2 --> IN3 M1(VL53LDK) --> 4
GPIO3 --> IN4 M1(VL53LDK) --> 5

GPIO4 --> IN1 M2(PLATO) --> 6
GPIO5 --> IN2 M2(PLATO) --> 7
GPIO6 --> IN3 M2(PLATO) --> 9
GPIO7 --> IN4 M2(PLATO) --> 10

GPIO8 --> Limit Switch --> 34

GPIO16 --> SDA - SENSOR VL53LDK --> 22
GPIO17 --> SCL - SENSOR VL53LDK --> 21
"""

from machine import Pin, I2C
import time
import utime
from vl53l0x import VL53L0X
from stepMotor import M1_DER_VL53LDK, M1_IZQ_VL53LDK, M2_DER_PLATO, M2_IZQ_PLATO, M1_OFF, M2_OFF
import _thread

def home(): #Buscar el limite inferior
    global flagEnd
    
    for i in range(0,10000,1):
        print("A")
        if flagEnd:
            break
        M1_DER_VL53LDK(1,5) #1 paso del motor hacia abajo (5ms)  
    M1_IZQ_VL53LDK(50,5) #50 pasos del motor hacia arriba (5ms)
    flagEnd = False #Limpiar la bandera del limite
    
def limitSwitch(endStop): #Se llego al limite 
    global flagEnd
    flagEnd = True
    utime.sleep_ms(250)

#limit switch
endStop = Pin(28, Pin.IN, Pin.PULL_DOWN)
endStop.irq(limitSwitch, Pin.IRQ_RISING)
flagEnd = False

#Configuracion del sensor VL53LDK
sda = Pin(16)
scl = Pin(17)
id = 0
i2c = I2C(id=id, sda=sda, scl=scl)

vl53ldk = VL53L0X(i2c)
vl53ldk.set_measurement_timing_budget(40000)
vl53ldk.set_Vcsel_pulse_period(vl53ldk.vcsel_period_type[0], 12)
vl53ldk.set_Vcsel_pulse_period(vl53ldk.vcsel_period_type[1], 8)

medidaVacio = 200 #Medida en mm que me indica que no hay un objeto
flagNoObjeto = False #Bandera que me indica si hay o no un objeto
contadorNoObjetos = 0
flagFinObjeto = False #Bandera que me indica si se llego al final del objeto

#361 puntos --> 512 revolucion
#-->
led = Pin(25, Pin.OUT)

home() #Buscar el punto de inicio

#Verificar si hay objeto
d_mm = vl53ldk.ping()-50

flagData = True
for i in range(0,10000,1): #Movimiento del sensor
    contadorNoObjetos = 0
    for j in range(0,512,1): #Movimiento del plato exactamente 512 pasos(1 rev)
        d_mm = vl53ldk.ping()-50
        radio = 300-d_mm
        if radio<=1:
            radio = 0
        print(radio,j)
        if d_mm >= medidaVacio:
            contadorNoObjetos += 1
        M2_DER_PLATO(1,10)
    led.toggle()
    if contadorNoObjetos > 50:
        break
    M1_IZQ_VL53LDK(15,3)

#Finalizar serial en Labview
flagData = True
for i in range(0,10,1):
    print(1,0)
    utime.sleep_ms(50)

M1_OFF()
M2_OFF()


    

