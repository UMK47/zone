from ctypes import *
import typing
from enum import *

# def List2C_uint8List(ListDat:list):
# 	buffer_t = (c_uint8(len(ListDat)))
# 	buffer =buffer_t(*ListDat)
# 	return buffer

class FT_STATUS(Enum):
	FT_OK							= 0
	FT_INVALID_HANDLE				= 1
	FT_DEVICE_NOT_FOUND				= 2
	FT_DEVICE_NOT_OPENED			= 3
	FT_IO_ERROR						= 4
	FT_INSUFFICIENT_RESOURCES		= 5
	FT_INVALID_PARAMETER			= 6
	FT_INVALID_BAUD_RATE			= 7
	FT_DEVICE_NOT_OPENED_FOR_ERASE	= 8
	FT_DEVICE_NOT_OPENED_FOR_WRITE	= 9
	FT_FAILED_TO_WRITE_DEVICE		= 10
	FT_EEPROM_READ_FAILED			= 11
	FT_EEPROM_WRITE_FAILED			= 12
	FT_EEPROM_ERASE_FAILED			= 13
	FT_EEPROM_NOT_PRESENT			= 14
	FT_EEPROM_NOT_PROGRAMMED		= 15
	FT_INVALID_ARGS					= 16
	FT_NOT_SUPPORTED				= 17
	FT_OTHER_ERROR					= 18
	FT_DEVICE_LIST_NOT_READY		= 19

class FT_DEVICE_LIST_INFO_NODE(Structure):
	'''	typedef struct _ft_device_list_info_node {
			ULONG Flags;
			ULONG Type;
			ULONG ID;
			DWORD LocId;
			char SerialNumber[16];
			char Description[64];
			FT_HANDLE ftHandle;
		} FT_DEVICE_LIST_INFO_NODE;'''
	_fields_ = [
		('Flags'		, c_uint	),
		('Type'			, c_uint	),
		('ID'			, c_uint	),
		('LocId'		, c_uint	),
		('SerialNumber'	, c_char*16	),
		('Description'	, c_char*64	),
		('ftHandle'		, c_void_p	)]	
	def __repr__(self):
		return f"""FT_DEVICE_LIST_INFO_MODEFlags = {self.Flags},Type = {self.Type},ID = {self.ID},LocId = {self.LocId},SerialNumber = {self.SerialNumber},Description = {self.Description},ftHandle = {self.ftHandle}"""


class ChannelConfig_SPI(Structure):
	_fields_ = [
		("ClockRate"	, c_uint32,	32	),
		("LatencyTimer"	, c_uint8,	8	),
		("configOptions", c_uint32,	32	),
		("Pin"			, c_uint32,	32	),
		("reserved"		, c_uint16,	16	)] 
	def __repr__(self):
		return f'ChannelConfig_SPI(ClockRate={self.ClockRate},LatencyTimer={self.LatencyTimer},configOptions={self.configOptions},Pin={self.Pin},reserved={self.reserved}'



class FTDI_SPI():
	
# transferOptions-Bit0: If this bit is 0 then it means that the transfer size provided is in bytes */
	SPI_TRANSFER_OPTIONS_SIZE_IN_BYTES			= 0x00000000
# transferOptions-Bit0: If this bit is 1 then it means that the transfer size provided is in bytes */
	SPI_TRANSFER_OPTIONS_SIZE_IN_BITS			= 0x00000001
# transferOptions-Bit1: if BIT1 is 1 then CHIP_SELECT line will be enabled at start of transfer */
	SPI_TRANSFER_OPTIONS_CHIPSELECT_ENABLE		= 0x00000002
# transferOptions-Bit2: if BIT2 is 1 then CHIP_SELECT line will be disabled at end of transfer */
	SPI_TRANSFER_OPTIONS_CHIPSELECT_DISABLE		= 0x00000004
