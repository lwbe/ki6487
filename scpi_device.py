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
        "idn": {
            "cmd_string": "*IDN?"   , "type": "query", },
        "rst":{
            "cmd_string": "*RST"    , "type": "write", },
        }
    alias = {
        "get_ident" : "idn",
        }
    
    device_commands = {}
    device_alias = {}
    
    def __init__(self, confstring):
        mylogger.debug("__init__"+confstring)
        self.EOT="\r\n"
        self.commands.update(self.device_commands)
        self.alias.update(self.device_alias)
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
    

    def _create_function(self,name):
        """
        Return a function to be executed created on the fly 
        """
        
        func_def = self.commands[name]
        if func_def["type"]=="query":
            function_to_execute = self._query
        elif func_def["type"]=="write":
            function_to_execute = self._write

        if "<n>" in func_def["cmd_string"]:
            string_to_send = func_def["cmd_string"].replace("<n>","%d")
        else:
            string_to_send = func_def["cmd_string"]
        mylogger.debug("string for command %s (type %s) is %s"% (name,func_def["type"],string_to_send))
        def f(*args):
            return function_to_execute(string_to_send % args)
        return f

    def __getattr__(self,kc):
        """
        Overriding the base function __getattr__ from the python class to create a function on the fly
        in looking in dictionnaries self.commands and self.aliases
        """
        mylogger.debug("in __getattr__ %s"% (kc))
        if kc in self.alias.keys():
            kc = self.alias[kc]

        if kc in self.commands.keys():
            return self._create_function(kc)
        else:
            print("Available functions")
            print(", ".join(self.commands.keys()))
            print(",".join([func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__")]))
            raise AttributeError("%s is not an attibute of the class %s" % (kc,self.__class__.__name__))
