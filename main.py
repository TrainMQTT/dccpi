import pigpio
import time

pi = pigpio.pi("10.0.0.112", 8888)

G1 = 13
G2 = 18

pi.set_mode(G1, pigpio.OUTPUT)
pi.set_mode(G2, pigpio.OUTPUT)

waves = []
cleanup_waves = []
wave_data = {}


def clear():
    pi.wave_clear()


def reset():
    global cleanup_waves, waves
    #pi.wave_tx_stop()
    #pi.wave_clear()
    cleanup_waves = waves
    waves = []


def add_wave(data):
    wave = []
    for bit in data:
        if bit == "0":
            write_zero(wave)
        else:
            write_one(wave)

    pi.wave_add_generic(wave)
    ft = pi.wave_create()
    waves.append(ft)
    wave_data[ft] = data
    return ft
    #pi.wave_send_repeat(ft)


def send_waves():
    output = [255, 0]
    output.extend(waves)
    output.extend([255, 3])
    pi.wave_chain(output)
    do_cleanup()


def do_cleanup():
    for wave in cleanup_waves:
        pi.wave_delete(wave)


def write_zero(wave):
    wave.append(pigpio.pulse(1 << G1, 0, 100))
    wave.append(pigpio.pulse(0, 1 << G1, 100))


def write_one(wave):
    wave.append(pigpio.pulse(1 << G1, 0, 58))
    wave.append(pigpio.pulse(0, 1 << G1, 58))

