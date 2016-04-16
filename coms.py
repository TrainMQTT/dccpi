import pigpio

# setup py ip port and gpio pins
pi = pigpio.pi("127.0.0.1", 8888)
G1 = 18 # Wave pin 18=pin 12
G2 = 17 # On off pin 17=pin 11

pi.set_mode(G1, pigpio.OUTPUT)
pi.set_mode(G2, pigpio.OUTPUT)

waves = []
cleanup_waves = []
wave_data = {}
no_op = []
idle_wave_id = None
idle_wave_data = None

def turn_on():
    pi.write(G2, 1)

def turn_off():
    pi.write(G2, 0)

def clear():
    pi.wave_clear()

def reset():
    global cleanup_waves, waves
    cleanup_waves = waves
    waves = []

def add_wave(data):
    global waves
    wave_id = encode(data)
    wave_data[wave_id] = data
    waves.append(wave_id)

def encode(data):
    wave = []
    for bit in data:
        #print bit
        if bit == "0":
            write_zero(wave)
        else:
            write_one(wave)
    pi.wave_add_generic(wave)
    wave_id = pi.wave_create()
    #print "Wave id %d" % wave_id
    return wave_id

def send_waves():
    print idle_wave_id
    output = [255, 0]
    output.extend(waves)
    output.extend([255, 1, 10, 0])
    if idle_wave_id is not None:
        output.extend([255, 0])
        output.extend([idle_wave_id])
        output.extend([255, 3])
    print output
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

