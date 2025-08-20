from LIB.ISP_FTDI import *
import math
MIPI_RX0_VC_ADDR = 0x000b;	MIPI_RX0_VC_OFFS = 2**8;	MIPI_RX0_VC_OFFE = 2**10;
def MIPI_RX0_VCw(data):
    rreg = ISP_Read(MIPI_RX0_VC_ADDR);		wreg = ((math.floor(data) * MIPI_RX0_VC_OFFS)% MIPI_RX0_VC_OFFE) + (rreg % MIPI_RX0_VC_OFFS) + (rreg-(rreg % MIPI_RX0_VC_OFFE));		ISP_Write(MIPI_RX0_VC_ADDR, wreg);
def MIPI_RX0_VCr():
    return math.floor((ISP_Read(MIPI_RX0_VC_ADDR) % MIPI_RX0_VC_OFFE)/MIPI_RX0_VC_OFFS);  
MIPI_RX0_TYPE_ADDR = 0x000b;	MIPI_RX0_TYPE_OFFS = 2**0;	MIPI_RX0_TYPE_OFFE = 2**6;
def MIPI_RX0_TYPEw(data):
    rreg = ISP_Read(MIPI_RX0_TYPE_ADDR);		wreg = ((math.floor(data) * MIPI_RX0_TYPE_OFFS)% MIPI_RX0_TYPE_OFFE) + (rreg % MIPI_RX0_TYPE_OFFS) + (rreg-(rreg % MIPI_RX0_TYPE_OFFE));		ISP_Write(MIPI_RX0_TYPE_ADDR, wreg);
def MIPI_RX0_TYPEr():
    return math.floor((ISP_Read(MIPI_RX0_TYPE_ADDR) % MIPI_RX0_TYPE_OFFE)/MIPI_RX0_TYPE_OFFS);  
MIPI_RX0_ERROR_ADDR = 0x000c;	MIPI_RX0_ERROR_OFFS = 2**0;	MIPI_RX0_ERROR_OFFE = 2**18;
def MIPI_RX0_ERRORw(data):
    rreg = ISP_Read(MIPI_RX0_ERROR_ADDR);		wreg = ((math.floor(data) * MIPI_RX0_ERROR_OFFS)% MIPI_RX0_ERROR_OFFE) + (rreg % MIPI_RX0_ERROR_OFFS) + (rreg-(rreg % MIPI_RX0_ERROR_OFFE));		ISP_Write(MIPI_RX0_ERROR_ADDR, wreg);
def MIPI_RX0_ERRORr():
    return math.floor((ISP_Read(MIPI_RX0_ERROR_ADDR) % MIPI_RX0_ERROR_OFFE)/MIPI_RX0_ERROR_OFFS);  
MIPI_RX0_CLEAR_ADDR = 0x0010;	MIPI_RX0_CLEAR_OFFS = 2**8;	MIPI_RX0_CLEAR_OFFE = 2**9;
def MIPI_RX0_CLEARw(data):
    rreg = ISP_Read(MIPI_RX0_CLEAR_ADDR);		wreg = ((math.floor(data) * MIPI_RX0_CLEAR_OFFS)% MIPI_RX0_CLEAR_OFFE) + (rreg % MIPI_RX0_CLEAR_OFFS) + (rreg-(rreg % MIPI_RX0_CLEAR_OFFE));		ISP_Write(MIPI_RX0_CLEAR_ADDR, wreg);
def MIPI_RX0_CLEARr():
    return math.floor((ISP_Read(MIPI_RX0_CLEAR_ADDR) % MIPI_RX0_CLEAR_OFFE)/MIPI_RX0_CLEAR_OFFS);  
MIPI_RX0_LANES_ADDR = 0x0010;	MIPI_RX0_LANES_OFFS = 2**6;	MIPI_RX0_LANES_OFFE = 2**8;
def MIPI_RX0_LANESw(data):
    rreg = ISP_Read(MIPI_RX0_LANES_ADDR);		wreg = ((math.floor(data) * MIPI_RX0_LANES_OFFS)% MIPI_RX0_LANES_OFFE) + (rreg % MIPI_RX0_LANES_OFFS) + (rreg-(rreg % MIPI_RX0_LANES_OFFE));		ISP_Write(MIPI_RX0_LANES_ADDR, wreg);
def MIPI_RX0_LANESr():
    return math.floor((ISP_Read(MIPI_RX0_LANES_ADDR) % MIPI_RX0_LANES_OFFE)/MIPI_RX0_LANES_OFFS);  
