from communication_device import CommDevice

import logging
from logtools import create_logger

mylogger=create_logger(log_name="scpi_device",log_level=logging.DEBUG)


class SCPIDevice(object):

    # commands is a dictionary to map easily SCPI strings to methods of the class.
    # A typical entry is
    #     method_name : {
    #                     "cmd_string": the string that will be send to the device,
    #                     "type": either query or write
    #   }
    # the idea is to parse the "cmd_string" to define the variable that are expected or optionnal
    # for clarity the best is to write the full 

    # for the device module it should be named extra_command
    commands ={
        "idn"       : {"cmd_string": "*IDN?"   , "type": "query", },
        "rst"     : {"cmd_string": "*RST"    , "type": "write", },
        }
    
    extra_commands = {}
    
    def __init__(self, confstring):
        mylogger.debug("__init__"+confstring)
        self.EOT="\r\n"
        self.commands.update(self.extra_commands)
        self.comm_device = CommDevice(confstring)


    def flush(self):
        """
        function to be implemented specifically for each device
        """
        return 0,"flushed"

    def sanitize(self,input_string):
        return input_string
    
        
    def _write(self,data_to_send):
        self.comm_device._write(self.sanitize(data_to_send))
        return
    
    def _read(self):
        return self.comm_device._read()

    def _query(self,data_to_send):
        self.write(data_to_send)
        return self.read()
    

