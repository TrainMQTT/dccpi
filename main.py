import pigpio
import time

pi = pigpio.pi("10.0.0.112", 8888)

G1 = 13
G2 = 18

pi.set_mode(G1, pigpio.OUTPUT)
pi.set_mode(G2, pigpio.OUTPUT)

def writeData(data):
    wave = []
    for bit in data:
        #print bit
        if bit == "0":
            writeZero(wave)
        else:
            writeOne(wave)
    pi.wave_tx_stop()
    pi.wave_clear()
    pi.wave_add_generic(wave)
    ft = pi.wave_create()
    pi.wave_send_repeat(ft)

def writeZero(wave):
    wave.append(pigpio.pulse(1 << G1, 0, 100))
    wave.append(pigpio.pulse(0, 1 << G1, 100))

def writeOne(wave):
    wave.append(pigpio.pulse(1 << G1, 0, 58))
    wave.append(pigpio.pulse(0, 1 << G1, 58))