MIPI_RX0_VC_ENA_ADDR = 0x0010;	MIPI_RX0_VC_ENA_OFFS = 2**2;	MIPI_RX0_VC_ENA_OFFE = 2**6;
def MIPI_RX0_VC_ENAw(data):
    rreg = ISP_Read(MIPI_RX0_VC_ENA_ADDR);		wreg = ((math.floor(data) * MIPI_RX0_VC_ENA_OFFS)% MIPI_RX0_VC_ENA_OFFE) + (rreg % MIPI_RX0_VC_ENA_OFFS) + (rreg-(rreg % MIPI_RX0_VC_ENA_OFFE));		ISP_Write(MIPI_RX0_VC_ENA_ADDR, wreg);
def MIPI_RX0_VC_ENAr():
    return math.floor((ISP_Read(MIPI_RX0_VC_ENA_ADDR) % MIPI_RX0_VC_ENA_OFFE)/MIPI_RX0_VC_ENA_OFFS);  
MIPI_RX0_RSTN_ADDR = 0x0010;	MIPI_RX0_RSTN_OFFS = 2**1;	MIPI_RX0_RSTN_OFFE = 2**2;
def MIPI_RX0_RSTNw(data):
    rreg = ISP_Read(MIPI_RX0_RSTN_ADDR);		wreg = ((math.floor(data) * MIPI_RX0_RSTN_OFFS)% MIPI_RX0_RSTN_OFFE) + (rreg % MIPI_RX0_RSTN_OFFS) + (rreg-(rreg % MIPI_RX0_RSTN_OFFE));		ISP_Write(MIPI_RX0_RSTN_ADDR, wreg);
def MIPI_RX0_RSTNr():
    return math.floor((ISP_Read(MIPI_RX0_RSTN_ADDR) % MIPI_RX0_RSTN_OFFE)/MIPI_RX0_RSTN_OFFS);  
MIPI_RX0_DPHY_RSTN_ADDR = 0x0010;	MIPI_RX0_DPHY_RSTN_OFFS = 2**0;	MIPI_RX0_DPHY_RSTN_OFFE = 2**1;
def MIPI_RX0_DPHY_RSTNw(data):
    rreg = ISP_Read(MIPI_RX0_DPHY_RSTN_ADDR);		wreg = ((math.floor(data) * MIPI_RX0_DPHY_RSTN_OFFS)% MIPI_RX0_DPHY_RSTN_OFFE) + (rreg % MIPI_RX0_DPHY_RSTN_OFFS) + (rreg-(rreg % MIPI_RX0_DPHY_RSTN_OFFE));		ISP_Write(MIPI_RX0_DPHY_RSTN_ADDR, wreg);
def MIPI_RX0_DPHY_RSTNr():
    return math.floor((ISP_Read(MIPI_RX0_DPHY_RSTN_ADDR) % MIPI_RX0_DPHY_RSTN_OFFE)/MIPI_RX0_DPHY_RSTN_OFFS);  
MIPI_TX0_FRAME_MODE_ADDR = 0x0011;	MIPI_TX0_FRAME_MODE_OFFS = 2**7;	MIPI_TX0_FRAME_MODE_OFFE = 2**8;
def MIPI_TX0_FRAME_MODEw(data):
    rreg = ISP_Read(MIPI_TX0_FRAME_MODE_ADDR);		wreg = ((math.floor(data) * MIPI_TX0_FRAME_MODE_OFFS)% MIPI_TX0_FRAME_MODE_OFFE) + (rreg % MIPI_TX0_FRAME_MODE_OFFS) + (rreg-(rreg % MIPI_TX0_FRAME_MODE_OFFE));		ISP_Write(MIPI_TX0_FRAME_MODE_ADDR, wreg);
def MIPI_TX0_FRAME_MODEr():
    return math.floor((ISP_Read(MIPI_TX0_FRAME_MODE_ADDR) % MIPI_TX0_FRAME_MODE_OFFE)/MIPI_TX0_FRAME_MODE_OFFS);  
MIPI_TX0_VC_ADDR = 0x0011;	MIPI_TX0_VC_OFFS = 2**4;	MIPI_TX0_VC_OFFE = 2**6;
def MIPI_TX0_VCw(data):
    rreg = ISP_Read(MIPI_TX0_VC_ADDR);		wreg = ((math.floor(data) * MIPI_TX0_VC_OFFS)% MIPI_TX0_VC_OFFE) + (rreg % MIPI_TX0_VC_OFFS) + (rreg-(rreg % MIPI_TX0_VC_OFFE));		ISP_Write(MIPI_TX0_VC_ADDR, wreg);
def MIPI_TX0_VCr():
    return math.floor((ISP_Read(MIPI_TX0_VC_ADDR) % MIPI_TX0_VC_OFFE)/MIPI_TX0_VC_OFFS);  
