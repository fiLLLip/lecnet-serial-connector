from pylibftdi import Device, USB_PID_LIST, USB_VID_LIST

USB_VID_LIST.append(0x1321)
USB_PID_LIST.append(0x1001)

dev = Device(mode='t')
dev.baudrate = 57600
dev.open()
cmd = 'serial?'
while cmd != 'quit':
    if cmd != '':
        dev.flush_input()
        dev.writelines(cmd + '\r')
    out = ''
    while out == '':
        out = dev.readline()
    print(out)
    cmd = input('Type command: ')
