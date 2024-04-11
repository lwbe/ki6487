from get_new_usb_devices import get_current_devices_list, get_dev_path_from_pid_vid_sn
import re

import logging
from logtools import create_logger

mylogger = create_logger(log_name="confstring",log_level=logging.DEBUG)

class ConfStringL(object):
    """
    lighweight confstring typically pid=xxxx,vid=yyyyy,sn=zzzzz,baudrate=cccc,....
    """
    def __init__(self, confstring,confstring_def={}):
        print("In init")
        mylogger.debug("in __init__")
        self.conf_as_dict={}
        for k,v in [i.split("=",maxsplit=1) for i in confstring.split(",")]:
            if confstring_def.get(k):                
                v = confstring_def.get(k)(v)
                    
            self.conf_as_dict.update(((k,v),))

    def get_conf(self):
        return self.conf_as_dict



if __name__ == "__main__":
    # we should show some example
    print(ConfStringL("a=b,c=d,e=f").get_conf())