MIPI_TX0_LANES_ADDR = 0x0011;	MIPI_TX0_LANES_OFFS = 2**2;	MIPI_TX0_LANES_OFFE = 2**4;
def MIPI_TX0_LANESw(data):
    rreg = ISP_Read(MIPI_TX0_LANES_ADDR);		wreg = ((math.floor(data) * MIPI_TX0_LANES_OFFS)% MIPI_TX0_LANES_OFFE) + (rreg % MIPI_TX0_LANES_OFFS) + (rreg-(rreg % MIPI_TX0_LANES_OFFE));		ISP_Write(MIPI_TX0_LANES_ADDR, wreg);
def MIPI_TX0_LANESr():
    return math.floor((ISP_Read(MIPI_TX0_LANES_ADDR) % MIPI_TX0_LANES_OFFE)/MIPI_TX0_LANES_OFFS);  
MIPI_TX0_RSTN_ADDR = 0x0011;	MIPI_TX0_RSTN_OFFS = 2**1;	MIPI_TX0_RSTN_OFFE = 2**2;
def MIPI_TX0_RSTNw(data):
    rreg = ISP_Read(MIPI_TX0_RSTN_ADDR);		wreg = ((math.floor(data) * MIPI_TX0_RSTN_OFFS)% MIPI_TX0_RSTN_OFFE) + (rreg % MIPI_TX0_RSTN_OFFS) + (rreg-(rreg % MIPI_TX0_RSTN_OFFE));		ISP_Write(MIPI_TX0_RSTN_ADDR, wreg);
def MIPI_TX0_RSTNr():
    return math.floor((ISP_Read(MIPI_TX0_RSTN_ADDR) % MIPI_TX0_RSTN_OFFE)/MIPI_TX0_RSTN_OFFS);  
MIPI_TX0_DPHY_RSTN_ADDR = 0x0011;	MIPI_TX0_DPHY_RSTN_OFFS = 2**0;	MIPI_TX0_DPHY_RSTN_OFFE = 2**1;
def MIPI_TX0_DPHY_RSTNw(data):
    rreg = ISP_Read(MIPI_TX0_DPHY_RSTN_ADDR);		wreg = ((math.floor(data) * MIPI_TX0_DPHY_RSTN_OFFS)% MIPI_TX0_DPHY_RSTN_OFFE) + (rreg % MIPI_TX0_DPHY_RSTN_OFFS) + (rreg-(rreg % MIPI_TX0_DPHY_RSTN_OFFE));		ISP_Write(MIPI_TX0_DPHY_RSTN_ADDR, wreg);
def MIPI_TX0_DPHY_RSTNr():
    return math.floor((ISP_Read(MIPI_TX0_DPHY_RSTN_ADDR) % MIPI_TX0_DPHY_RSTN_OFFE)/MIPI_TX0_DPHY_RSTN_OFFS);  
MIPI_TX0_TYPE_ADDR = 0x0012;	MIPI_TX0_TYPE_OFFS = 2**16;	MIPI_TX0_TYPE_OFFE = 2**22;
def MIPI_TX0_TYPEw(data):
    rreg = ISP_Read(MIPI_TX0_TYPE_ADDR);		wreg = ((math.floor(data) * MIPI_TX0_TYPE_OFFS)% MIPI_TX0_TYPE_OFFE) + (rreg % MIPI_TX0_TYPE_OFFS) + (rreg-(rreg % MIPI_TX0_TYPE_OFFE));		ISP_Write(MIPI_TX0_TYPE_ADDR, wreg);
def MIPI_TX0_TYPEr():
    return math.floor((ISP_Read(MIPI_TX0_TYPE_ADDR) % MIPI_TX0_TYPE_OFFE)/MIPI_TX0_TYPE_OFFS);  
MIPI_TX0_HRES_ADDR = 0x0012;	MIPI_TX0_HRES_OFFS = 2**0;	MIPI_TX0_HRES_OFFE = 2**16;
def MIPI_TX0_HRESw(data):
    rreg = ISP_Read(MIPI_TX0_HRES_ADDR);		wreg = ((math.floor(data) * MIPI_TX0_HRES_OFFS)% MIPI_TX0_HRES_OFFE) + (rreg % MIPI_TX0_HRES_OFFS) + (rreg-(rreg % MIPI_TX0_HRES_OFFE));		ISP_Write(MIPI_TX0_HRES_ADDR, wreg);
def MIPI_TX0_HRESr():
    return math.floor((ISP_Read(MIPI_TX0_HRES_ADDR) % MIPI_TX0_HRES_OFFE)/MIPI_TX0_HRES_OFFS);  