# Bit defination of the Options member of configOptions structure*/
	SPI_CONFIG_OPTION_MODE_MASK		= 0x00000003
	SPI_CONFIG_OPTION_MODE0			= 0x00000000
	SPI_CONFIG_OPTION_MODE1			= 0x00000001
	SPI_CONFIG_OPTION_MODE2			= 0x00000002
	SPI_CONFIG_OPTION_MODE3			= 0x00000003
	SPI_CONFIG_OPTION_CS_MASK		= 0x0000001C
	SPI_CONFIG_OPTION_CS_DBUS3		= 0x00000000
	SPI_CONFIG_OPTION_CS_DBUS4		= 0x00000004
	SPI_CONFIG_OPTION_CS_DBUS5		= 0x00000008
	SPI_CONFIG_OPTION_CS_DBUS6		= 0x0000000C
	SPI_CONFIG_OPTION_CS_DBUS7		= 0x00000010
	SPI_CONFIG_OPTION_CS_ACTIVELOW	= 0x00000020

	def __init__(self,dll_path):
		self.path_dll = dll_path
		self.p = cdll.LoadLibrary(dll_path)
		self.handle = c_void_p()
		self.set_channelConfig(ClockRate=1000000,LatencyTimer=1,configOptions=self.SPI_CONFIG_OPTION_MODE0 | self.SPI_CONFIG_OPTION_CS_DBUS3 | self.SPI_CONFIG_OPTION_CS_ACTIVELOW,Pin=0)

	def set_channelConfig(self,ClockRate=1000000,LatencyTimer=1,configOptions=SPI_CONFIG_OPTION_MODE0 | SPI_CONFIG_OPTION_CS_DBUS3 | SPI_CONFIG_OPTION_CS_ACTIVELOW,Pin=0)->None:
		self.channelConf = ChannelConfig_SPI(ClockRate=ClockRate ,LatencyTimer=LatencyTimer ,Options=configOptions,Pin=Pin)

	################################################################################################################################ Init
	def SPI_Init(self,index):
		self.Init_libMPSSE()
		self.SPI_OpenChannel(index,pointer(self.handle))
		

		self.channelConf.configOptions=0x20
		self.channelConf.Pin=0
		self.channelConf.reserved=0
		self.SPI_InitChannel(self.handle,pointer(self.channelConf))

	def Init_libMPSSE(self)->None:
		'''FTDI_API void Init_libMPSSE(void);'''
		self.p.Init_libMPSSE()
		return None
	def SPI_OpenChannel(self,index:c_uint32, handle:c_void_p)->FT_STATUS:
		'''FTDI_API FT_STATUS SPI_OpenChannel(uint32 index, FT_HANDLE *handle);'''
		self.Status=FT_STATUS(self.p.SPI_OpenChannel(index,handle))
		return self.Status
	def SPI_InitChannel(self,handle:c_void_p,config:c_void_p)->FT_STATUS:
		'''FTDI_API FT_STATUS SPI_InitChannel(FT_HANDLE handle, ChannelConfig *config);'''
		self.Status=FT_STATUS(self.p.SPI_InitChannel(handle,config))
		return self.Status


	################################################################################################################################ de-Init

	def SPI_deInit(self):
		self.SPI_CloseChannel(self.handle)
		self.Cleanup_libMPSSE()

	def SPI_CloseChannel(self,handle:c_void_p)->FT_STATUS:
		'''FTDI_API FT_STATUS SPI_CloseChannel(FT_HANDLE handle);'''
		self.Status=FT_STATUS(self.p.SPI_CloseChannel(handle))
		return self.Status

	def Cleanup_libMPSSE(self)->None:
		'''FTDI_API void Cleanup_libMPSSE(void);'''
		self.p.Cleanup_libMPSSE()
		return None

	################################################################################################################################ Read & Write
	def SPI_RegRead(self,addr:int):
		zero_list = [0,0,0,0]
		buffer_t = (c_uint8 * len(zero_list))
		buffer =buffer_t(*zero_list)
		
		addr_upper=c_uint8(addr>>8)
		addr_lower=c_uint8(addr)
		buffer[0]=addr_upper
		buffer[1]=addr_lower

		sizeTransfered = c_uint32(0)
		self.SPI_Write(self.handle,buffer, c_uint32(2), pointer(sizeTransfered),
			c_uint32(self.SPI_TRANSFER_OPTIONS_SIZE_IN_BYTES
					|self.SPI_TRANSFER_OPTIONS_CHIPSELECT_ENABLE))
		
		sizeTransfered = c_uint32(0)
		buffer[0] = 0
		buffer[1] = 0
		buffer[2] = 0
		buffer[3] = 0
		self.SPI_Read(self.handle,buffer, c_uint32(4) , pointer(sizeTransfered),
			c_uint32(self.SPI_TRANSFER_OPTIONS_SIZE_IN_BYTES
					|self.SPI_TRANSFER_OPTIONS_CHIPSELECT_DISABLE))
		return buffer

	def SPI_RegWrite(self,Addr:int, Data:int):
		sizeTransfered = c_uint32(0)

		zero_list = [0,0,0,0,0,0]
		buffer_t = (c_uint8 * len(zero_list))
		buffer =buffer_t(*zero_list)

		
		buffer[0] = c_uint8(Addr>>8)
		buffer[1] = c_uint8(Addr)
		buffer[2] = c_uint8(Data>>24)
		buffer[3] = c_uint8(Data>>16)
		buffer[4] = c_uint8(Data>>8)
		buffer[5] = c_uint8(Data>>0)

		self.SPI_Write(self.handle, buffer, c_uint32(6), pointer(sizeTransfered),c_uint32(self.SPI_TRANSFER_OPTIONS_SIZE_IN_BYTES|self.SPI_TRANSFER_OPTIONS_CHIPSELECT_ENABLE|self.SPI_TRANSFER_OPTIONS_CHIPSELECT_DISABLE))
		# self.Status=FT_STATUS(self.p.SPI_Write(self.handle,buffer,6,pointer(sizeTransfered),params))

		return self.Status
		
	def SPI_Read(self,handle:c_void_p,buffer:c_void_p,sizeToTransfer:c_uint32,sizeTransfered:c_void_p,params:c_uint32)-> FT_STATUS:
		'''FTDI_API FT_STATUS SPI_Read( FT_HANDLE handle, uint8 *buffer,uint32 sizeToTransfer, uint32 *sizeTransfered, uint32 options);'''
		self.Status=FT_STATUS(self.p.SPI_Read(handle,buffer,sizeToTransfer,sizeTransfered,params))
		return self.Status
	def SPI_Write(self,handle:c_void_p,buffer:c_void_p,sizeToTransfer:c_uint32,sizeTransfered:c_void_p,params:c_uint32)-> FT_STATUS:
		'''FTDI_API FT_STATUS SPI_Write(FT_HANDLE handle, uint8 *buffer,uint32 sizeToTransfer, uint32 *sizeTransfered, uint32 options);'''
		self.Status=FT_STATUS(self.p.SPI_Write(handle,buffer,sizeToTransfer,sizeTransfered,params))
		return self.Status
	################################################################################################################################ Write

	def SPI_GetNumChannels(self,numChannels:c_void_p)->FT_STATUS:
		'''FTDI_API FT_STATUS SPI_GetNumChannels(uint32 *numChannels);'''
		self.Status=FT_STATUS(self.p.SPI_GetNumChannels(numChannels))
		return self.Status
	def SPI_GetChannelInfo(self,index:c_uint32,chanInfo:c_void_p)-> FT_STATUS:
		'''FTDI_API FT_STATUS SPI_GetChannelInfo(uint32 index,FT_DEVICE_LIST_INFO_NODE *chanInfo);'''
		self.Status=FT_STATUS(self.p.SPI_GetChannelInfo(index,chanInfo))
		return self.Status
	def SPI_ReadWrite(self,handle:c_void_p,inBuffer:c_void_p,outBuffer:c_void_p,sizeToTransfer:c_uint32,sizeTransferred:c_void_p,transferOptions:c_uint32)->FT_STATUS:
		'''FTDI_API FT_STATUS SPI_ReadWrite(FT_HANDLE handle, uint8 *inBuffer,uint8 *outBuffer, uint32 sizeToTransfer, uint32 *sizeTransferred,uint32 transferOptions);'''
		self.Status=FT_STATUS(self.p.SPI_ReadWrite(handle,inBuffer,outBuffer,sizeToTransfer,sizeTransferred,transferOptions))
		return self.Status
	def SPI_IsBusy(self,handle:c_void_p,state:c_void_p)->FT_STATUS:
		'''FTDI_API FT_STATUS SPI_IsBusy(FT_HANDLE handle, bool *state);'''
		self.Status=FT_STATUS(self.p.SPI_IsBusy(handle,state))
		return self.Status
	def SPI_ChangeCS(self,handle:c_void_p,configOptions:c_uint32)->FT_STATUS:
		'''FTDI_API FT_STATUS SPI_ChangeCS(FT_HANDLE handle, uint32 configOptions);'''
		self.Status=FT_STATUS(self.p.SPI_ChangeCS(handle,configOptions))
		return self.Status
	def FT_WriteGPIO(self,	handle:c_void_p, direction:c_uint8,value:c_uint8)->FT_STATUS:
		'''FTDI_API FT_STATUS FT_WriteGPIO(FT_HANDLE handle, uint8 dir, uint8 value);'''
		self.Status=FT_STATUS(self.p.FT_WriteGPIO(handle,direction,value))
		return self.Status
	def FT_ReadGPIO(self,	handle:c_void_p, value:c_void_p)->FT_STATUS:
		'''FTDI_API FT_STATUS FT_ReadGPIO(FT_HANDLE handle,uint8 *value);'''
		self.Status=FT_STATUS(self.p.FT_ReadGPIO(handle,value))
		return self.Status
	def SPI_ToggleCS(self,	handle:c_void_p, state:c_bool)->FT_STATUS:
		'''FTDI_API FT_STATUS SPI_ToggleCS(FT_HANDLE handle, bool state);'''
		self.Status=FT_STATUS(self.p.SPI_ToggleCS(handle,state))
		return self.Status






