from scpi_device import SCPIDevice        

import logging
from logtools import create_logger
mylogger=create_logger(log_name="ki6487",log_level=logging.DEBUG)

class ki6487(SCPIDevice):


    # commands is a dictionary to map easily SCPI strings to methods of the class.
    # beware that scpi class also provides a base commands (for typical command like *IDN? or *CLS)
    # and you should check to avoir reimplementing it. They can be overrides here if you need.
    # A typical entry is
    #     method_name : {
    #                     "cmd_string": the string that will be send to the device,
    #                     "type": either query or write
    #   }
    # the idea is to parse the "cmd_string" to define the variable that are expected or optionnal
    # for clarity the best is to write the full 

    device_commands = {
        "read":{
            "cmd_string": "READ?"           , "type": "query", },
        "trac_cle":{
            "cmd_string": "TRAC:CLE"        , "type": "query", },
        "trace_usage":{
            "cmd_string": "TRAC:FREE"       , "type": "query", },
        "trace_set_point":{
            "cmd_string": "TRAC:POIN <n>"   , "type": "write", },
        }
    device_alias={
        "TRAC:CLE" : "trace_clear_readings",
    }

    def __init__(self,confstring):
        super(ki6487,self).__init__(confstring)
        self.MAX_COUNT = 2        
        # flush the msg queue
        self.check_errors()

    def sanitize(self, input_string):
        if type(input_string) == type("a"):
            return (input_string+self.EOT).encode()
        return input_string+self.EOT.encode()
    
    def check_errors(self):
        DO_CHECK = True
        err_msg = []
        while DO_CHECK:
            self.comm_device._write(self.sanitize("SYST:ERR?"))
            res = self.comm_device._read().decode().strip().split(",")
            if len(res) == 2:
                if res[0] == '0':
                    DO_CHECK=False
                else:
                    err_msg.append(", ".join([str(i) for i in res]))
            else:
                err_msg.append("got strange data %s" % str(res))
        if err_msg:
            return -1,";".join(err_msg)
        return 0,"OK"

    def _write(self,data_to_send):
        mylogger.debug("%s -> %s"% (data_to_send,str(self.sanitize(data_to_send))))
        self.comm_device._write(self.sanitize(data_to_send))
        self.comm_device._read()
        err_status, err_response = self.check_errors()
        if err_status:
            return -1,f"got error {err_status} {err_response}"
        else:
            return 0,"ok"
        
    def _query(self,data_to_send):
        mylogger.debug("%s -> %s"% (data_to_send,str(self.sanitize(data_to_send))))
        self.comm_device._write(self.sanitize(data_to_send))
        response = self.comm_device._read()
        count = 0
        while not response and count < self.MAX_COUNT:
            print("response", response)
            count += 1
            response = self.comm_device._read()
        if count == self.MAX_COUNT:
            return -1,f"timeout while trying to receive data from the query {data_to_send}"

        err_status, err_response = self.check_errors()
        if err_status:
            return -1,f"got error {err_status} {err_response}"
        else:
            return 0,response.decode().strip()




class ki6487_acq(ki6487):

    def init(self):
        print(self.idn())
        print(self.get_ident())


    
        
if __name__ == "__main__":

    
    k = ki6487_acq("usb_prologix(pid=24577,vid=1027,sn=None,baudrate=57600,timeout=10)")
    print(k.init())
              
    
