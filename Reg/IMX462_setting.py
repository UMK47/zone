from LIB.ISP_FTDI import *
from Sensor_setting import *
from macro import *
import time


TABLE = (
    #{'ADDR':0x3005,     'NOR30P':0x01},  	# ADBIT
    {'ADDR':0x3005,     'NOR30P':0x00},  	# ADBIT
    {'ADDR':0x3007,     'NOR30P':0x03},  	# WINMODE (1080p)
    #{'ADDR':0x3009,     'NOR30P':0x02},  	# FRSEL *
    {'ADDR':0x3009,     'NOR30P':0x01},  	# FRSEL
    {'ADDR':0x300a,     'NOR30P':0x00}, 	# BLKLEVEL (recommend : 0xf0 at 12b mode)
    {'ADDR':0x300b,     'NOR30P':0x00},  	# "
    {'ADDR':0x300c,     'NOR30P':0x00}, 	# WDSEL/WDMODE (normal : 0x0, DOL2p : 0x11)
    {'ADDR':0x300f,     'NOR30P':0x00}, 	# fixed		
    {'ADDR':0x3010,     'NOR30P':0x21},  	# FPGC : each frame gain of DOL 0x61, common gain of DOL 0x21 (normal, datasheet default is wrong)
    {'ADDR':0x3011,     'NOR30P':0x02},  	# (IMX462) fixed at DATASHEET 0.3
    {'ADDR':0x3012,     'NOR30P':0x64}, 	# fixed
    {'ADDR':0x3016,     'NOR30P':0x09}, 	# fixed

    {'ADDR':0x3018,     'NOR30P':0x65}, 	# fixed
    {'ADDR':0x3019,     'NOR30P':0x04}, 	# fixed
    {'ADDR':0x301A,     'NOR30P':0x00}, 	# fixed
    {'ADDR':0x301C,     'NOR30P':0x98}, 	# fixed
    {'ADDR':0x301D,     'NOR30P':0x08}, 	# fixed

    {'ADDR':0x3020,     'NOR30P':0x02},  	# SHS1
    {'ADDR':0x3021,     'NOR30P':0x00},  	# "
    {'ADDR':0x3022,     'NOR30P':0x00}, 	# "
    {'ADDR':0x3024,     'NOR30P':0x00},  	# SHS2
    {'ADDR':0x3025,     'NOR30P':0x00},  	# "
    {'ADDR':0x3026,     'NOR30P':0x00}, 	# "
    {'ADDR':0x3028,     'NOR30P':0x00},  	# SHS3
    {'ADDR':0x3029,     'NOR30P':0x00},  	# "
    {'ADDR':0x302A,     'NOR30P':0x00}, 	# "
    {'ADDR':0x3030,     'NOR30P':0x00},  	# RHS1
    {'ADDR':0x3031,     'NOR30P':0x00},  	# "
    {'ADDR':0x3032,     'NOR30P':0x00}, 	# "
    {'ADDR':0x3034,     'NOR30P':0x00},  	# RHS2
    {'ADDR':0x3035,     'NOR30P':0x00},  	# "
    {'ADDR':0x3036,     'NOR30P':0x00}, 	# "
    {'ADDR':0x3045,     'NOR30P':0x01}, 	# DOLSCDEN, DOLSYDINFOEN, HINFOEN
    #{'ADDR':0x3046,     'NOR30P':0x01},  	# OPORTSEL, ODBIT (normal, DOL)						#MIPI
    {'ADDR':0x3046,     'NOR30P':0x00},  	# OPORTSEL, ODBIT (normal, DOL)						#MIPI
    {'ADDR':0x305c,     'NOR30P':0x18},  	# INCKSEL1
    {'ADDR':0x305d,     'NOR30P':0x03}, 	# INCKSEL2 
    {'ADDR':0x305e,     'NOR30P':0x20},  	# INCKSEL3
    {'ADDR':0x305f,     'NOR30P':0x01},  	# INCKSEL4
    {'ADDR':0x3070,     'NOR30P':0x02},  	# fixed
    {'ADDR':0x3071,     'NOR30P':0x11},  	# fixed								
    {'ADDR':0x309b,     'NOR30P':0x10},  	# fixed
    {'ADDR':0x309c,     'NOR30P':0x21},  	# fixed							
    {'ADDR':0x30a2,     'NOR30P':0x02}, 	# (IMX462) fixed
    {'ADDR':0x30a6,     'NOR30P':0x20}, 	# (IMX462) fixed
    {'ADDR':0x30a8,     'NOR30P':0x20}, 	# (IMX462) fixed
    {'ADDR':0x30aa,     'NOR30P':0x20}, 	# (IMX462) fixed
    {'ADDR':0x30ac,     'NOR30P':0x20}, 	# (IMX462) fixed
    {'ADDR':0x30b0,     'NOR30P':0x43}, 	# (IMX462) fixed
    {'ADDR':0x30f0,     'NOR30P':0xf0}, 	# S1 gain off
    {'ADDR':0x3106,     'NOR30P':0x00},  	# XVS,HVS subsampling when DOL (2p master : 0x15)
    {'ADDR':0x3119,     'NOR30P':0x9e},  	# 
    {'ADDR':0x311c,     'NOR30P':0x1e},  	# 
    {'ADDR':0x311e,     'NOR30P':0x08}, 	# fixed
    {'ADDR':0x3128,     'NOR30P':0x05}, 	# fixed
    #{'ADDR':0x3129,     'NOR30P':0x00}, 	# ADBIT1
    {'ADDR':0x3129,     'NOR30P':0x1d}, 	# ADBIT1
    {'ADDR':0x313d,     'NOR30P':0x83}, 	# WINWV
    {'ADDR':0x3150,     'NOR30P':0x03}, 	# 
    {'ADDR':0x315e,     'NOR30P':0x1a},  	# INCKSEL5
    {'ADDR':0x3164,     'NOR30P':0x1a},  	# INCKSEL6
    #{'ADDR':0x317c,     'NOR30P':0x00},  	# ADBIT2
    {'ADDR':0x317c,     'NOR30P':0x12},  	# ADBIT2
    {'ADDR':0x317e,     'NOR30P':0x00}, 	#
    {'ADDR':0x31a0,     'NOR30P':0xfc}, 	#
    {'ADDR':0x31a1,     'NOR30P':0x00}, 	#
    #{'ADDR':0x31ec,     'NOR30P':0x0e}, 	# (IMX462) ADBIT3
    {'ADDR':0x31ec,     'NOR30P':0x37}, 	# (IMX462) ADBIT3
    {'ADDR':0x3257,     'NOR30P':0x03}, 	# fixed
    {'ADDR':0x3264,     'NOR30P':0x1a}, 	# INCKSEL6
    {'ADDR':0x3265,     'NOR30P':0xb0}, 	# fixed
    {'ADDR':0x3266,     'NOR30P':0x02}, 	# fixed
    {'ADDR':0x326b,     'NOR30P':0x10}, 	# fixed
    {'ADDR':0x3274,     'NOR30P':0x1b}, 	# fixed
    {'ADDR':0x3275,     'NOR30P':0xa0}, 	# fixed
    {'ADDR':0x3276,     'NOR30P':0x02}, 	# fixed
    {'ADDR':0x32b8,     'NOR30P':0x50}, 	# fixed
    {'ADDR':0x32b9,     'NOR30P':0x10}, 	# fixed
    {'ADDR':0x32ba,     'NOR30P':0x00}, 	# fixed
    {'ADDR':0x32bb,     'NOR30P':0x04}, 	# fixed
    {'ADDR':0x32c8,     'NOR30P':0x50}, 	# fixed
    {'ADDR':0x32c9,     'NOR30P':0x10}, 	# fixed
    {'ADDR':0x32ca,     'NOR30P':0x00}, 	# fixed
    {'ADDR':0x32cb,     'NOR30P':0x04}, 	# fixed
    {'ADDR':0x332c,     'NOR30P':0xd3}, 	# fixed
    {'ADDR':0x332d,     'NOR30P':0x10}, 	# fixed
    {'ADDR':0x332e,     'NOR30P':0x0d}, 	# fixed
    {'ADDR':0x3358,     'NOR30P':0x06}, 	# fixed
    {'ADDR':0x3359,     'NOR30P':0xe1}, 	# fixed
    {'ADDR':0x335a,     'NOR30P':0x11}, 	# fixed
    {'ADDR':0x3360,     'NOR30P':0x1e}, 	# fixed
    {'ADDR':0x3361,     'NOR30P':0x61}, 	# fixed
    {'ADDR':0x3362,     'NOR30P':0x10}, 	# fixed	
    {'ADDR':0x33b0,     'NOR30P':0x50}, 	# fixed
    {'ADDR':0x33b2,     'NOR30P':0x1a}, 	# fixed
    {'ADDR':0x33b3,     'NOR30P':0x04}, 	# fixed
    #{'ADDR':0x3405,     'NOR30P':0x10}, 	# REPETITION 			(only MIPI) 
    {'ADDR':0x3405,     'NOR30P':0x00},     # REPETITION    DATA RATE 445->891       1->0으로 바꿈
    {'ADDR':0x3407,     'NOR30P':0x01}, 	# PHYSICAL_LANE_NUM 	(only MIPI)
    {'ADDR':0x3415,     'NOR30P':0x01}, 	# DOL : 0x00
    {'ADDR':0x3418,     'NOR30P':0x49},   # Y_OUT_SIZ (normal : 0x449, DOL2P : 0x89c , DOL3P : 0x1155)
    {'ADDR':0x3419,     'NOR30P':0x04},   # "
    #{'ADDR':0x3441,     'NOR30P':0x0C},   # CSI_DT_FMT (0x0C : 12bit, 0x0A : 10bit)	(only MIPI)
    #{'ADDR':0x3442,     'NOR30P':0x0C},   # CSI_DT_FMT (0x0C : 12bit, 0x0A : 10bit)	(only MIPI)
    {'ADDR':0x3441,     'NOR30P':0x0A},   # CSI_DT_FMT (0x0C : 12bit, 0x0A : 10bit)	(only MIPI)
    {'ADDR':0x3442,     'NOR30P':0x0A},   # CSI_DT_FMT (0x0C : 12bit, 0x0A : 10bit)	(only MIPI)
    {'ADDR':0x3443,     'NOR30P':0x01},   # CSI_LANE_MODE (4lane)(only MIPI)
    {'ADDR':0x3444,     'NOR30P':0x20},   # EXTCK_FREQ			(only MIPI)
    {'ADDR':0x3445,     'NOR30P':0x25},   # EXTCK_FREQ			(only MIPI)
    #{'ADDR':0x3446,     'NOR30P':0x57},   # TCLKPOST				(only MIPI)
    #{'ADDR':0x3447,     'NOR30P':0x00},   # TCLKPOST				(only MIPI)
    {'ADDR':0x3446,     'NOR30P':0x77},   # TCLKPOST				(only MIPI)
    {'ADDR':0x3447,     'NOR30P':0x00},   # TCLKPOST
    #{'ADDR':0x3448,     'NOR30P':0x37},   # THSZERO				(only MIPI)
    #{'ADDR':0x3449,     'NOR30P':0x00},   # THSZERO				(only MIPI)
    {'ADDR':0x3448,     'NOR30P':0x67},   # THSZERO				(only MIPI)
    {'ADDR':0x3449,     'NOR30P':0x00},   # THSZERO				(only MIPI)
    #{'ADDR':0x344A,     'NOR30P':0x1F},   # THSPREPARE			(only MIPI)
    #{'ADDR':0x344B,     'NOR30P':0x00},   # THSPREPARE			(only MIPI)
    {'ADDR':0x344A,     'NOR30P':0x47},   # THSPREPARE			(only MIPI)
    {'ADDR':0x344B,     'NOR30P':0x00},   # THSPREPARE			(only MIPI)
    #{'ADDR':0x344C,     'NOR30P':0x1F},   # TCLKTRAIL				(only MIPI)
    #{'ADDR':0x344D,     'NOR30P':0x00},   # TCLKTRAIL				(only MIPI)
     {'ADDR':0x344A,     'NOR30P':0x37},   # THSPREPARE			(only MIPI)
    {'ADDR':0x344B,     'NOR30P':0x00},   # THSPREPARE			(only MIPI)
    #{'ADDR':0x344E,     'NOR30P':0x1F},   # THSTRAIL				(only MIPI)
    #{'ADDR':0x344F,     'NOR30P':0x00},   # THSTRAIL				(only MIPI)
    {'ADDR':0x344E,     'NOR30P':0x3F},   # THSTRAIL				(only MIPI)
    {'ADDR':0x344F,     'NOR30P':0x00},   # THSTRAIL				(only MIPI)
    #{'ADDR':0x3450,     'NOR30P':0x77},   # TCLKZERO				(only MIPI)
    #{'ADDR':0x3451,     'NOR30P':0x00},   # TCLKZERO				(only MIPI)
    {'ADDR':0x3450,     'NOR30P':0xFF},   # TCLKZERO				(only MIPI)
    {'ADDR':0x3451,     'NOR30P':0x00},   # TCLKZERO				(only MIPI)
    #{'ADDR':0x3452,     'NOR30P':0x1F},   # TCLKPREPARE			(only MIPI)
    #{'ADDR':0x3453,     'NOR30P':0x00},   # TCLKPREPARE			(only MIPI)
    {'ADDR':0x3452,     'NOR30P':0x3F},   # TCLKPREPARE			(only MIPI)
    {'ADDR':0x3453,     'NOR30P':0x00},   # TCLKPREPARE			(only MIPI)
    #{'ADDR':0x3454,     'NOR30P':0x17},   # TLPX					(only MIPI)
    #{'ADDR':0x3455,     'NOR30P':0x00},   # TLPX					(only MIPI)
    {'ADDR':0x3454,     'NOR30P':0x37},   # TLPX					(only MIPI)
    {'ADDR':0x3455,     'NOR30P':0x00},   # TLPX					(only MIPI)
    {'ADDR':0x3472,     'NOR30P':0x9C},   # X_OUT_SIZE			(only MIPI)
    {'ADDR':0x3473,     'NOR30P':0x07},   # X_OUT_SIZE			(only MIPI)
    {'ADDR':0x347b,     'NOR30P':0x24},   # MIF_SYNC_TIM0			(only MIPI)
    {'ADDR':0x3480,     'NOR30P':0x49})   # INCKSEL7