MIPI_TX0_ULPS_EXIT_ADDR = 0x0013;	MIPI_TX0_ULPS_EXIT_OFFS = 2**8;	MIPI_TX0_ULPS_EXIT_OFFE = 2**12;
def MIPI_TX0_ULPS_EXITw(data):
    rreg = ISP_Read(MIPI_TX0_ULPS_EXIT_ADDR);		wreg = ((math.floor(data) * MIPI_TX0_ULPS_EXIT_OFFS)% MIPI_TX0_ULPS_EXIT_OFFE) + (rreg % MIPI_TX0_ULPS_EXIT_OFFS) + (rreg-(rreg % MIPI_TX0_ULPS_EXIT_OFFE));		ISP_Write(MIPI_TX0_ULPS_EXIT_ADDR, wreg);
def MIPI_TX0_ULPS_EXITr():
    return math.floor((ISP_Read(MIPI_TX0_ULPS_EXIT_ADDR) % MIPI_TX0_ULPS_EXIT_OFFE)/MIPI_TX0_ULPS_EXIT_OFFS);  
MIPI_TX0_ULPS_ENTER_ADDR = 0x0013;	MIPI_TX0_ULPS_ENTER_OFFS = 2**4;	MIPI_TX0_ULPS_ENTER_OFFE = 2**8;
def MIPI_TX0_ULPS_ENTERw(data):
    rreg = ISP_Read(MIPI_TX0_ULPS_ENTER_ADDR);		wreg = ((math.floor(data) * MIPI_TX0_ULPS_ENTER_OFFS)% MIPI_TX0_ULPS_ENTER_OFFE) + (rreg % MIPI_TX0_ULPS_ENTER_OFFS) + (rreg-(rreg % MIPI_TX0_ULPS_ENTER_OFFE));		ISP_Write(MIPI_TX0_ULPS_ENTER_ADDR, wreg);
def MIPI_TX0_ULPS_ENTERr():
    return math.floor((ISP_Read(MIPI_TX0_ULPS_ENTER_ADDR) % MIPI_TX0_ULPS_ENTER_OFFE)/MIPI_TX0_ULPS_ENTER_OFFS);  
MIPI_TX0_ULPS_CLK_EXIT_ADDR = 0x0013;	MIPI_TX0_ULPS_CLK_EXIT_OFFS = 2**1;	MIPI_TX0_ULPS_CLK_EXIT_OFFE = 2**2;
def MIPI_TX0_ULPS_CLK_EXITw(data):
    rreg = ISP_Read(MIPI_TX0_ULPS_CLK_EXIT_ADDR);		wreg = ((math.floor(data) * MIPI_TX0_ULPS_CLK_EXIT_OFFS)% MIPI_TX0_ULPS_CLK_EXIT_OFFE) + (rreg % MIPI_TX0_ULPS_CLK_EXIT_OFFS) + (rreg-(rreg % MIPI_TX0_ULPS_CLK_EXIT_OFFE));		ISP_Write(MIPI_TX0_ULPS_CLK_EXIT_ADDR, wreg);
def MIPI_TX0_ULPS_CLK_EXITr():
    return math.floor((ISP_Read(MIPI_TX0_ULPS_CLK_EXIT_ADDR) % MIPI_TX0_ULPS_CLK_EXIT_OFFE)/MIPI_TX0_ULPS_CLK_EXIT_OFFS);  
MIPI_TX0_ULPS_CLK_ENTER_ADDR = 0x0013;	MIPI_TX0_ULPS_CLK_ENTER_OFFS = 2**0;	MIPI_TX0_ULPS_CLK_ENTER_OFFE = 2**1;
def MIPI_TX0_ULPS_CLK_ENTERw(data):
    rreg = ISP_Read(MIPI_TX0_ULPS_CLK_ENTER_ADDR);		wreg = ((math.floor(data) * MIPI_TX0_ULPS_CLK_ENTER_OFFS)% MIPI_TX0_ULPS_CLK_ENTER_OFFE) + (rreg % MIPI_TX0_ULPS_CLK_ENTER_OFFS) + (rreg-(rreg % MIPI_TX0_ULPS_CLK_ENTER_OFFE));		ISP_Write(MIPI_TX0_ULPS_CLK_ENTER_ADDR, wreg);
def MIPI_TX0_ULPS_CLK_ENTERr():
    return math.floor((ISP_Read(MIPI_TX0_ULPS_CLK_ENTER_ADDR) % MIPI_TX0_ULPS_CLK_ENTER_OFFE)/MIPI_TX0_ULPS_CLK_ENTER_OFFS);  
SS_RSTN_ADDR = 0x001F;	SS_RSTN_OFFS = 2**0;	SS_RSTN_OFFE = 2**1;
def SS_RSTNw(data):
    rreg = ISP_Read(SS_RSTN_ADDR);		wreg = ((math.floor(data) * SS_RSTN_OFFS)% SS_RSTN_OFFE) + (rreg % SS_RSTN_OFFS) + (rreg-(rreg % SS_RSTN_OFFE));		ISP_Write(SS_RSTN_ADDR, wreg);
