from urllib.parse import urlparse, parse_qs
import http.server
import logging
import base64

from zkteco_push.zkdevice import ZKDevice
from zkteco_push.zkuser import ZKUser
from zkteco_push.zklog import ZKLog
import os

class ZKRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.zk_devices = []

        test_user = ZKUser(
            2,
            "Xavier Mukalamushi",
            "1234",
            "14",
            [self.load_image("../xm-user-1.png")],
        )
        
        self.command_list = {
    'CKJE202260085': [
        # {'cmdId': 'CMD0001', 'cmd': 'configure_machine'},
        # {'cmdId': 'CMD0003', 'cmd': 'reload'},
        # {'cmdId': 'CMD0010', 'cmd': 'reboot'},
        # {'cmdId': 'CMD0050', 'cmd': 'update_userinfo', 'user': test_user},
        # {'cmdId': 'CMD0051', 'cmd': 'update_userpic', 'user': test_user}, #Not Working
        # {'cmdId': 'CMD0052', 'cmd': 'update_face', 'user': test_user},
        {'cmdId': 'CMD0053', 'cmd': 'update_biodata', 'user': test_user},
        # {'cmdId': 'CMD0054', 'cmd': 'update_biophoto', 'user': test_user},
    ]
}

        super().__init__(*args, **kwargs)

    def load_image(self, filename):
        image_path = os.path.join(os.path.dirname(__file__), filename)
        # with open(image_path, "rb") as image_file:
        #     encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        # return encoded_string

        image_file = open(image_path, "rb")
        image_data = image_file.read()
        image_file.close()
        return image_data
        
    def add_device(self, device):
        self.zk_devices.append(device)

    def remove_device(self, device):
        self.zk_devices.remove(device)
    
    def get_device(self, serial_number):
        ''' Get a device by serial number '''
        return next((zk_device for zk_device in self.zk_devices if zk_device.serial_number == serial_number), None)
        

    
    def zk_parse_request(self):
        parsed_url = urlparse(self.path)
        if "iclock" in parsed_url.path:
            
            command = parsed_url.path.split("/iclock/")[1]
            query_params = parse_qs(parsed_url.query)
            serial_number = query_params.get('SN', [None])[0]
            options = query_params.get('options', [None])[0]
            version = query_params.get('pushver', [None])[0]
            device_type = query_params.get('DeviceType', [None])[0]
            language = query_params.get('langage', [None])[0]
            pushcommkeys = query_params.get('pushcommkey', [None])[0]
            
            #If a ZkDevice with this serial number exists in zk_devices list, get its ZKMachine object in zk_device_field, otherwise instantiate a new ZKMachine object, add it to the list, and return its instance
            zk_device = next((zk_device for zk_device in self.zk_devices if zk_device.serial_number == serial_number), None)
            if zk_device is None:
                zk_device = ZKDevice(self, serial_number,
                                     options, version,
                                     device_type, language, pushcommkeys)
                self.add_device(zk_device)
                
            return zk_device, command, query_params
        else:
            return None
    
    def zk_send_response(self, code=200, content=None):
        self.send_response(code)
        self.send_header("Content-type", "text/plain")
        if content is not None:
            self.send_header("Content-length", len(content))
        self.end_headers()
        if content is not None:
            self.wfile.write(content.encode())
        logging.debug("Response sent %s - %s" %(code, content))
        
        
    def do_GET(self):
        # Process GET requests
        # Read self.path depending on value perform action.
        # In case path do not represent anything known, write in console and continue
        try:
            zk_device, command, params = self.zk_parse_request()
        except Exception as e:
            print(f"Error found: {e}")
            command = None
        
        if command is None:
            # Will write log and ignore it
            print(f"This is not a zkteco command: {self.path}")
            pass
        else:
            code = None
            response = None
            if command == "cdata":
                if not zk_device.is_initialized:
                    code, response = zk_device.initialize()
                else:
                    table = params.get('table', [None])[0]
                    pass
            elif command == "getrequest":
                
                infos = params.get('INFO', [None])[0].split(",") if params.get('INFO', [None])[0] is not None else None
                if infos:
                    code, response = zk_device.set_infos(infos)
                else:
                    zk_commands = []
                    for zk_command in self.command_list[zk_device.serial_number]:
                        new_cmd = zk_device.zk_build_command(zk_command['cmdId'], zk_command['cmd'], zk_command['user'])
                        if new_cmd:
                            zk_commands.append(new_cmd)
                    if len(zk_commands):
                        code = 200
                        response = "\n".join(zk_commands)
                    else:
                        code = 200
                        response = "OK"
            elif command == "ping":
                code = 200
                response = "OK"
            else:
                # Will write log but acknowledge the request
                print(f"Unknwon command: {command}")
                self.zk_send_response()
            
            if code is not None:
                self.zk_send_response(code, response)
                

    def do_POST(self):
        # Process POST requests
        # Read self.path depending on value perform action.
        # In case path do not represent anything known, write in console and continue
        zk_device, command, params = self.zk_parse_request()
        
        
        if command is None:
            # Will write log and ignore it
            print(f"Command Not recognized: {self.path}")
        else: 
            code = None
            response = None
            if command == "cdata":
                table = params.get('table', [None])[0]
                if table == "options":
                    ''' Client pushes its configuration from request content'''
                    options =  self.rfile.read(int(self.headers['Content-Length'])).decode().split(",")
                
                    code, response = zk_device.set_options(options)
                elif table == "OPERLOG":
                    stamp = params.get('Stamp', [None])[0]
                    logs = self.rfile.read(int(self.headers['Content-Length'])).decode().split("\n")
                    code, response, zk_logs = zk_device.zk_process_logs(stamp, logs)
                else:
                    print(f"Unknwon command: {command}")
                    # self.zk_send_response()
            elif command == "devicecmd":
                #TODO implement devicecmd
                code = 200
                response = "OK"
            else:
                logging.debug("Command not defined %s" % command)
                
            if code is not None:
                self.zk_send_response(code, response)
                
                
                    
