
import serial
import re
from get_new_usb_devices import get_current_devices_list, get_dev_path_from_pid_vid_sn
from confstring import ConfStringL


import logging
from logtools import create_logger
mylogger=create_logger(log_name="communication_device",log_level=logging.DEBUG)




class UsbSerial(object):
    confstring_def={
        "pid":int,
        "vid":int,
        "baudrate":int,
        "timeout":int,
        }
    
    def __init__(self, confstring_l):
        # analyse the confstring
        mylogger.debug("__init__")
        conf = ConfStringL(confstring_l, self.confstring_def).get_conf()
        pid = conf.pop("pid")
        vid = conf.pop("vid")
        sn = conf.pop("sn")
        if sn == "None":
            sn = None

        device_path = get_dev_path_from_pid_vid_sn(pid,vid,sn,get_current_devices_list())
        print(f"device path {device_path}")

        # configure the device
        self.device = serial.Serial(device_path,**conf)


    def _write(self,string):
        mylogger.debug("write %s " % str(string))
        self.device.write(string)

    def _read(self):
        mylogger.debug("read")
        return self.device.readline()

    def _query(self,string):
        mylogger.debug("query")
        self._write(string)
        return self._read()


class UsbPrologix(UsbSerial):

    def __init__(self, confstring):
        super().__init__(confstring)

    def init(self):
        self.device.write(b"++auto 0\n")
        
    def _write(self,string):
        self.device.write(string)

    def _read(self):
        self.device.write(b"++read eoi\n")
        return self.device.readline()

    def _query(self,string):
        self._write(string)
        return self._read()
    
    def dump_configuration(self):
        for kw in ("addr", "eoi", "eos", "eot_enable", "eot_char", "mode","ver"):
            print(kw, self._query(("++%s\n" % kw).encode()))
    
    
class CommDevice(object):
    def __init__(self, confstring):
        mylogger.debug("__init__"+confstring)

        comm_device_type, comm_confstring = re.search("([^(]*)\((.*)\)",confstring).groups()
        
        if comm_device_type == "usbserial":
            self.comm_device = UsbSerial(comm_confstring)
        elif comm_device_type == "usb_prologix":
            self.comm_device = UsbPrologix(comm_confstring)
        else:
            raise Exception("commnunication protocol {comm_device_type} not implemented")
        
        self._write = self.comm_device._write
        self._read = self.comm_device._read
        self._query = self.comm_device._query

    def init_device(self):
        print("not implemented for this device")
                  
    def dump_configuration(self):
        if hasattr(self.comm_device,"dump_configuration"):
            self.comm_device.dump_configuration()
        else:
            print("not implemented for this device")