def SS_RSTNr():
    return math.floor((ISP_Read(SS_RSTN_ADDR) % SS_RSTN_OFFE)/SS_RSTN_OFFS);  
SYNC_HTW_ADDR = 0x0016;	SYNC_HTW_OFFS = 2**0;	SYNC_HTW_OFFE = 2**12;
def SYNC_HTWw(data):
    rreg = ISP_Read(SYNC_HTW_ADDR);		wreg = ((math.floor(data) * SYNC_HTW_OFFS)% SYNC_HTW_OFFE) + (rreg % SYNC_HTW_OFFS) + (rreg-(rreg % SYNC_HTW_OFFE));		ISP_Write(SYNC_HTW_ADDR, wreg);
def SYNC_HTWr():
    return math.floor((ISP_Read(SYNC_HTW_ADDR) % SYNC_HTW_OFFE)/SYNC_HTW_OFFS);  
SYNC_VTW_ADDR = 0x0017;	SYNC_VTW_OFFS = 2**0;	SYNC_VTW_OFFE = 2**11;
def SYNC_VTWw(data):
    rreg = ISP_Read(SYNC_VTW_ADDR);		wreg = ((math.floor(data) * SYNC_VTW_OFFS)% SYNC_VTW_OFFE) + (rreg % SYNC_VTW_OFFS) + (rreg-(rreg % SYNC_VTW_OFFE));		ISP_Write(SYNC_VTW_ADDR, wreg);
def SYNC_VTWr():
    return math.floor((ISP_Read(SYNC_VTW_ADDR) % SYNC_VTW_OFFE)/SYNC_VTW_OFFS);  
SYNC_HW_ADDR = 0x0018;	SYNC_HW_OFFS = 2**0;	SYNC_HW_OFFE = 2**11;
def SYNC_HWw(data):
    rreg = ISP_Read(SYNC_HW_ADDR);		wreg = ((math.floor(data) * SYNC_HW_OFFS)% SYNC_HW_OFFE) + (rreg % SYNC_HW_OFFS) + (rreg-(rreg % SYNC_HW_OFFE));		ISP_Write(SYNC_HW_ADDR, wreg);
def SYNC_HWr():
    return math.floor((ISP_Read(SYNC_HW_ADDR) % SYNC_HW_OFFE)/SYNC_HW_OFFS);  
SYNC_VW_ADDR = 0x0019;	SYNC_VW_OFFS = 2**0;	SYNC_VW_OFFE = 2**11;
def SYNC_VWw(data):
    rreg = ISP_Read(SYNC_VW_ADDR);		wreg = ((math.floor(data) * SYNC_VW_OFFS)% SYNC_VW_OFFE) + (rreg % SYNC_VW_OFFS) + (rreg-(rreg % SYNC_VW_OFFE));		ISP_Write(SYNC_VW_ADDR, wreg);
def SYNC_VWr():
    return math.floor((ISP_Read(SYNC_VW_ADDR) % SYNC_VW_OFFE)/SYNC_VW_OFFS);  
SYNC_HSP_ADDR = 0x0020;	SYNC_HSP_OFFS = 2**0;	SYNC_HSP_OFFE = 2**11;
def SYNC_HSPw(data):
    rreg = ISP_Read(SYNC_HSP_ADDR);		wreg = ((math.floor(data) * SYNC_HSP_OFFS)% SYNC_HSP_OFFE) + (rreg % SYNC_HSP_OFFS) + (rreg-(rreg % SYNC_HSP_OFFE));		ISP_Write(SYNC_HSP_ADDR, wreg);
def SYNC_HSPr():
    return math.floor((ISP_Read(SYNC_HSP_ADDR) % SYNC_HSP_OFFE)/SYNC_HSP_OFFS);  
SYNC_VSP_ADDR = 0x0021;	SYNC_VSP_OFFS = 2**0;	SYNC_VSP_OFFE = 2**11;
def SYNC_VSPw(data):
    rreg = ISP_Read(SYNC_VSP_ADDR);		wreg = ((math.floor(data) * SYNC_VSP_OFFS)% SYNC_VSP_OFFE) + (rreg % SYNC_VSP_OFFS) + (rreg-(rreg % SYNC_VSP_OFFE));		ISP_Write(SYNC_VSP_ADDR, wreg);
def SYNC_VSPr():
    return math.floor((ISP_Read(SYNC_VSP_ADDR) % SYNC_VSP_OFFE)/SYNC_VSP_OFFS);  
MTX_ON_ADDR = 0x0022;	MTX_ON_OFFS = 2**31;	MTX_ON_OFFE = 2**32;
def MTX_ONw(data):
    rreg = ISP_Read(MTX_ON_ADDR);		wreg = ((math.floor(data) * MTX_ON_OFFS)% MTX_ON_OFFE) + (rreg % MTX_ON_OFFS) + (rreg-(rreg % MTX_ON_OFFE));		ISP_Write(MTX_ON_ADDR, wreg);
