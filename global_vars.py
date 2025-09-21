from entity.Student import Student

SERVER_ADDRESS = 'http://127.0.0.1:8888/'
WORKSTATION_SERVER_ADDRESS = 'http://127.0.0.1:8080'
student = Student("","","",0,0,0,"")    # 用于全局保存本次实验对象的信息

# gazepoint 相关共享数据
gazepoint_pid = None
gazepoint_hwnd = None

# 用于保存选择的实验范式id
paradigm_id = None

# 实验id
experiment_id = None
# 实验状态
experiment_status = None

# 设备状态信息
CREAM_STATUS = False
HR_STATUS = False
GSR_STATUS = False
EEG_IMP_STATUS = False
EEG_DATA_STATUS = False
GAZEPOINT_CAL_STATUS = False
GAZEPOINT_DATA_STATUS = False