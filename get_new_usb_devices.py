import serial.tools.list_ports


def get_current_devices_list():
    return [p for p in serial.tools.list_ports.comports()]
    
def get_info_from_device_path(device_paths, devices):
    """
    extract data form serial.tools.list_ports for certain device path (ex /sys/devices/pci0000:00/0000:00:14.0/usb1/1-10/1-10:1.0/ttyUSB0
)
    """
    r=[]
    for i in device_paths:
        for d in devices:
            if d.device_path == i:
                r.append({"device":d.device,
                          "pid":d.pid,
                          "vid":d.vid,
                          "serial_number":d.serial_number,
                          "manufacturer":d.manufacturer})
    return r

def get_dev_path_from_pid_vid_sn(pid,vid,serial_number,devices):

    for d in devices:
        if pid:
            if pid != d.pid:
                continue
        if vid:
            if vid != d.vid:
                continue
        if serial_number:
            if serial_number != d.serial_number:
                continue
        return d.device
    return None
            
def print_info(device_data):
    for i,d in enumerate(device_data):
        print("device %d" % i)
        for k, v in d.items():
            print(f"\t{k} : {v}")
                


if __name__ == "__main__":

    # get a list of device and extract the device path which is unique
    previous_devices = get_current_devices_list()
    previous_dev_path = [p.device_path for p in previous_devices]

    input('press return when new device is inserted or removed')

    # get a list of device after plug in or out a device and extract the device path which is unique
    new_devices = get_current_devices_list()
    new_dev_path = [p.device_path for p in new_devices]


    # compare the two lists and extract the difference
    tmp = previous_dev_path[:]

    for i in previous_dev_path:
        if i in new_dev_path:
            new_dev_path.remove(i)
            tmp.remove(i)

    # print if one device has been removed
    if tmp:
        print("REMOVED device ")
        data = get_info_from_device_path(tmp, previous_devices)
        print_info(data)
        if data:
            for d in data:
                found_path = get_dev_path_from_pid_vid_sn(d["pid"],d["vid"],d["serial_number"],previous_devices)
                print(d,found_path)
    # or 
    if new_dev_path:
        print("ADDED device ")
        data = get_info_from_device_path(new_dev_path, new_devices)
        print_info(data)
        if data:
            for d in data:
                found_path = get_dev_path_from_pid_vid_sn(d["pid"],d["vid"],d["serial_number"],new_devices)
                print(d,found_path)



    print(get_dev_path_from_pid_vid_sn(8200,1367,"",previous_devices))
    print(get_dev_path_from_pid_vid_sn(8200,1367,"",new_devices))

