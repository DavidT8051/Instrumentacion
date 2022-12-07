from machine import Pin
import utime

trig = Pin(16, Pin.OUT)
echo = Pin(17, Pin.IN, Pin.PULL_DOWN)

while True:
    
     trig.value(0)
     utime.sleep(0.1)
     trig.value(1)
     utime.sleep_us(10)
     trig.value(0)
     
     while not echo.value():
          tiempoInicio = utime.ticks_cpu()
     while echo.value():
          tiempoFinal = utime.ticks_cpu()
          
     print(tiempoFinal - tiempoInicio)
     
     utime.sleep_ms(100)


