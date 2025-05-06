#LIBRERIAS USADAS
from machine import Pin, Timer
from lcd1602 import LCD #hay que cargar previamente este modulo a la placa
from utime import sleep

print("INICIO SISTEMA SEMÁFORO")

#SALIDAS
rojo=Pin(13, Pin.OUT)
ama=Pin(12, Pin.OUT)
verde=Pin(14, Pin.OUT)
verde_peaton=Pin(27, Pin.OUT)
rojo_peaton=Pin(26, Pin.OUT)
lcd=LCD()


#ENTRADAS
S1=Pin(36, Pin.IN) #PULSADOR

#TEMPORIZADORES
timer0=Timer(0)
timer1=Timer(1)
timer2=Timer(2)
timer3=Timer(3)

#ESTADO INICIAL
verde.on()
rojo_peaton.on()
verde_peaton.off()

#FUNCIONES PARA LOS 4 TEMPORIZADORES
def ambar(t):
    lcd.clear() #limpia el mensaje anterior que hubiese
    print("Ámbar coches") #salida por consola
    lcd.message("Ambar coches") #salida epor pantalla lcd, no admite tildes.
    verde.off()
    ama.on()
    rojo.off()
    timer0.deinit() #desactivar timer que llamó a esta funcion
    timer1.init(period=4000,mode=Timer.ONE_SHOT,callback=intermitente) #activa siguiente timer
    
def intermitente(t):
    lcd.clear()
    print("Ambar coches intermitente")
    lcd.message("Ambar coches \nintermitente")
    timer1.deinit()
    timer2.init(period=4000,mode=Timer.ONE_SHOT,callback=stop) #he observado que da igual la duracion que ponga aquí, no se ejecuta el siguiente timer hasta que termine el bucle para intermitencia
    i=0
    while True: #bucle while para intermitencia, tal vez tenga más sentido usar un bucle for.
        ama.off()
        sleep(0.5)
        ama.on()
        sleep(0.5)
        i=i+1
        if i==4:
            break
    
def stop(t):
    lcd.clear()
    print("STOP coches.Paso peatones")
    lcd.message("STOP coches.\nPaso peatones")
    timer2.deinit()
    timer3.init(period=8000,mode=Timer.ONE_SHOT,callback=reposo) #he observado que da igual la duracion que ponga aquí, no se ejecuta el siguiente timer hasta que termina el bucle para intermitencia
    ama.off()
    verde.off()
    rojo.on()
    rojo_peaton.off()
    verde_peaton.on()
    sleep(4) #4 segundos de VERDE PEATON, luego otros 4 segundos de VERDE PEATON intermitente
    i=0
    for i in range(0,4): #bucle for para intermitencia de VERDE PEATON
        verde_peaton.on()
        sleep(0.5)
        verde_peaton.off()
        sleep(0.5)
        i=i+1

def reposo(t):
    timer3.deinit()
    lcd.clear()
    print("STOP peatones.Pulse para pasar")
    lcd.message("STOP peatones. \nPulse para pasar")
    rojo.off()
    verde.on()
    ama.off()
    verde_peaton.off()
    rojo_peaton.on()
    

#MENSAJE AL INICIAR SISTEMA
lcd.clear()
print("SEMÁFORO ON. Pulse para pasar")
lcd.message("SEMAFORO ON.\nPulse para pasar")

#ACTIVACION DE SECUENCIA AL PULSAR EL BOTON
while True:
    if S1.value()==1:
        timer0.init(period=4000,mode=Timer.ONE_SHOT,callback=ambar)
        lcd.clear()
        print("Petición de paso peatones")
        lcd.message("Peticion de paso \npeatones")
        sleep(0.5)



