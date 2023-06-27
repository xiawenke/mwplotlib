import os
import pandas as pd
import numpy as np
from io import StringIO

class ArmsData(): 
    def __init__(self):
        self.__dir__ = os.path.dirname(os.path.realpath(__file__))
        self._path_apjacc45ct1_mrt = os.path.join(self.__dir__, "data", 'apjacc45ct1_mrt.txt')
        self._path_apjacc45ct2_ascii = os.path.join(self.__dir__, "data", 'apjacc45ct2_ascii.txt')

        self._HMSFR_masers_data_df = pd.DataFrame()
        self._HMSFR_masers_data_dict = {}
        self._HMSFR_masers_data_df, self._HMSFR_masers_data_dict = self.apjacc45ct1_mrt(); 
    
        self._spiral_arm_param_df = pd.DataFrame()
        self._spiral_arm_param_dict = {}
        self._spiral_arm_param_df, self._spiral_arm_param_dict = self.apjacc45ct2_ascii(); 
    
    def __call__(self, type, format = "dict"):
        if(type == 'scatter'):
            if(format == 'df'):
                return self._HMSFR_masers_data_df
            elif(format == 'dict'):
                return self._HMSFR_masers_data_dict
            else:
                raise Exception('Format not supported: {}'.format(format))
        elif(type == 'shape'):
            if(format == 'df'):
                return self._spiral_arm_param_df
            elif(format == 'dict'):
                return self._spiral_arm_param_dict
            else:
                raise Exception('Format not supported: {}'.format(format))
        else:
            raise Exception('Type not supported: {}'.format(type))
    
    def apjacc45ct1_mrt_idx(self, idx_data):
        columns = ["Start", "End", "DataType", "Unit", "Name", "Description"]

        data_dict = {}
        for row in idx_data:
            # print(row[:5])
            bytes_range = row[:8].strip()
            if(len(bytes_range.split('-')) == 1):
                bytes_range = bytes_range + '-' + bytes_range

            start = int(bytes_range.split('-')[0].strip())
            end = int(bytes_range.split('-')[1].strip())
            data_type = row[9:15].strip()
            unit = row[16:23].strip()
            name = row[24:31].strip()
            description = row[32:].strip()
            data_dict[name] = {"Start": start, "End": end, "DataType": data_type, "Unit": unit, "Description": description}

        # df = pd.DataFrame.from_dict(data_dict, orient='index', columns=columns)
        # print(data_dict)

        return data_dict

    def apjacc45ct1_mrt(self):
        if(os.path.exists(self._path_apjacc45ct1_mrt) == False):
            raise Exception('File not found: {}'.format(self._path_apjacc45ct1_mrt))
        
        data_splitted = [[]]
        data_dict = {}

        with open(self._path_apjacc45ct1_mrt, 'r') as file:
            for line in file:
                if line.strip().startswith('--------------------------------------------------------------------------------'):
                    data_splitted.append([])
                    continue
                data_splitted[-1].append(line)

        data_idx = self.apjacc45ct1_mrt_idx(data_splitted[2])
        # print(data_idx)

        # df = pd.DataFrame([row.split() for row in data_splitted[-1]])
        
        # ref_i = 0
        # column_names = ['Source', 'RA1', 'RA2', 'RA3', 'Dec1', 'Dec2', 'Dec3', 'Parallax', 'Parallax_err', 'PM_x', 'PM_x_err', 'PM_y', 'PM_y_err', 'Velocity', 'Velocity_err', 'Spiral_arm']
        # while len(df.columns) > len(column_names):
        #     ref_i += 1
        #     column_names.append('Reference_' + str(ref_i))
        # df.columns = column_names

        data_dict = {}
        for row in data_splitted[-1]:
            this_dict = {}
            for key in data_idx:
                this_dict[key] = row[(data_idx[key]['Start']-1):data_idx[key]['End']].strip()
            data_dict[row[:8].strip()] = this_dict
        
        df = pd.DataFrame.from_dict(data_dict, orient='index')
        df = df.replace(r'^\s*$', np.nan, regex=True)

        return df, df.to_dict(orient='records')

    def apjacc45ct2_ascii(self):
        if(os.path.exists(self._path_apjacc45ct2_ascii) == False):
            raise Exception('File not found: {}'.format(self._path_apjacc45ct2_ascii))

        # start reading from line 7
        # end reading at line 19
        data_splitted = []
        colomn_names = []
        with open(self._path_apjacc45ct2_ascii, 'r') as file:
            for line in file:
                data_splitted.append(line)
        
        colomn_names = data_splitted[4].split('\t')
        data_splitted = data_splitted[6:17]
        data_str = ''.join(data_splitted)
        # print(data_str)

        # use pd to read the table from data, data splitted by tab
        df = pd.read_csv(
            StringIO(data_str),
            sep='\t',
            header=None
        )
        df.columns = colomn_names

        # if the Spiral Arm column is empty, fill it with the previous value
        df['Spiral Arm'] = df['Spiral Arm'].fillna(method='ffill')

        # print(df)
        
        return df, df.to_dict(orient='records')
        

# Tests
# arms = ArmsData()
# print(arms())