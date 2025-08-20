from LIB.ISP_FTDI import *
from macro import *

class Sensor_I2C ():
    def __init__(self,slave,aByte,dByte,LSB=1):
        self.SLV=slave
        self.AB=aByte
        self.DB=dByte
        self.LSB=LSB
    

    def Write2(self,addr,data,LSB=1):
        if(LSB==0) :    
            self.Write(addr,data>>8)
            self.Write(addr+1,data&0xFF)
        else:           
            self.Write(addr,data&0xFF)
            self.Write(addr+1,data>>8)

    def Write3(self,addr,data,LSB=1):
        if(LSB==0) :    
            self.Write(addr,data>>16)
            self.Write(addr+1,data>>8)
            self.Write(addr+2,data&0xFF)
        else:           
            self.Write(addr,data&0xFF)
            self.Write(addr+1,data>>8)
            self.Write(addr+2,data>>16)

    def Write(self,addr,data):
        ISP_Write(addr, data, mode='IIC', slv_addr=self.SLV,AByte=self.AB,Byte=self.DB,LSB=self.LSB)
        printh(0,self.SLV,addr,data)

    def Read(self,addr):
        rdata = ISP_Read(addr,mode='IIC',slv_addr=self.SLV,AByte=self.AB,Byte=self.DB)
        printh(1,self.SLV,addr,rdata)
        return rdata

    def Reset(self):
        SS_RSTNw(0)
        SS_RSTNw(1)
        # L_I2C_ONw(3)
        # GPIO_Ow((GPIO_Or()&0xFFFFFB))
        # GPIO_Ow((GPIO_Or()&0xFFFFFB)|4)

