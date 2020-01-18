#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import serial

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
    ser.write(
        serial.to_bytes([0xC1, 0x03, 0x05, 0x02, 0x01, 0x65, 0x6C, 0x0F,
                         0xC2]))
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

FunLora_0_GetChipID()
FunLora_1_Init()
FunLora_2_ReadSetup()
#----------------------
FunLora_3_TX()
FunLora_5_write_test()
