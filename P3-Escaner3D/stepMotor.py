"""
Motor a pasos 28byj48
512 pasos simples para 1 revolucion

GPIOS - RASPBERRY PI PICO:
M1 - VL53LDK
GPIO0 --> IN1
GPIO1 --> IN2
GPIO2 --> IN3
GPIO3 --> IN4
M2 - PLATO
GPIO4 --> IN1
GPIO5 --> IN2
GPIO6 --> IN3
GPIO7 --> IN4

Funciones M1(VL53LDK):
M1_IZQ_VL53LDK(#pasos, tiempoPasos) --> Hace un paso simple n veces a la izquierda
M1_DER_VL53LDK(#pasos, tiempoPasos) --> Hace un paso simple n veces a la derecha
M1_OFF() --> Apaga los pines del M1

Funciones M2(PLATO):
M2_IZQ_PLATO(#pasos, tiempoPasos) --> Hace un paso simple n veces a la izquierda
M2_DER_PLATO(#pasos, tiempoPasos) --> Hace un paso simple n veces a la derecha
M2_OFF() --> Apaga los pines del M2

"""

from machine import Pin
import utime

def M2_IZQ_PLATO(veces, tiempo):
    global secuenciaM2
    
    for i in range(0,veces,1):
        secuenciaM2[3].value(1)
        secuenciaM2[2].value(0)
        secuenciaM2[1].value(0)
        secuenciaM2[0].value(0)
        utime.sleep_ms(tiempo)
        
        secuenciaM2[3].value(0)
        secuenciaM2[2].value(1)
        secuenciaM2[1].value(0)
        secuenciaM2[0].value(0)
        utime.sleep_ms(tiempo)
        
        secuenciaM2[3].value(0)
        secuenciaM2[2].value(0)
        secuenciaM2[1].value(1)
        secuenciaM2[0].value(0)
        utime.sleep_ms(tiempo)
        
        secuenciaM2[3].value(0)
        secuenciaM2[2].value(0)
        secuenciaM2[1].value(0)
        secuenciaM2[0].value(1)
        utime.sleep_ms(tiempo)

def M2_DER_PLATO(veces, tiempo):
    global secuenciaM2
    
    for i in range(0,veces,1):
        secuenciaM2[0].value(1)
        secuenciaM2[1].value(0)
        secuenciaM2[2].value(0)
        secuenciaM2[3].value(0)
        utime.sleep_ms(tiempo)
        
        secuenciaM2[0].value(0)
        secuenciaM2[1].value(1)
        secuenciaM2[2].value(0)
        secuenciaM2[3].value(0)
        utime.sleep_ms(tiempo)
        
        secuenciaM2[0].value(0)
        secuenciaM2[1].value(0)
        secuenciaM2[2].value(1)
        secuenciaM2[3].value(0)
        utime.sleep_ms(tiempo)
        
        secuenciaM2[0].value(0)
        secuenciaM2[1].value(0)
        secuenciaM2[2].value(0)
        secuenciaM2[3].value(1)
        utime.sleep_ms(tiempo)

def M2_OFF():
    global secuenciaM2
    
    secuenciaM2[0].value(0)
    secuenciaM2[1].value(0)
    secuenciaM2[2].value(0)
    secuenciaM2[3].value(0)

def M1_IZQ_VL53LDK(veces, tiempo):
    global secuenciaM1
    
    for i in range(0,veces,1):
        secuenciaM1[3].value(1)
        secuenciaM1[2].value(0)
        secuenciaM1[1].value(0)
        secuenciaM1[0].value(0)
        utime.sleep_ms(tiempo)
        
        secuenciaM1[3].value(0)
        secuenciaM1[2].value(1)
        secuenciaM1[1].value(0)
        secuenciaM1[0].value(0)
        utime.sleep_ms(tiempo)
        
        secuenciaM1[3].value(0)
        secuenciaM1[2].value(0)
        secuenciaM1[1].value(1)
        secuenciaM1[0].value(0)
        utime.sleep_ms(tiempo)
        
        secuenciaM1[3].value(0)
        secuenciaM1[2].value(0)
        secuenciaM1[1].value(0)
        secuenciaM1[0].value(1)
        utime.sleep_ms(tiempo)

def M1_DER_VL53LDK(veces, tiempo):
    global secuenciaM1
    
    for i in range(0,veces,1):
        secuenciaM1[0].value(1)
        secuenciaM1[1].value(0)
        secuenciaM1[2].value(0)
        secuenciaM1[3].value(0)
        utime.sleep_ms(tiempo)
        
        secuenciaM1[0].value(0)
        secuenciaM1[1].value(1)
        secuenciaM1[2].value(0)
        secuenciaM1[3].value(0)
        utime.sleep_ms(tiempo)
        
        secuenciaM1[0].value(0)
        secuenciaM1[1].value(0)
        secuenciaM1[2].value(1)
        secuenciaM1[3].value(0)
        utime.sleep_ms(tiempo)
        
        secuenciaM1[0].value(0)
        secuenciaM1[1].value(0)
        secuenciaM1[2].value(0)
        secuenciaM1[3].value(1)
        utime.sleep_ms(tiempo)

def M1_OFF():
    global secuenciaM1
    
    secuenciaM1[0].value(0)
    secuenciaM1[1].value(0)
    secuenciaM1[2].value(0)
    secuenciaM1[3].value(0)

#secuencia del motor a pasos VL53LDK --> GPIO0, GPIO1, GPIO2, GPIO3
secuenciaM1 = [0,0,0,0]
for i in range(0,4,1):
    secuenciaM1[i] = Pin(i, Pin.OUT)
        
#secuencia del motor a pasos PLATO --> GPIO4, GPIO5, GPIO6, GPIO7
secuenciaM2 = [0,0,0,0]
for i in range(0,4,1):
    secuenciaM2[i] = Pin(i+4, Pin.OUT)
    
while True:
    M1_IZQ_VL53LDK(1000,5)