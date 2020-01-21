#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import serial
import RPi.GPIO as GPIO
import httplib

COM_PORT = '/dev/ttyUSB0'  # 指定通訊埠名稱
BAUD_RATES = 115200  # 設定傳輸速率
ser = serial.Serial(COM_PORT, BAUD_RATES, timeout=10)  # 初始化序列通訊埠


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


def FunLora_3_TX():
    # * 設定 TX (R)_OUT 發送端
    print("設定 TX (R)_OUT 發送端")
    # ser.write(
    #     serial.to_bytes([0xC1, 0x03, 0x05, 0x02, 0x01, 0x65, 0x6C, 0x0F,
    #                      0xC2]))
    ser.write(
        serial.to_bytes([0xC1, 0x03, 0x05, 0x02, 0x01, 0x67, 0x60, 0x0F,
                         0xCC]))
    data = ser.read(5)
    print(data.encode('hex'))


def FunLora_3_RX():
    # * 設定 RX (W)_IN 接收端
    print("設定 RX (W)_IN 接收端")
    #ser.write(
    #    serial.to_bytes([0xC1, 0x03, 0x05, 0x03, 0x01, 0x65, 0x6C, 0x0F,
    #                      0xC3]))
    ser.write(
        serial.to_bytes([0xC1, 0x03, 0x05, 0x03, 0x01, 0x67, 0x60, 0x0F,
                         0xCD]))
    data = ser.read(5)
    print(data.encode('hex'))


def FunLora_5_write_test():
    # * 寫入資料
    print("寫入資料")
    ser.write(
        serial.to_bytes([
            0xC1, 0x05, 0x10, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
            0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0xC4
        ]))
    data = ser.read(5)
    print(data.encode('hex'))
    print("=====switch=====")
    time.sleep(1)
    FunLora_3_RX()
    Fun_ckonoff()

def FunLora_6_redata():
    # * 讀取資料
    print("讀取資料")
    ser.write(serial.to_bytes([0xC1, 0x06, 0x00, 0xC7]))
    data = ser.read(22)
    print(data.encode('hex'))

    #print(len(data)) #總數量
    #3~18 20
    if len(data) == 22:
        d0 = (int(data[0].encode('hex'), 16))  #c1
        d1 = (int(data[1].encode('hex'), 16))  #86
        d2 = (int(data[2].encode('hex'), 16))  #12
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
        d19 = (int(data[19].encode('hex'), 16))  #ff
        d20 = (int(data[20].encode('hex'), 16))  #rssi
        d21 = (int(data[21].encode('hex'), 16))  #crc
        print "rssi", d20
        print "crc", d21
        #*CRC測試
        array1 = [
            d0, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14,
            d15, d16, d17, d18, d19, d20
        ]
        ckcrc = Fun_CRC(array1)
        print "ckcrc", ckcrc
        if d21 == ckcrc:
            #正確
            print("=====success=====")
            urlData = "/develop/lora/v3/data.php?action=insertByAPIKey&data3=%d&data4=%d&data5=%d&data6=%d&data7=%d&data8=%d&data9=%d&data10=%d&data11=%d&data12=%d&data13=%d&data14=%d&data15=%d&data16=%d&data17=%d&data18=%d&data20=%d" % (
                d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16,
                d17, d18, d20)
            Fun_HTTPGet(urlData)

        else:
            print("=====error=====")
            urlData = "/develop/lora/v3/data.php?action=insertByAPIKey&data3=%d&data4=%d&data5=%d&data6=%d&data7=%d&data8=%d&data9=%d&data10=%d&data11=%d&data12=%d&data13=%d&data14=%d&data15=%d&data16=%d&data17=%d&data18=%d&data20=%d" % (
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0)
            Fun_HTTPGet(urlData)
        time.sleep(10)
        FunLora_3_TX()
        FunLora_5_write_test()


def Fun_HTTPGet(iURLPath):
    conn = httplib.HTTPConnection("web.wshin.online")
    conn.request("GET", iURLPath)
    res = conn.getresponse()
    print(res.status, res.reason)
    conn.close()


# 計算CRC 檢查碼
def Fun_CRC(data):
    crc = 0
    for i in data:
        crc = crc ^ i
    return crc


# 讀取lora on off 第一排,腳位6 #12,GPIO18
def loraswitch():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.IN, GPIO.PUD_UP)  #上拉電阻
    #print('Switch status = ', GPIO.input(12))
    x = GPIO.input(12)
    GPIO.cleanup()
    return x


# 檢查是否有資料進來 pin12 GPIO18
def Fun_ckonoff():
    while True:
        dataled = loraswitch()
        if dataled == 1:  #有資料
            FunLora_6_redata()
            break
        #else:       #等待資料中...
        #print dataled  #低電位 0
        time.sleep(1)


FunLora_0_GetChipID()
FunLora_1_Init()
FunLora_2_ReadSetup()
#----------------------
#FunLora_3_TX()
#FunLora_5_write_test()
#----------------------
FunLora_3_RX()
Fun_ckonoff()
   

ser.close()
