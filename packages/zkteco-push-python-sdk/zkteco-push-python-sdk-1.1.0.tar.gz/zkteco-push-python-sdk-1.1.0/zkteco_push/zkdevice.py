import logging
import base64

from zkteco_push.zklog import ZKLog
from zkteco_push.ZKTECO_HELPERS import zkteco_format_image, normalize_pin


CONVERT_B64 = False
class ZKDevice:
    def __init__(self, serial_number, options, version, device_type, language, pushcommkeys):
        ''' Application parameters '''
        
        self.attlog_stamp = 0
        self.operlog_stamp = 0
        self.attphoto_stamp = 0
        self.biodata_stamp = 0
        self.idcard_stamp = 0
        self.errorlog_stamp = 0 
        
        ''' Device details '''
        self.serial_number = serial_number
        self.options = options
        self.version = version
        self.device_type = device_type
        self.language = language
        self.pushcommkeys = pushcommkeys
        
        self.users = []
        
         
        ''' Application informations '''
        self.is_initialized = False
        self.number_of_users = 0
        
        ''' Command related variables '''
        self.commands_list = []
        

    ''' Commands to initialize device '''
    def initialize(self):
        self.is_initialized = True
        body_content = '''GET OPTION FROM:%s
ATTLOGStamp=%s
OPERLOGStamp=%s
ATTPHOTOStamp=%s
ERRORLOGStamp=%s
ErrorDelay=300
Delay=30
TransTimes=00:00;24:00
TransInterval=1
TransFlag=AttLog    OpLog   AttPhoto    EnrollUser  ChgUser EnrollFP    ChgFP   Userpic
TimeZone=2
Realtime=1
Encrypt=0
ServerVer=2.2.14
PushProtVer=2.2.14
PushOptionsFlag=1
PushOptions=UserCount,TransactionCount,FingerFunOn,FPVersion,FPCount,FaceFunOn,FaceVersion,FaceCount,FvFunOn,FvVersion,FvCount,PvFunOn,PvVersion,PvCount,BioPhotoFun,BioDataFun,PhotoFunOn,~LockFunOn,CardProtFormat,~Platform,MultiBioPhotoSupport,MultiBioDataSupport,MultiBioVersion,MaskDetectionFunOn
''' % (self.serial_number,
       self.attlog_stamp if self.attlog_stamp > 0 else "None",
       self.operlog_stamp if self.operlog_stamp > 0 else "None",
       self.attphoto_stamp if self.attphoto_stamp > 0 else "None",
       self.errorlog_stamp if self.errorlog_stamp > 0 else "None")

        return 200, body_content
    
    def configure_device(self):
        ''' Configure device'''
        #TODO #3 Set language
        #TODO #2 split in multiple calls
        cmd = []
        cmd.append("SET OPTION Language=%s" % self.language if self.language else 69)
        cmd.append("SET OPTION IRTempDetectionFunOn=1")
        cmd.append("SET OPTION MaskDetectionFunOn=1")
        cmd.append("SET OPTION EnableIRTempDetection=0")
        cmd.append("SET OPTION EnableMaskDetection=0")
        cmd.append("SET OPTION DeviceType=%s" % self.device_type if self.device_type else "att")
        cmd.append("SET OPTION VOLUME=30")
        return cmd
    
    def reload_options(self):
        ''' Configure device'''
        #TODO #3 Set language
        #TODO #2 split in multiple calls
        cmd = []
        cmd.append("RELOAD OPTIONS")
        return cmd
    
    def push_user_data(self, employee_ids):
        #TODO #4 Convert to api user_id
        cmd = []
        for employee_id in employee_ids:
            cmd.append("DATA UPDATE USERINFO PIN=%s\tName=%s\tPri=%s\tPasswd=%s\tGrp=%s\tTZ=%s\tVerify=%s\tCard=%s\n" % (normalize_pin(employee_id.registration_number),
                                                                                                                         employee_id.name,
                                                                                                                         employee_id.zk_privilege,
                                                                                                                         employee_id.pin,
                                                                                                                         0, 2, 0,None))
       
        return cmd

    def push_user_biodata(self, employeee_ids):
        cmd = []
        for employee_id in employeee_ids:
            index=0
            for biodata in employee_id.biodata_ids:
                # img = base64.b64encode(biodata.template).decode('utf-8') if CONVERT_B64 else biodata.template.decode('utf-8')
                try:
                    img = zkteco_format_image(biodata.template) 
                except Exception as e:
                    return None
                cmd.append("DATA UPDATE BIODATA Pin=%s\tNo=0\tIndex=%s\tValid=%s\tDuress=%s\tType=%s\tMajorVer=%s\tMinorVer=%s\tFormat=%s\tTmp=%s" % (normalize_pin(employee_id.registration_number),
                                                                                                                                                      index,
                                                                                                                                                      biodata.validity,
                                                                                                                                                      biodata.duress,
                                                                                                                                                      biodata.type,
                                                                                                                                                      biodata.major_version,
                                                                                                                                                      biodata.minor_version,
                                                                                                                                                      biodata.format,
                                                                                                                                                      img))
                index +=1
        return cmd 
    
    def push_user_biophoto(self, employeee_ids):
        cmd = []
        for employee_id in employeee_ids:
            index=0
            for biodata in employee_id.biodata_ids:
                # img = base64.b64encode(biodata.template).decode('utf-8') if CONVERT_B64 else biodata.template.decode('utf-8')
                img = zkteco_format_image(biodata.template)
                size = len(img)
                cmd.append("DATA UPDATE BIOPHOTO PIN=%s\tType=%s\tSize=%s\tContent=%s\tFormat=0\tPostBackTmpFlag=0" % (normalize_pin(employee_id.registration_number),
                                                                                                                        biodata.type,
                                                                                                                        size,
                                                                                                                        img))
                index +=1
        return cmd 
    
    def push_user_face(self, employeee_ids):
        cmd = []
        for employee_id in employeee_ids:
            index=0
            for biodata in employee_id.biodata_ids:
                # img = base64.b64encode(biodata.template).decode('utf-8') if CONVERT_B64 else biodata.template.decode('utf-8')
                img = zkteco_format_image(biodata.template)
                size = len(img) 
                cmd.append("DATA UPDATE FACE PIN=%s\tFID=%s\tValid=%s\tSize=%s\tTMP=%s" % (normalize_pin(employee_id.registration_number),
                                                                                           index,
                                                                                           biodata.validity,
                                                                                           size,
                                                                                           img))
                index +=1
        return cmd 
    
    def push_user_photo(self, employeee_ids):
        cmd = []
        for employee_id in employeee_ids:
            if employee_id.image_1920:
                img = zkteco_format_image(employee_id.image_1920) 
                size = len(img) 
                cmd.append("DATA UPDATE USERPIC PIN=%s\tSize=%s\tContent=%s" % (normalize_pin(employee_id.registration_number),
                                                                                size,
                                                                                img))
        return cmd 
    
    def delete_user_data(self, user_ids):
        cmd = []
        if isinstance(user_ids, str):
            cmd.append("DATA DELETE USERINFO PIN=%s" % normalize_pin(user_ids))
        else:
            for user_id in user_ids:
                cmd.append("DATA DELETE USERINFO PIN=%s" % normalize_pin(user_id))
        return cmd
     
    def set_options(self, options):
        ''' Set device options'''
        #TODO save options
        logging.debug("TODO set_option not implemented")
        return 200, "OK"
    
    def set_infos(self, infos):
        ''' Set device infos'''
        #TODO save infos cfr 9. Uploading Update information
        logging.debug("TODO set_infos not implemented")
        return 200, "OK"
    
    ''' Commands to operate device '''
    def reboot(self):
        ''' Reboot device'''
        return ["REBOOT"]
    
    def clear_device_data(self):
        return ["CLEAR DATA"]
    
    ''' Commands to manipulate data '''
    def zk_build_command(self, command_id, command, args=None):
        ''' Build command to send to device'''
        return_cmd = None
        if command == "update_userpic":
            ''' Define the User Photo '''
            face_count = 0
            for face in args.faces:
                b64_image =base64.b64encode(face).decode("utf-8") #Not working
                b64_image = face
                #Not Working
                return_cmd = "C:%s:DATA UPDATE USERPIC PIN=%s\tSize=%s\tContent=%s\n" % (command_id,
                                                                                          normalize_pin(args.user_id),
                                                                                          str(len(b64_image)),
                                                                                          b64_image)
                                                                     
                face_count += 1
            
        elif command == "update_face":
            face_count = 0
            for face in args.faces:
                b64_image =base64.b64encode(face).decode("utf-8") #Not working
                b64_image = face #Not Working
                return_cmd = "C:%s:DATA UPDATE FACE PIN=%s\tFID=%s\tValid=1\tSize=%s\tTMP=%s\n" % (command_id,
                                                                                                   normalize_pin(args.user_id),
                                                                                                   face_count,
                                                                                                   str(len(b64_image)),
                                                                                                   b64_image)
                                                                     
                face_count += 1
        elif command == "update_biodata":
            face_count = 0
            for face in args.faces:
                b64_image =base64.b64encode(face).decode("utf-8")
                # b64_image =face.decode("utf-8")
                return_cmd = "C:%s:DATA UPDATE BIODATA Pin=%s\tNo=0\tIndex=%s\tValid=1\tDuress=0\tType=9\tMajorVer=58\tMinorVer=12\tFormat=0\tTmp=%s" % (command_id,
                                                                                                                                                           normalize_pin(args.user_id),
                                                                                                                                                           face_count,
                                                                                                                                                           b64_image)
                                                                     
                face_count += 1
        elif command == "update_biophoto":
            face_count = 0
            for face in args.faces:
                b64_image =base64.b64encode(face).decode("utf-8")
                return_cmd = "C:%s:DATA UPDATE BIOPHOTO PIN=%s\tType=9\tSize=%s\tContent=%s\tFormat=0\tPostBackTmpFlag=0\n" % (command_id,
                                                                                                                               normalize_pin(args.user_id),
                                                                                                                               str(len(b64_image)),
                                                                                                                               b64_image)
                                                                     
                face_count += 1
            
        elif command == "reload":
            '''Reload options'''
            return_cmd = "C:%s:RELOAD OPTIONS" % command_id
        elif command == "reboot":
            '''Reboot device'''
            return_cmd = "C:%s:REBOOT" % command_id
        elif command == "clear":
            ''' Clear all device data '''
            return_cmd = "C:%s:CLEAR DATA" % command_id
        else:
            logging.debug("Unknown build_command request: %s", command)
        return return_cmd
    
    def zk_process_logs(self, stamp, logs):
        items = 0
        zk_logs = []
        for log in logs:
            if len(log) == 0:
                break
            # Check that log starts with OPLOG
            if log.startswith("OPLOG"):
                logging.debug("Log %s" % log)
                # Extract prefix OPLOG
                zk_logs.append(ZKLog(log[6:], self))
                items += 1
            else:
                raise Exception("Log not recognized")
        return 200, "OK: %s" % items, zk_logs
    
    def add_user(self, user):
        self.users.append(user)

    def remove_user(self, user):
        self.users.remove(user)
            
        
        
    
        