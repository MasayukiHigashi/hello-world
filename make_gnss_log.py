# coding:utf8
import serial
import sys
import time
import datetime
import csv
import os
from serial.tools import list_ports
import traceback

#gnss_hertz = 10
#recording_time = 60

def preprocess(windows_flag=False,baudrate = 230400,device_name = '/dev/ttyUSB0',device_name_keyword = "MOXA"):
    if windows_flag:
        # port num search for windows
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
        comport = serial.Serial(comport_search(device_name_keyword),baudrate=baudrate,parity=serial.PARITY_NONE)
    # for ubuntu
    else :
        import subprocess
        # permission change 
        subprocess.run('sudo chmod o+wr ' + device_name,shell=True)
        comport = serial.Serial(device_name,baudrate=baudrate,parity=serial.PARITY_NONE)
    return comport

def create_log_file(log_save_dir = 'gnss_log'):
    start_time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    os.makedirs(log_save_dir, exist_ok=True)
    log_name = 'GNSS_log_'+ start_time_str+'.csv'
    log_path = log_save_dir + os.sep + log_name
    log_header = ['UNIX_Time','UTC_Date','UTC_Time', 'Latitude', 'North-South', 'Longitude', 'East-West']
    # make log file
    with open(log_path , 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(log_header)
    return log_path

def log_gnss(comport,log_path,print_flag = True):
    # all_time = 0
    try:
        # for i in range(recording_time*gnss_hertz):
        while True:
            #tmp_time = time.time()
            #recv_data = comport.read(100).decode()
            recv_data = comport.readline().decode()
            #recv_data = '$GPRMC,083912.30,A,3538.53636147,N,13944.52325433,E,0.020,0.00,070122,,,A*6E'
            recv_list = recv_data.rsplit(',')
            # for GPRMC
            log_data_list = [time.time(),recv_list[9],recv_list[1],recv_list[3],recv_list[4],recv_list[5],recv_list[6]]
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
            if print_flag:
                print(recv_data) 
    except KeyboardInterrupt:
        comport.close()
        print('### Info: Ctrl + c interrupt. End GNSS Log ###')
        sys.exit()
    except :
        comport.close()
        print('### Info: Unknown Error. End GNSS Log ###')
        print('# traceback.format_exc()')
        t = traceback.format_exc()
        print(t)
        sys.exit()

if __name__ == "__main__":
    if os.name == 'nt':
        windows_flag = True
    else:
        windows_flag = False
    comport = preprocess(windows_flag)
    log_path = create_log_file()
    log_gnss(comport,log_path,print_flag = False)
    # log_gnss(comport,log_path)
