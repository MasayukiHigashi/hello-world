import serial
import time
import datetime
import csv
import os
from serial.tools import list_ports



# for ubuntu
import subprocess
device_name = '/dev/ttyUSB0'
# permission change 
subprocess.run('sudo chmod o+wr ' + device_name,shell=True)

# port num search　for windows
# set device keyword
def comport_search(device_name_keyword = "MOXA"):
    # return port num
    ports = list_ports.comports()
    device = [info for info in ports if device_name_keyword in info.description]

    try:
        return device[0].device
    except:
        print("計測器が接続されていません")
        exit()


comport = serial.Serial(device_name,baudrate=230400,parity=serial.PARITY_NONE)
#comport = serial.Serial(comport_search(),baudrate=230400,parity=serial.PARITY_NONE)

all_time = 0
gnss_hertz = 10
# Hikisuu de toru
recording_time = 60

start_time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
log_save_dir = 'gnss_log'
os.makedirs(log_save_dir, exist_ok=True)
log_name = 'GNSS_log_'+ start_time_str+'.csv'
log_path = log_save_dir + os.sep + log_name
log_header = ['UNIX_Time','UTC', 'latitude', 'North-south', 'longitude', 'East-west']
# make log file
with open(log_path , 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerow(log_header)


for i in range(recording_time*gnss_hertz):
    #tmp_time = time.time()
    #recv_data = comport.read(100).decode()
    recv_data = comport.readline().decode()
    #recv_data = '$GPRMC,083912.30,A,3538.53636147,N,13944.52325433,E,0.020,0.00,070122,,,A*6E'
    recv_list = recv_data.rsplit(',')
    # for GPRMC
    log_data_list = [time.time(),recv_list[1],recv_list[3],recv_list[4],recv_list[5],recv_list[6]]
    with open(log_path , 'a', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(log_data_list)

    """
    # print time detail
    time_diff = time.time() - tmp_time
    all_time += time_diff
    print(str(i) + ': UNIX time:'+str(time.time())+', UTC Time:'+str(datetime.datetime.utcnow()))
    print('Processing Time:'+str(time_diff) + ', Ave:'+str(all_time/(i+1)))
    """
    print(recv_data) 


comport.close()