def MTX_ONr():
    return math.floor((ISP_Read(MTX_ON_ADDR) % MTX_ON_OFFE)/MTX_ON_OFFS);  
MTX_HTW_ADDR = 0x0022;	MTX_HTW_OFFS = 2**0;	MTX_HTW_OFFE = 2**11;
def MTX_HTWw(data):
    rreg = ISP_Read(MTX_HTW_ADDR);		wreg = ((math.floor(data) * MTX_HTW_OFFS)% MTX_HTW_OFFE) + (rreg % MTX_HTW_OFFS) + (rreg-(rreg % MTX_HTW_OFFE));		ISP_Write(MTX_HTW_ADDR, wreg);
def MTX_HTWr():
    return math.floor((ISP_Read(MTX_HTW_ADDR) % MTX_HTW_OFFE)/MTX_HTW_OFFS);  
MTX_VTW_ADDR = 0x0023;	MTX_VTW_OFFS = 2**0;	MTX_VTW_OFFE = 2**11;
def MTX_VTWw(data):
    rreg = ISP_Read(MTX_VTW_ADDR);		wreg = ((math.floor(data) * MTX_VTW_OFFS)% MTX_VTW_OFFE) + (rreg % MTX_VTW_OFFS) + (rreg-(rreg % MTX_VTW_OFFE));		ISP_Write(MTX_VTW_ADDR, wreg);
def MTX_VTWr():
    return math.floor((ISP_Read(MTX_VTW_ADDR) % MTX_VTW_OFFE)/MTX_VTW_OFFS);  
MTX_HW_ADDR = 0x0024;	MTX_HW_OFFS = 2**0;	MTX_HW_OFFE = 2**11;
def MTX_HWw(data):
    rreg = ISP_Read(MTX_HW_ADDR);		wreg = ((math.floor(data) * MTX_HW_OFFS)% MTX_HW_OFFE) + (rreg % MTX_HW_OFFS) + (rreg-(rreg % MTX_HW_OFFE));		ISP_Write(MTX_HW_ADDR, wreg);
def MTX_HWr():
    return math.floor((ISP_Read(MTX_HW_ADDR) % MTX_HW_OFFE)/MTX_HW_OFFS);  
MTX_VW_ADDR = 0x0025;	MTX_VW_OFFS = 2**0;	MTX_VW_OFFE = 2**11;
def MTX_VWw(data):
    rreg = ISP_Read(MTX_VW_ADDR);		wreg = ((math.floor(data) * MTX_VW_OFFS)% MTX_VW_OFFE) + (rreg % MTX_VW_OFFS) + (rreg-(rreg % MTX_VW_OFFE));		ISP_Write(MTX_VW_ADDR, wreg);
def MTX_VWr():
    return math.floor((ISP_Read(MTX_VW_ADDR) % MTX_VW_OFFE)/MTX_VW_OFFS);  
MTX_HSP_ADDR = 0x0026;	MTX_HSP_OFFS = 2**0;	MTX_HSP_OFFE = 2**11;
def MTX_HSPw(data):
    rreg = ISP_Read(MTX_HSP_ADDR);		wreg = ((math.floor(data) * MTX_HSP_OFFS)% MTX_HSP_OFFE) + (rreg % MTX_HSP_OFFS) + (rreg-(rreg % MTX_HSP_OFFE));		ISP_Write(MTX_HSP_ADDR, wreg);
def MTX_HSPr():
    return math.floor((ISP_Read(MTX_HSP_ADDR) % MTX_HSP_OFFE)/MTX_HSP_OFFS);  
MTX_VSP_ADDR = 0x0027;	MTX_VSP_OFFS = 2**0;	MTX_VSP_OFFE = 2**11;
def MTX_VSPw(data):
    rreg = ISP_Read(MTX_VSP_ADDR);		wreg = ((math.floor(data) * MTX_VSP_OFFS)% MTX_VSP_OFFE) + (rreg % MTX_VSP_OFFS) + (rreg-(rreg % MTX_VSP_OFFE));		ISP_Write(MTX_VSP_ADDR, wreg);
def MTX_VSPr():
    return math.floor((ISP_Read(MTX_VSP_ADDR) % MTX_VSP_OFFE)/MTX_VSP_OFFS);  
HSYNC_WING_ADDR = 0x0028;	HSYNC_WING_OFFS = 2**5;	HSYNC_WING_OFFE = 2**10;
def HSYNC_WINGw(data):
    rreg = ISP_Read(HSYNC_WING_ADDR);		wreg = ((math.floor(data) * HSYNC_WING_OFFS)% HSYNC_WING_OFFE) + (rreg % HSYNC_WING_OFFS) + (rreg-(rreg % HSYNC_WING_OFFE));		ISP_Write(HSYNC_WING_ADDR, wreg);
