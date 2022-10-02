from machine import Pin, PWM, I2C
from math import sqrt, degrees, acos, atan2
from imu import MPU6050
import utime
import random

"""
grados*220+2225000

MOTOR A PASOS
GPIO18 --> IN1 
GPIO19 --> IN2
GPIO20 --> IN3 
GPIO21 --> IN4 
GPIO22 --> EN

BOTONES DE CONTROL
GPIO9 --> BOTON ON/OF
GPIO10 --> CAMBIO DISCO
GPIO11 --> V MAX
GPIO12 --> V MIN
GPIO13 --> INICIAR

SERVOS
GPIO17 --> SERVO X
GPIO18 --> SERVO Y

GIROSCOPIO
GPIO14 --> SDA
GPIO15 --> SCL
"""
def giroscopio():
    global grados, flagDePolaridad
    #Calculo de la magnitud
    x = imu.accel.x
    y = imu.accel.y
    z = imu.accel.z
    gradosPar = degrees(acos(z / sqrt(x**2 + y**2 + z**2)))
    
    #Identificacion del sentido
    gy = imu.gyro.y
    
    if gy>15 and gradosPar<10:
        #Se movio a la IZQUIERDA (-)
        flagDePolaridad = False
        
    elif gy<-15 and gradosPar<10:
        #Se movio a la DERECHA (+)
        flagDePolaridad = True
    
    if flagDePolaridad:
        gradosPar = abs(gradosPar)
    else:
        gradosPar = -gradosPar
    
    grados = -gradosPar + 90
    
    if grados > 180:
        grados = 180
    elif grados < 0:
        grados = 0


def pasoSimple():
    global secuencia
    
    secuencia[0].value(1)
    secuencia[1].value(0)
    secuencia[2].value(0)
    secuencia[3].value(0)
    utime.sleep_ms(10)
    secuencia[0].value(0)
    secuencia[1].value(1)
    secuencia[2].value(0)
    secuencia[3].value(0)
    utime.sleep_ms(10)
    secuencia[0].value(0)
    secuencia[1].value(0)
    secuencia[2].value(1)
    secuencia[3].value(0)
    utime.sleep_ms(10)
    secuencia[0].value(0)
    secuencia[1].value(0)
    secuencia[2].value(0)
    secuencia[3].value(1)
    utime.sleep_ms(10)

def apagarMP():
    global secuencia
    EN.value(0)
    secuencia[0].value(0)
    secuencia[1].value(0)
    secuencia[2].value(0)
    secuencia[3].value(0)
    
def encenderMP():
    EN.value(1)

def encendido(botonON):# flagON == True --> ENCENDIDO DEL SISTEMA *** flagON = False --> APAGADO DEL SISTEMA
    global flagON
    flagON = not flagON
    print("Encendido del sistema: ",flagON)
    utime.sleep_ms(1000)
   
def cambioDisco(botonCD):
    global flagCambioDisco
    flagCambioDisco = not flagCambioDisco
    print("Cambio de disco: ",flagCambioDisco)
    utime.sleep_ms(1000)

def valorMax(botonVMA):
    global rango
    if rango<100:
        rango += 20
        
    print(rango)
    utime.sleep_ms(100)

def valorMin(botonVMI):
    global rango
    if rango>-100:
        rango -= 20
        
    print(rango)
    utime.sleep_ms(100)

def inicio(botonST):
    global flagST
    flagST = not flagST
    print("Proceso: ",flagST)
    utime.sleep_ms(1000)

#tiempo en alto en ns --> min. 500000 - max. 2500000

#Servo escribe los grados
servoX = PWM(Pin(16))
servoX.freq(50)
servoX.duty_ns(2460400)

#Servo levanta el lapiz
servoY = PWM(Pin(17))
servoY.freq(50)
servoY.duty_ns(2100000) #Lapiz levantado comienzo

#Boton de ON/OFF
botonON = Pin(9, Pin.IN, Pin.PULL_DOWN)
botonON.irq(encendido, Pin.IRQ_FALLING)

#Boton de Cambio de disco
botonCD = Pin(10, Pin.IN, Pin.PULL_DOWN)
botonCD.irq(cambioDisco, Pin.IRQ_FALLING)

#Boton de valor maximo
botonVMA = Pin(11, Pin.IN, Pin.PULL_DOWN)
botonVMA.irq(valorMax, Pin.IRQ_RISING)

#Boton de valor minimo
botonVMI = Pin(12, Pin.IN, Pin.PULL_DOWN)
botonVMI.irq(valorMin, Pin.IRQ_RISING)

#Boton de iniciar
botonST = Pin(13, Pin.IN, Pin.PULL_DOWN)
botonST.irq(inicio, Pin.IRQ_RISING)

#GPIOS del motor a pasos
secuencia = [0,0,0,0]
for i in range(0,4,1):
    secuencia[i] = Pin(i+18, Pin.OUT)
    
#Habilitacion del MP
EN = Pin(22, Pin.OUT)
EN.value(0)
    
#Leds indicadores
LEDON = Pin(28, Pin.OUT)
LEDON.value(0)
LEDOFF = Pin(27, Pin.OUT)
LEDOFF.value(0)
LEDPRO = Pin(26, Pin.OUT)
LEDPRO.value(0)

flagCambioDisco = False #Bandera que indica el Cambio de disco: True(abajo) y False(arriba)
flagON = False #Bandera que indica el ON/OFF del sistema
flagST = False #Bandera que indica el inicio del sistema

#GIROSCOPIO
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)
imu = MPU6050(i2c)
flagDePolaridad = True

grados = 0
rango = 0

while True:
    
    #Leds indicadores
    if flagON:
        LEDON.value(1)
        LEDOFF.value(0)
        LEDPRO.value(0)
    else:
        LEDON.value(0)
        LEDOFF.value(1)
        LEDPRO.value(0)
    
    #Cambio de disco
    if flagCambioDisco:
        servoY.duty_ns(920000) #Baja el lapiz 1000000
    else:
        servoY.duty_ns(2100000) #Sube el lapiz
        servoX.duty_ns(2460400) #Posicion de inicio en X
        
    if flagON:
        while not flagST:
            LEDON.value(1)
            LEDOFF.value(0)
            
        LEDPRO.value(1)
        LEDON.value(0)
        espiral = 0
        rango = 0
        
        for i in range(0,2048,1):
            #grados = random.randint(0,180)
            
            giroscopio()
            print(grados)
            
            #Rango de Vmax y Vmin --> 450 - 250
            espiral -= 195 #default = 350
            servoX.duty_ns(int(grados*(300+rango)+2397400+espiral))
            
            encenderMP()
            pasoSimple()
            if not flagCambioDisco or not flagON:
                servoY.duty_ns(2100000) #Sube el lapiz
                servoX.duty_ns(2460400) #Posicion de inicio en X
                apagarMP()
                flagON = False
                flagST = False
                break
        #Se termina el ciclo
        flagON = False
        flagST = False
        flagCambioDisco = False
        servoX.duty_ns(2460400) #Posicion de inicio en X
        apagarMP()
        


