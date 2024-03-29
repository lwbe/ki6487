import serial.tools.list_ports


def get_info_from_device_path(device_paths, devices):
    r=[]
    for i in device_paths:
        for d in devices:
            if d.device_path == i:
                r.append({"device":d.device,
                          "pid":d.pid,
                          "vid":d.vid,
                          "sn":d.serial_number})
    return r

previous_devices = [p for p in serial.tools.list_ports.comports()]
previous_dev_path = [p.device_path for p in previous_devices]

input('press return when new device is inserted or removed')
new_devices = [p for p in serial.tools.list_ports.comports()]
new_dev_path = [p.device_path for p in new_devices]

tmp = previous_dev_path[:]

for i in previous_dev_path:
    if i in new_dev_path:
        new_dev_path.remove(i)
        tmp.remove(i)

if tmp:
    print("Removed device ")
    
    for d in get_info_from_device_path(tmp, previous_devices):
        print("--")
        for k, v in d.items():
            print(f"\t{k} : {v}")


if new_dev_path:
    print("Added device ")
    for d in get_info_from_device_path(new_dev_path, new_devices):
        print("--")
        for k, v in d.items():
            print(f"\t{k} : {v}")
