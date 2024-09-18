import datetime
from zkteco_push.ZKTECO_CONST import ZKTECO_OPERATION_CODES
from zkteco_push.ZKTECO_HELPERS import resolve_zkteco_codes
 
class ZKLog:
    def __init__(self, log, zk_machine_id):
        vals = log.split('\t')
        self.name = resolve_zkteco_codes(ZKTECO_OPERATION_CODES, vals[0])
        self.zk_machine_id = zk_machine_id
        self.table = "OPLOG"
        self.date = datetime.datetime.strptime(vals[2], "%Y-%m-%d %H:%M:%S")
        #TODO Convert time in UTC
        self.operation_type = vals[0]
        self.alarm_cause = vals[3]
        # self.error_codes = error_codes
        # self.user = user
        