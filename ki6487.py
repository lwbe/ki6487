from get_new_usb_devices import get_current_devices_list, get_dev_path_from_pid_vid_sn
import serial
import re



class ConfStringL(object):
    """
    lighweight confstring typically pid=xxxx,vid=yyyyy,sn=zzzzz,baudrate=cccc,....
    """
    def __init__(self, confstring,confstring_def={}):
        
        self.conf_as_dict={}
        for k,v in [i.split("=",maxsplit=1) for i in confstring.split(",")]:
            if confstring_def.get(k):                
                v = confstring_def.get(k)(v)
                    
            self.conf_as_dict.update(((k,v),))
        print(self.conf_as_dict)

    def get_conf(self):
        return self.conf_as_dict



class UsbSerial(object):
    confstring_def={
        "pid":int,
        "vid":int,
        "baudrate":int,
        "timeout":int,
        }
    def __init__(self, confstring_l):
        # analyse the confstring
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


    def _send(self,string):
        pass

    def __receive(self):
        return "OK"




class ki6487(object):
    def __init__(self, confstring):

        comm_device_type, comm_confstring = re.search("([^(]*)\((.*)\)",confstring).groups()
        
        if comm_device_type == "usbserial":
            self.comm_device = UsbSerial(comm_confstring)
        else:
            raise Exception("commnunication protocol {comm_device_type} not implemented")
        



        
        
if __name__ == "__main__":
    
    k = ki6487("usbserial(pid=8200,vid=1367,sn=None,baudrate=57600,timeout=1)")
