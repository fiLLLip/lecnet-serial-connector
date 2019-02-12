import paho.mqtt.client as mqtt
import json
from pylibftdi import Device, USB_PID_LIST, USB_VID_LIST

USB_VID_LIST.append(0x1321)
USB_PID_LIST.append(0x1001)

dev = Device(mode='t')
dev.baudrate = 57600
dev.open()


def run_command(cmd):
    if cmd != '':
        dev.flush()
        print('TX: ' + cmd)
        dev.writelines(cmd + '\r')
        out = ''
        while out == '':
            out = dev.readline()
        print('RX: ' + out)


def to_command(obj):
    cmds = []
    for input in obj:
        cmd = 'xpgn(' + input + ',*)='
        # print('Input: ' + input)
        # print(obj[input])
        vals = []
        for output in range(1, 24+1):
            # print('Output: ' + output + ', Volume: ' + str(obj[input][output]))
            vals.append(str(obj[input][str(output)]))
        cmd += '{' + ','.join(vals) + '}'
        cmds.append(cmd)
    return cmds


def handle_message(message):
    obj = (json.loads(str(message.payload.decode("utf-8"))))
    cmds = to_command(obj)
    for cmd in cmds:
        run_command(cmd)

def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)
    handle_message(message)
    
def on_connect(client, userdata, flags, rc):
    client.subscribe('lecnet')

client = mqtt.Client()
client.on_message = on_message
client.connect('192.168.12.58')

run_command('serial?')
for val in range(1, 16+1):
    cmd = 'xpmode(' + str(val) + ',*)='
    cmd += '{' + ','.join(['1'] * 24) + '}'
    run_command(cmd)

run_command('ingn(*)={-5,-5,-5,-5,-5-,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5}')

client.loop_forever()
