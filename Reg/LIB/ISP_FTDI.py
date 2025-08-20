## PYTHON Version : 3.8.5

from LIB.FTDI_IIC import FTDI_IIC
from LIB.FTDI_SPI import FTDI_SPI
# from ctypes import *
# from enum import Enum
# import typing

# global IIC_inst
# global slv_addr

global SPI_inst

# slv_addr = 0x6E

IIC_inst = FTDI_IIC("./LIB/libMPSSE-I2C/lib/windows/visualstudio/x64/Release/libMPSSE.dll")
SPI_inst = FTDI_SPI("./LIB/libMPSSE-I2C/lib/windows/visualstudio/x64/Release/libMPSSE.dll")

# #################################
# Initit
# #################################
def ISP_Init(mode='IIC'):
    if(mode=='SPI'):
        SPI_inst.SPI_Init(1)
    else:
        IIC_inst.IIC_Init(0)

def ISP_deInit(mode='IIC'):
    if(mode=='SPI'):
        SPI_inst.SPI_deInit()
    else:
        IIC_inst.IIC_deInit()

def printr(macro):
    print(macro.__name__,hex(macro()))

def printh(*val):
    data =[]
    for i in val:
        data.append(hex(int(i)))
    print(data)
# #################################
# Write Address 16bit, Data 32bit
# #################################
def ISP_Write(addr,*data,mode='IIC',slv_addr=0x49,AByte=2,Byte=4,LSB=1):
    # f=open('ISP_Write.log','a')
    # f.write('ISP_Write('+hex(addr)+', '+hex(data)+')\n')
    # f.close()

    if(mode=='SPI'):
        SPI_inst.SPI_RegWrite(addr,data)
        return (SPI_inst)
    else:
        txList=[]
        for i in range(0,AByte):
            txList.append((addr>>(8*(AByte-i-1)))%(2**8))
        # txList.append((addr>>8)%(2**8))
        # txList.append(addr%(2**8))
        # printh(addr)
        for j in data:
            for i in range(0,Byte):
                if(LSB==1):
                    txList.append((j>>(8*i))%(2**8))
                else:
                    txList.append((j>>(8*(Byte-i-1)))%(2**8))
                    # printh((j>>(8*(Byte-i-1)))%(2**8))

        # if(Byte == 1)   :  txList=[(addr>>8)%(2**8),addr%(2**8),(data)%(2**8)]
        # elif(Byte == 2) :  txList=[(addr>>8)%(2**8),addr%(2**8),(data)%(2**8),(data>>8)%(2**8)]
        # elif(Byte == 3) :  txList=[(addr>>8)%(2**8),addr%(2**8),(data)%(2**8),(data>>8)%(2**8),(data>>16)%(2**8)]
        # elif(Byte == 4) :  txList=[(addr>>8)%(2**8),addr%(2**8),(data)%(2**8),(data>>8)%(2**8),(data>>16)%(2**8),(data>>24)%(2**8)]
        IIC_inst.IIC_txWords(slv_addr,txList)
        return (IIC_inst)

def ISP_WriteLog(addr,*data,mode='IIC',slv_addr=0x49,AByte=2,Byte=4,LSB=1,fname='RegControl.log'):
    f=open(fname,'a')
    # f.write(hex(addr)+', '+hex(data)+'\n')
    f.write(hex(addr)+', ')

    if(mode=='SPI'):
        SPI_inst.SPI_RegWrite(addr,data)
        return (SPI_inst)
    else:
        txList=[]
        for i in range(0,AByte):
            txList.append((addr>>(8*(AByte-i-1)))%(2**8))
        # txList.append((addr>>8)%(2**8))
        # txList.append(addr%(2**8))
        # printh(addr)
        for j in data:
            # print(j,type(j))
            for i in range(0,Byte):
                if(LSB==1):
                    txList.append((j>>(8*i))%(2**8))
                else:
                    txList.append((j>>(8*(Byte-i-1)))%(2**8))
            f.write(hex(j))
            f.write('\n')
            # printh(j)
        # if(Byte == 1)   :  txList=[(addr>>8)%(2**8),addr%(2**8),(data)%(2**8)]
        # elif(Byte == 2) :  txList=[(addr>>8)%(2**8),addr%(2**8),(data)%(2**8),(data>>8)%(2**8)]
        # elif(Byte == 3) :  txList=[(addr>>8)%(2**8),addr%(2**8),(data)%(2**8),(data>>8)%(2**8),(data>>16)%(2**8)]
        # elif(Byte == 4) :  txList=[(addr>>8)%(2**8),addr%(2**8),(data)%(2**8),(data>>8)%(2**8),(data>>16)%(2**8),(data>>24)%(2**8)]
        IIC_inst.IIC_txWords(slv_addr,txList)
        return (IIC_inst)
    f.close()

# #################################
# Read Address 16bit, Data 32bit
# #################################
def ISP_Read(addr,mode='IIC',slv_addr=0x49,AByte=2,Byte=4,LSB=1):
    if(mode=='SPI'):
        ret=(SPI_inst.SPI_RegRead(addr+0x8000))
        return (ret[0]<<24 | ret[1]<<16 | ret[2]<<8 | ret[3])
    else:
        txList=[]
        for i in range(0,AByte):
            txList.append((addr>>(8*(AByte-i-1)))%(2**8))
        # txList=[(addr>>8)%(2**8),addr%(2**8)]
        IIC_inst.IIC_txWords(slv_addr,txList)
        ret = IIC_inst.IIC_Read(slv_addr,Byte)
        
        if(LSB==1):
            if(Byte == 1)   :  return (ret[0])
            elif(Byte == 2) :  return (ret[1]<<8 | ret[0])
            elif(Byte == 3) :  return (ret[2]<<16 | ret[1]<<8 | ret[0])
            elif(Byte == 4) :  return (ret[3]<<24 | ret[2]<<16 | ret[1]<<8 | ret[0])
        else:
            if(Byte == 1)   :  return (ret[0])
            elif(Byte == 2) :  return (ret[1] | ret[0]<<8)
            elif(Byte == 3) :  return (ret[2] | ret[1]<<8 | ret[0]<<16)
            elif(Byte == 4) :  return (ret[3] | ret[2]<<8 | ret[1]<<16 | ret[0]<<24)