def HSYNC_WINGr():
    return math.floor((ISP_Read(HSYNC_WING_ADDR) % HSYNC_WING_OFFE)/HSYNC_WING_OFFS);  
VSYNC_WING_ADDR = 0x0029;	VSYNC_WING_OFFS = 2**0;	VSYNC_WING_OFFE = 2**5;
def VSYNC_WINGw(data):
    rreg = ISP_Read(VSYNC_WING_ADDR);		wreg = ((math.floor(data) * VSYNC_WING_OFFS)% VSYNC_WING_OFFE) + (rreg % VSYNC_WING_OFFS) + (rreg-(rreg % VSYNC_WING_OFFE));		ISP_Write(VSYNC_WING_ADDR, wreg);
def VSYNC_WINGr():
    return math.floor((ISP_Read(VSYNC_WING_ADDR) % VSYNC_WING_OFFE)/VSYNC_WING_OFFS);  
CH_ADDR = 0x002a;	CH_OFFS = 2**0;	CH_OFFE = 2**3;
def CHw(data):
    rreg = ISP_Read(CH_ADDR);		wreg = ((math.floor(data) * CH_OFFS)% CH_OFFE) + (rreg % CH_OFFS) + (rreg-(rreg % CH_OFFE));		ISP_Write(CH_ADDR, wreg);
def CHr():
    return math.floor((ISP_Read(CH_ADDR) % CH_OFFE)/CH_OFFS);  
SYNC_UP_ADDR = 0x002b;	SYNC_UP_OFFS = 2**0;	SYNC_UP_OFFE = 2**1;
def SYNC_UPw(data):
    rreg = ISP_Read(SYNC_UP_ADDR);		wreg = ((math.floor(data) * SYNC_UP_OFFS)% SYNC_UP_OFFE) + (rreg % SYNC_UP_OFFS) + (rreg-(rreg % SYNC_UP_OFFE));		ISP_Write(SYNC_UP_ADDR, wreg);
def SYNC_UPr():
    return math.floor((ISP_Read(SYNC_UP_ADDR) % SYNC_UP_OFFE)/SYNC_UP_OFFS);  
MRX_R_HSP_ADDR = 0x002c;	MRX_R_HSP_OFFS = 2**0;	MRX_R_HSP_OFFE = 2**12;
def MRX_R_HSPw(data):
    rreg = ISP_Read(MRX_R_HSP_ADDR);		wreg = ((math.floor(data) * MRX_R_HSP_OFFS)% MRX_R_HSP_OFFE) + (rreg % MRX_R_HSP_OFFS) + (rreg-(rreg % MRX_R_HSP_OFFE));		ISP_Write(MRX_R_HSP_ADDR, wreg);
def MRX_R_HSPr():
    return math.floor((ISP_Read(MRX_R_HSP_ADDR) % MRX_R_HSP_OFFE)/MRX_R_HSP_OFFS);  
MRX_R_VSP_ADDR = 0x002d;	MRX_R_VSP_OFFS = 2**0;	MRX_R_VSP_OFFE = 2**12;
def MRX_R_VSPw(data):
    rreg = ISP_Read(MRX_R_VSP_ADDR);		wreg = ((math.floor(data) * MRX_R_VSP_OFFS)% MRX_R_VSP_OFFE) + (rreg % MRX_R_VSP_OFFS) + (rreg-(rreg % MRX_R_VSP_OFFE));		ISP_Write(MRX_R_VSP_ADDR, wreg);
def MRX_R_VSPr():
    return math.floor((ISP_Read(MRX_R_VSP_ADDR) % MRX_R_VSP_OFFE)/MRX_R_VSP_OFFS);  
MRX_WR_HW_ADDR = 0x002e;	MRX_WR_HW_OFFS = 2**0;	MRX_WR_HW_OFFE = 2**12;
def MRX_WR_HWw(data):
    rreg = ISP_Read(MRX_WR_HW_ADDR);		wreg = ((math.floor(data) * MRX_WR_HW_OFFS)% MRX_WR_HW_OFFE) + (rreg % MRX_WR_HW_OFFS) + (rreg-(rreg % MRX_WR_HW_OFFE));		ISP_Write(MRX_WR_HW_ADDR, wreg);
def MRX_WR_HWr():
    return math.floor((ISP_Read(MRX_WR_HW_ADDR) % MRX_WR_HW_OFFE)/MRX_WR_HW_OFFS);  
