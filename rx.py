#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import serial

COM_PORT = '/dev/ttyUSB0'  # 指定通訊埠名稱
BAUD_RATES = 115200  # 設定傳輸速率
ser = serial.Serial(COM_PORT, BAUD_RATES, timeout=10)  # 初始化序列通訊埠

# 計算CRC 檢查碼
def Fun_CRC(data):
    crc = 0
    for i in data:
        crc = crc ^ i
    return crc

def FunLora_0_GetChipID():
    # * 讀取F/W版本及Chip ID
    print("讀取F/W版本及Chip ID")
    ser.write(serial.to_bytes([0x80, 0x00, 0x00, 0x80]))
    data = ser.read(10)
    print(data.encode('hex'))

def FunLora_1_Init():
    # * 重置 & 初始化
    print("重置 & 初始化")
    ser.write(serial.to_bytes([0xC1, 0x01, 0x00, 0xC0]))
    data = ser.read(5)
    print(data.encode('hex'))

def FunLora_2_ReadSetup():
    # * 讀取設定狀態
    print("讀取設定狀態")
    ser.write(serial.to_bytes([0xC1, 0x02, 0x00, 0xC3]))
    data = ser.read(12)
    print(data.encode('hex'))

def FunLora_3_RX():
    # * 設定 RX (W)_IN 接收端
    print("設定 RX (W)_IN 接收端")
    ser.write(
        serial.to_bytes([0xC1, 0x03, 0x05, 0x03, 0x01, 0x65, 0x6C, 0x0F,
                         0xC3]))
    data = ser.read(5)
    print(data.encode('hex'))

def FunLora_6_redata():
    # * 讀取資料
    print("讀取資料")
    ser.write(serial.to_bytes([0xC1, 0x06, 0x00, 0xC7]))
    data = ser.read(22)
    print(data.encode('hex'))

    #print(len(data)) #總數量
    #3~18 20
    if len(data) == 22:
        d0 = (int(data[0].encode('hex'), 16)) #c1
        d1 = (int(data[1].encode('hex'), 16)) #86
        d2 = (int(data[2].encode('hex'), 16)) #12
        #======data=====start==================
        d3 = (int(data[3].encode('hex'), 16))
        d4 = (int(data[4].encode('hex'), 16))
        d5 = (int(data[5].encode('hex'), 16))
        d6 = (int(data[6].encode('hex'), 16))
        d7 = (int(data[7].encode('hex'), 16))
        d8 = (int(data[8].encode('hex'), 16))
        d9 = (int(data[9].encode('hex'), 16))
        d10 = (int(data[10].encode('hex'), 16))
        d11 = (int(data[11].encode('hex'), 16))
        d12 = (int(data[12].encode('hex'), 16))
        d13 = (int(data[13].encode('hex'), 16))
        d14 = (int(data[14].encode('hex'), 16))
        d15 = (int(data[15].encode('hex'), 16))
        d16 = (int(data[16].encode('hex'), 16))
        d17 = (int(data[17].encode('hex'), 16))
        d18 = (int(data[18].encode('hex'), 16))
        #======data=====end==================
        d19 = (int(data[19].encode('hex'), 16)) #ff
        d20 = (int(data[20].encode('hex'), 16)) #rssi
        d21 = (int(data[21].encode('hex'), 16)) #crc
        print "rssi",d20
        print "crc",d21
        #*CRC測試
        array1=[d0,d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13,d14,d15,d16,d17,d18,d19,d20]
        ckcrc=Fun_CRC(array1)     
        print "ckcrc",ckcrc
        if d21 == ckcrc:
            #正確
            print("=====success=====")
        else:
            print("=====error=====")

FunLora_0_GetChipID()
FunLora_1_Init()
FunLora_2_ReadSetup()
#----------------------
FunLora_3_RX()
FunLora_6_redata()