# def SSWrReg(slv,addr,data):
#     register = slv*(2**24) + addr*(2**8) + data
#     # register = UINT(register)
#     # printh(register)
#     ISP_Write(SS_DATA1_ADDR, register)	    #time.sleep(0.01)
#     # printh(ISP_Read(SS_DATA1_ADDR))
#     ISP_Write(SS_CMD_ADDR, 0)				#time.sleep(0.01)

# def Sony_SSWrReg(slvad, addr,data):
#     waddr = addr
#     wdata = data%(2**8)
#     SSWrReg(slvad,waddr,wdata)

#     waddr = addr+1
#     wdata = data>>8
#     SSWrReg(slvad,waddr,wdata)


def Pre_IMX462():

    IMX462_I2C = Sensor_I2C(0x1a,2,1)
    IMX462_I2C.Reset()
    IMX462_I2C.Write(0x3000,0x01)
    IMX462_I2C.Write(0x3002,0x01)
    IMX462_I2C.Write(0x3001,0x01)
    IMX462_I2C.Write(0x3003,0x01)

    for i in TABLE:
        IMX462_I2C.Write(i['ADDR'],i['NOR30P'])
    
    IMX462_I2C.Write2(0x301C,0x1130)	
    # IMX462_I2C.Write2(0x301C,0x898)	
    IMX462_I2C.Write2(0x3018,0x465)		
    IMX462_I2C.Write2(0x3009,0x01)		

    IMX462_I2C.Write2(0x3020, 0x80)		# SHS1
        
    IMX462_I2C.Write(0x3003,0x00)
    IMX462_I2C.Write(0x3001,0x00)
    IMX462_I2C.Write(0x3000,0x00)
    IMX462_I2C.Write(0x3002,0x00)
    

