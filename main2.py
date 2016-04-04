import pigpio
from bitstring import BitArray

pi = pigpio.pi("10.0.0.112", 8888)

G1 = 13
G2 = 18

pi.set_mode(G1, pigpio.OUTPUT)
pi.set_mode(G2, pigpio.OUTPUT)

pi.wave_tx_stop()
pi.wave_clear()

flash_500 = []  # flash every 500 ms

flash_500.append(pigpio.pulse(1 << G1, 1 << G2, 500000))
flash_500.append(pigpio.pulse(1 << G2, 1 << G1, 500000))

pi.wave_clear()  # clear any existing waveforms
pi.wave_add_generic(flash_500)  # 500 ms flashes
f500 = pi.wave_create()  # create and save id
pi.wave_send_repeat(f500)

raw_input("Press Enter to continue...")

pi.wave_tx_stop()  # stop waveform
pi.wave_clear()  # clear all waveforms