MRX_R_HTW_ADDR = 0x002f;	MRX_R_HTW_OFFS = 2**0;	MRX_R_HTW_OFFE = 2**12;
def MRX_R_HTWw(data):
    rreg = ISP_Read(MRX_R_HTW_ADDR);		wreg = ((math.floor(data) * MRX_R_HTW_OFFS)% MRX_R_HTW_OFFE) + (rreg % MRX_R_HTW_OFFS) + (rreg-(rreg % MRX_R_HTW_OFFE));		ISP_Write(MRX_R_HTW_ADDR, wreg);
def MRX_R_HTWr():
    return math.floor((ISP_Read(MRX_R_HTW_ADDR) % MRX_R_HTW_OFFE)/MRX_R_HTW_OFFS);  
MRX_R_VTW_ADDR = 0x003a;	MRX_R_VTW_OFFS = 2**0;	MRX_R_VTW_OFFE = 2**12;
def MRX_R_VTWw(data):
    rreg = ISP_Read(MRX_R_VTW_ADDR);		wreg = ((math.floor(data) * MRX_R_VTW_OFFS)% MRX_R_VTW_OFFE) + (rreg % MRX_R_VTW_OFFS) + (rreg-(rreg % MRX_R_VTW_OFFE));		ISP_Write(MRX_R_VTW_ADDR, wreg);
def MRX_R_VTWr():
    return math.floor((ISP_Read(MRX_R_VTW_ADDR) % MRX_R_VTW_OFFE)/MRX_R_VTW_OFFS);  
MRX_R_HW_ADDR = 0x003b;	MRX_R_HW_OFFS = 2**0;	MRX_R_HW_OFFE = 2**12;
def MRX_R_HWw(data):
    rreg = ISP_Read(MRX_R_HW_ADDR);		wreg = ((math.floor(data) * MRX_R_HW_OFFS)% MRX_R_HW_OFFE) + (rreg % MRX_R_HW_OFFS) + (rreg-(rreg % MRX_R_HW_OFFE));		ISP_Write(MRX_R_HW_ADDR, wreg);
def MRX_R_HWr():
    return math.floor((ISP_Read(MRX_R_HW_ADDR) % MRX_R_HW_OFFE)/MRX_R_HW_OFFS);  
MRX_R_VW_ADDR = 0x003c;	MRX_R_VW_OFFS = 2**0;	MRX_R_VW_OFFE = 2**12;
def MRX_R_VWw(data):
    rreg = ISP_Read(MRX_R_VW_ADDR);		wreg = ((math.floor(data) * MRX_R_VW_OFFS)% MRX_R_VW_OFFE) + (rreg % MRX_R_VW_OFFS) + (rreg-(rreg % MRX_R_VW_OFFE));		ISP_Write(MRX_R_VW_ADDR, wreg);
def MRX_R_VWr():
    return math.floor((ISP_Read(MRX_R_VW_ADDR) % MRX_R_VW_OFFE)/MRX_R_VW_OFFS);  
DOT_H_ADDR = 0x0030;	DOT_H_OFFS = 2**0;	DOT_H_OFFE = 2**12;
def DOT_Hw(data):
    rreg = ISP_Read(DOT_H_ADDR);		wreg = ((math.floor(data) * DOT_H_OFFS)% DOT_H_OFFE) + (rreg % DOT_H_OFFS) + (rreg-(rreg % DOT_H_OFFE));		ISP_Write(DOT_H_ADDR, wreg);
def DOT_Hr():
    return math.floor((ISP_Read(DOT_H_ADDR) % DOT_H_OFFE)/DOT_H_OFFS);  
DOT_V_ADDR = 0x0031;	DOT_V_OFFS = 2**0;	DOT_V_OFFE = 2**12;
def DOT_Vw(data):
    rreg = ISP_Read(DOT_V_ADDR);		wreg = ((math.floor(data) * DOT_V_OFFS)% DOT_V_OFFE) + (rreg % DOT_V_OFFS) + (rreg-(rreg % DOT_V_OFFE));		ISP_Write(DOT_V_ADDR, wreg);
def DOT_Vr():
    return math.floor((ISP_Read(DOT_V_ADDR) % DOT_V_OFFE)/DOT_V_OFFS);  
DOT_W_ADDR = 0x0032;	DOT_W_OFFS = 2**0;	DOT_W_OFFE = 2**12;
def DOT_Ww(data):
    rreg = ISP_Read(DOT_W_ADDR);		wreg = ((math.floor(data) * DOT_W_OFFS)% DOT_W_OFFE) + (rreg % DOT_W_OFFS) + (rreg-(rreg % DOT_W_OFFE));		ISP_Write(DOT_W_ADDR, wreg);
def DOT_Wr():
    return math.floor((ISP_Read(DOT_W_ADDR) % DOT_W_OFFE)/DOT_W_OFFS);  
