from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
import datetime
import time
import sys
import pyodbc 

class SelectTable:
    table_service = TableService(account_name = 'newsolarwebstorage', account_key = 'VnAoHBffjISbdW84MoQgGwtfRSmovHNidkTSAxKq5TNMk8G3oX2yyO7CgrFahMLxFg2/bs/wwPhkUrgm611/Wg==')
    
    selectItem = ['PartitionKey', 'RowKey', 't0700', 't0720', 't0740', 't0800', 't0820', 't0840', 't0900', 't0920', 't0940', 't1000', 't1020', 't1040', 't1100', 't1120', 't1140', 't1200', 't1220', 't1240', 't1300', 't1320', 't1340', 't1400', 't1420', 't1440', 't1500', 't1520', 't1540', 't1600', 't1620', 't1640', 't1700', 't1720', 't1740', 't1800']
    selectText = 'PartitionKey, RowKey, t0700, t0720, t0740, t0800, t0820, t0840, t0900, t0920, t0940, t1000, t1020, t1040, t1100, t1120, t1140, t1200, t1220, t1240, t1300, t1320, t1340, t1400, t1420, t1440, t1500, t1520, t1540, t1600, t1620, t1640, t1700, t1720, t1740, t1800'

    def __init__(self):
        pass
    
    def selectOneDay(self, Date):
        self.Date = Date
        tasks = self.table_service.query_entities('gwstatus', filter=f"RowKey eq '{ Date }'", select=self.selectText)
        
        listTask = []
        for task in tasks:
            dictItem = []
            mydict = {'PartitionKey':'', 'RowKey':'', 't0700':'', 't0720':'', 't0740':'', 't0800':'', 't0820':'', 't0840':'', 't0900':'', 't0920':'', 't0940':'', 't1000':'', 't1020':'', 't1040':'', 't1100':'', 't1120':'', 't1140':'', 't1200':'', 't1220':'', 't1240':'', 't1300':'', 't1320':'', 't1340':'', 't1400':'', 't1420':'', 't1440':'', 't1500':'', 't1520':'', 't1540':'', 't1600':'', 't1620':'', 't1640':'', 't1700':'', 't1720':'', 't1740':'', 't1800':''}
            for select in self.selectItem:
                mydict[select] = task[select]
            dictItem.append(mydict)
            listTask.append(dictItem)
        output = []
        
        for item in listTask:
            id = []
            for select in self.selectItem:
                id.append(item[0][select])
            output.append(id)
        self.output = output

        return output
    
    def judgeToday(self):
        return False

    def judgeOneDay(self):
        selectTextforTpye = 'PartitionKey' + ',' + 'ConnectionType'
        taskforType = self.table_service.query_entities('gwData', filter="", select=selectTextforTpye)
        location_array = self.getAddress()
        
        now = 't' + datetime.datetime.now().strftime('%H%M')
        for i in range(2, len(self.selectItem)):
            if now < self.selectItem[i]:
                break
        if i - 1 < len(self.selectItem):
            endIndex = i - 1
        else:
            endIndex = len(self.selectItem)

        for SN in self.output:
            DISCONNECTCOUNT = self.findSerious(SN)
            RS485 = self.findRS485(SN)
            ETHERNET = self.findETHERNET(SN)
            RECONNET = self.findRECONNET(SN, endIndex + 1)    
            # 不需要連續
            if RS485 > ETHERNET:
                SN.insert(1, "RS485")
            elif ETHERNET > RS485:
                SN.insert(1, "ETHERNET")
            elif ETHERNET == RS485:
                SN.insert(1, "RS485/ETHERNET")
            else:
                SN.insert(1, None)
            
            if DISCONNECTCOUNT >= endIndex - 1:
                SN.insert(2, "☑")
            else:
                SN.insert(2, None)
            
            if RECONNET == False:
                SN.insert(3, None)
            else:
                flag = False
                for i in range(RECONNET, len(SN)):
                    if SN[i] == None:
                        flag = True
                        break
                if flag:
                    SN.insert(3, "☑")
                else:
                    SN.insert(3, None)

            location = None
            for item in location_array:
                flag = 1
                for i in range(len(item[0])):
                    if item[0][i] != SN[0][i]:
                        flag = 0
                        break
                if flag == 1:
                    location = item[1] + item[2]
                    break
            
            ConnectionType = None
            for item in taskforType:
                if len(item) > 2 and SN[0] == item['PartitionKey']:
                    ConnectionType = item['ConnectionType']
                    break
            
            SN.insert(1, location)
            SN.insert(2, ConnectionType)
            SN.pop(6)
        return self.output

    def mergeTwoDay(self, merge):
        mergeList = []
        
        i = 0
        j = 0
        while i < len(self.output) and j < len(merge):
            if self.output[i][0] < merge[j][0]:
                mergeList.append(self.output[i])
                i += 1
            else:
                mergeList.append(merge[j])
                j += 1
        while i < len(self.output):
            mergeList.append(self.output[i])
            i += 1
        while j < len(merge):
            mergeList.append(merge[j])
            j += 1
        
        output = []
        for i in range(len(mergeList)):
            if i-1 >= 0 and mergeList[i-1][0] == mergeList[i][0]:
                for item in mergeList[i]:
                    output[len(output) - 1].append(item)
            else:
                output.append(mergeList[i])
        
        for SN in output:
            if SN[1] == self.Date:
                for j in range( len(SN) ):
                    SN.insert(1, None)
        
        self.output = output

        return output

    def judgeTwoDay(self): 
        location_array = self.getAddress()
        
        for SN in self.output:
            if len(SN) > 36:
                SN.pop(36)
                SN.pop(36)
                if SN[35] != None and SN[36] != None:
                    SN[1] = "☑"
                else:
                    SN[1] = None
            else:
                SN[1] = None
        
        for SN in self.output:
            location = ''
            for item in location_array:
                flag = 1
                for i in range(len(item[0])):
                    if item[0][i] != SN[0][i]:
                        flag = 0
                        break
                if flag == 1:
                    location = item[1] + item[2]
                    break
            SN.insert(1, location)

        return self.output

    def findRECONNET(self, SN, end):
        count = 0
        for i in range(2, end):
            if(SN[i] == '1' or SN[i] == '2' or SN[i] == '4' or SN[i] == '5'):
                count += 1
            else:
                if count >= 4:
                    return i
                count = 0
        
        return False

    def findRS485(self, SN):
        # 不需要連續
        count = 0
        for i in range(len(SN)):
            if(SN[i] == '1' or SN[i] == '2' or SN[i] == '4'):
                count += 1
        return count

    def findETHERNET(self, SN):
        # 不需要連續
        count = 0
        for i in range(len(SN)):
            if(SN[i] == '5'):
                count += 1
        return count
    
    def findSerious(self, SN):
        count = 0
        max = 0
        for i in range(2, len(SN)):
            if(SN[i] == '1' or SN[i] == '2' or SN[i] == '4' or SN[i] == '5'):
                count += 1
            else:
                if count > max:
                    max = count
                count = 0
        if count > max:
            max = count
        
        return max

    def getAddress(self):
        selectstring = '''  
            SELECT
                [SITE_NO]
                ,[CITY_NAME]
                ,[CASE_NAME]
            FROM [dbo].[Info_Site_RC]
        '''
        output = []
        # Some other example server values are
        # server = 'localhost\sqlexpress' # for a named instance
        # server = 'myserver,port' # to specify an alternate port
        server = 'tatungtmiot.database.windows.net' 
        database = 'TATUNG_SOLAR_IOT' 
        username = 'readOnlyUser' 
        password = 'ReadOnly4321' 
        # 連線
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        # 查詢
        cursor.execute(selectstring) 
        row = cursor.fetchone() 
        while row:
            output.append(row)
            row = cursor.fetchone()
        # 關閉
        cnxn.close()
        
        return output