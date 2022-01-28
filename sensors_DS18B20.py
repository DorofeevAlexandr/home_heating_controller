import os
import glob


class Sensors_DS18B20():
    def __init__(self) -> None:
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        self.base_dir = '/sys/bus/w1/devices/'

    def read_temp_raw(self, sensor_adr):
        # print(device_file)
        device_folder = glob.glob(self.base_dir + sensor_adr)[0]
        device_file = device_folder + '/w1_slave'
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self, sensor_adr):
        lines = self.read_temp_raw(sensor_adr)
        # print(lines)
        if lines[0].strip()[-3:] == 'YES':
            equals_pos = lines[1].find('t=')
            # print(equals_pos)
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                return temp_c
        return None
