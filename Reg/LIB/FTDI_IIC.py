# FTDI_API FT_STATUS I2C_DeviceRead( FT_HANDLE handle, uint32 deviceAddress,uint32 sizeToTransfer, uint8 *buffer, uint32 *sizeTransfered, uint32 options); \
# FTDI_API FT_STATUS I2C_DeviceWrite(FT_HANDLE handle, uint32 deviceAddress,uint32 sizeToTransfer, uint8 *buffer, uint32 *sizeTransfered, uint32 options); \

# FTDI_API FT_STATUS I2C_GetNumChannels(uint32 *numChannels); \
# FTDI_API FT_STATUS I2C_GetChannelInfo(uint32 index,FT_DEVICE_LIST_INFO_NODE *chanInfo); \
# FTDI_API FT_STATUS I2C_OpenChannel(uint32 index, FT_HANDLE *handle); \
# FTDI_API FT_STATUS I2C_InitChannel(FT_HANDLE handle, ChannelConfig *config); \
# FTDI_API FT_STATUS I2C_CloseChannel(FT_HANDLE handle); \
# FTDI_API FT_STATUS FT_ReadGPIO(FT_HANDLE handle,uint8 *value); \
# FTDI_API FT_STATUS FT_WriteGPIO(FT_HANDLE handle, uint8 dir, uint8 value); \
# FTDI_API void      Init_libMPSSE(void); \
# FTDI_API void      Cleanup_libMPSSE(void); \



from ctypes import *
from enum import Enum
import typing

class I2C_CLOCKRATE(Enum):
	I2C_CLOCK_STANDARD_MODE   = 100000 ,
	I2C_CLOCK_FAST_MODE       = 400000 ,
	I2C_CLOCK_FAST_MODE_PLUS  = 1000000,
	I2C_CLOCK_HIGH_SPEED_MODE = 3400000

class _ft_device_list_info_node (Structure):
	_fields_ = [
		("Flags"		, c_ulong	),	# 	ULONG Flags;
		("Type"			, c_ulong	),	# 	ULONG Type;
		("ID"			, c_ulong	),	# 	ULONG ID;
		("LocId"		, c_uint	),	# 	DWORD LocId;
		("SerialNumber"	, c_char*16	),	# 	char SerialNumber[16];
		("Description"	, c_char*64	),	# 	char Description[64];
		("ftHandle"		, c_void_p	),	# 	FT_HANDLE ftHandle;
	]

class ChannelConfig_t(Structure):
	_fields_ = [("ClockRate"   ,c_uint32	),
				("LatencyTimer",c_uint8 ,8	),
				("Options"     ,c_uint32,32	)]
	def __repr__(self):
		return f'ChannelConfig_t(ClockRate={self.ClockRate},LatencyTimer={self.LatencyTimer},Options={self.Options})'

class Device_status(Enum):
	FT_OK							= (0),
	FT_INVALID_HANDLE				= (1),
	FT_DEVICE_NOT_FOUND				= (2),
	FT_DEVICE_NOT_OPENED			= (3),
	FT_IO_ERROR						= (4),
	FT_INSUFFICIENT_RESOURCES		= (5),
	FT_INVALID_PARAMETER			= (6),
	FT_INVALID_BAUD_RATE			= (7),
	FT_DEVICE_NOT_OPENED_FOR_ERASE	= (8),
	FT_DEVICE_NOT_OPENED_FOR_WRITE	= (9),
	FT_FAILED_TO_WRITE_DEVICE		= (10),
	FT_EEPROM_READ_FAILED			= (11),
	FT_EEPROM_WRITE_FAILED			= (12),
	FT_EEPROM_ERASE_FAILED			= (13),
	FT_EEPROM_NOT_PRESENT			= (14),
	FT_EEPROM_NOT_PROGRAMMED		= (15),
	FT_INVALID_ARGS					= (16),
	FT_NOT_SUPPORTED				= (17),
	FT_OTHER_ERROR					= (18),
	FT_DEVICE_LIST_NOT_READY		= (19)




class FTDI_IIC():
	I2C_TRANSFER_OPTIONS_START_BIT			= (0x00000001)
	I2C_TRANSFER_OPTIONS_STOP_BIT			= (0x00000002)
	I2C_TRANSFER_OPTIONS_BREAK_ON_NACK		= (0x00000004)
	I2C_TRANSFER_OPTIONS_NACK_LAST_BYTE		= (0x00000008)
	I2C_TRANSFER_OPTIONS_FAST_TRANSFER		= (0x00000030)
	I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BYTES= (0x00000010)
	I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BITS	= (0x00000020)
	I2C_TRANSFER_OPTIONS_NO_ADDRESS			= (0x00000040)

	def __init__(self,dll_path):
		self.path_dll = dll_path
		self.p= cdll.LoadLibrary(dll_path)
		self.handle = c_void_p()
		self.Set_Channel()
		
	def Set_Channel(self,ClockRate=400000,LatencyTimer=0,Options=0):
		self.ChannelConfig = ChannelConfig_t(ClockRate=ClockRate ,LatencyTimer=LatencyTimer ,Options=Options )

	def IIC_Init(self,index)->tuple:
		self.init_libMPSSE()
		OpenStatus = self.I2C_OpenChannel(c_uint32(index), pointer(self.handle       ))
		InitStatus = self.I2C_InitChannel(self.handle    , pointer(self.ChannelConfig))
		self.Set_Channel()
		return (OpenStatus,InitStatus)
	
	def IIC_deInit(self):
		self.I2C_CloseChannel(self.handle)
		self.Cleanup_libMPSSE()


	def IIC_Read(self,slvAddr,size):
		C_SlvAddr=(slvAddr)
		sizeToTransfer = size
		zero_list=[0 for i in range(size)]

		buffer_t = (c_uint8 * len(zero_list))
		buffer=buffer_t(*zero_list)

		bytesTransfered = c_void_p()
		bytesTransfered.contents=0

		params = 0
		params = params|self.I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BYTES
		params = params|self.I2C_TRANSFER_OPTIONS_START_BIT
		params = params|self.I2C_TRANSFER_OPTIONS_STOP_BIT
        # params = params|self.I2C_TRANSFER_OPTIONS_NO_ADDRESS


		self.I2C_DeviceRead( self.handle,c_uint32(C_SlvAddr)    ,c_uint32(sizeToTransfer),   buffer        ,   pointer(bytesTransfered)   , c_uint32(params))

		return buffer

	def IIC_txWords(self,slvAddr,txList):
		C_SlvAddr=(slvAddr)
		length=txList.__len__()

		bytesTransfered = c_void_p()
		bytesTransfered.contents=0

		bytesToTransfer = length
			
		buffer_t = (c_uint8 * len(txList))
		buffer=buffer_t(*txList)

		params = 0
		params = params|self.I2C_TRANSFER_OPTIONS_FAST_TRANSFER
		params = params|self.I2C_TRANSFER_OPTIONS_START_BIT
		params = params|self.I2C_TRANSFER_OPTIONS_STOP_BIT
		# params = params|self.I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BITS

		self.I2C_DeviceWrite(self.handle,c_uint32(C_SlvAddr),c_uint32(bytesToTransfer),buffer,pointer(bytesTransfered),c_uint32(params))




















		
	def init_libMPSSE(self):
		self.p.Init_libMPSSE()
	def Cleanup_libMPSSE(self):
		self.p.Cleanup_libMPSSE()

	def FT_WriteGPIO(self,handle: c_void_p ,dir: c_uint8 ,value: c_uint8): 
		self.Status= self.p.FT_WriteGPIO(handle, c_uint8(dir),c_uint8(value))
		return self.Status

	def FT_ReadGPIO(self,handle, uint8p_value):
		self.Status= self.p.FT_ReadGPIO(handle,uint8p_value)
		return self.Status

	def I2C_InitChannel(self,handle, pointer_config):
		self.Status= self.p.I2C_InitChannel(handle,pointer_config)
		return self.Status
	def I2C_CloseChannel(self,handle):
		self.Status= self.p.I2C_CloseChannel(handle)
		return self.Status

	# FTDI_API FT_STATUS I2C_OpenChannel(uint32 index, FT_HANDLE *handle);
	def I2C_OpenChannel(self,uint32_index,pointer_handle):
		self.Status= self.p.I2C_OpenChannel(uint32_index,pointer_handle)
		return self.Status

	# FTDI_API FT_STATUS I2C_GetChannelInfo(uint32 index,FT_DEVICE_LIST_INFO_NODE *chanInfo);
	def I2C_GetChannelInfo(self,uint32_index,FT_DEVICE_LIST_INFO_NODE_p_chanInfo):
		self.Status= self.p.I2C_GetChannelInfo(uint32_index,FT_DEVICE_LIST_INFO_NODE_p_chanInfo)
		return self.Status

	def I2C_GetNumChannels(self,uint32_p_numChannels):
		self.Status= self.p.I2C_GetNumChannels(uint32_p_numChannels)
		return self.Status

	def I2C_DeviceRead(self,handle, uint32_deviceAddress,uint32_sizeToTransfer, uint8_p_buffer, uint32_p_sizeTransfered, uint32_options):
		self.Status= self.p.I2C_DeviceRead(handle, uint32_deviceAddress,uint32_sizeToTransfer, uint8_p_buffer, uint32_p_sizeTransfered, uint32_options)
		return self.Status

	def I2C_DeviceWrite(self,handle, uint32_deviceAddress,uint32_sizeToTransfer, uint8_p_buffer, uint32_p_sizeTransfered, uint32_options):
		self.Status= self.p.I2C_DeviceWrite(handle, uint32_deviceAddress,uint32_sizeToTransfer, uint8_p_buffer, uint32_p_sizeTransfered, uint32_options)
		return self.Status

	def __str__(self):
		return f"Status : {self.status_dcoder(self.Status)}"

	def status_dcoder(self,status):
		if   status == Device_status.FT_OK.value[0]								: str = "FT_OK"							
		elif status == Device_status.FT_INVALID_HANDLE.value[0]					: str = "FT_INVALID_HANDLE"				
		elif status == Device_status.FT_DEVICE_NOT_FOUND.value[0]				: str = "FT_DEVICE_NOT_FOUND"				
		elif status == Device_status.FT_DEVICE_NOT_OPENED.value[0]				: str = "FT_DEVICE_NOT_OPENED"				
		elif status == Device_status.FT_IO_ERROR.value[0]						: str = "FT_IO_ERROR"						
		elif status == Device_status.FT_INSUFFICIENT_RESOURCES.value[0]			: str = "FT_INSUFFICIENT_RESOURCES"		
		elif status == Device_status.FT_INVALID_PARAMETER.value[0]				: str = "FT_INVALID_PARAMETER"				
		elif status == Device_status.FT_INVALID_BAUD_RATE.value[0]				: str = "FT_INVALID_BAUD_RATE"				
		elif status == Device_status.FT_DEVICE_NOT_OPENED_FOR_ERASE.value[0]	: str = "FT_DEVICE_NOT_OPENED_FOR_ERASE"	
		elif status == Device_status.FT_DEVICE_NOT_OPENED_FOR_WRITE.value[0]	: str = "FT_DEVICE_NOT_OPENED_FOR_WRITE"	
		elif status == Device_status.FT_FAILED_TO_WRITE_DEVICE.value[0]			: str = "FT_FAILED_TO_WRITE_DEVICE"		
		elif status == Device_status.FT_EEPROM_READ_FAILED.value[0]				: str = "FT_EEPROM_READ_FAILED"			
		elif status == Device_status.FT_EEPROM_WRITE_FAILED.value[0]			: str = "FT_EEPROM_WRITE_FAILED"			
		elif status == Device_status.FT_EEPROM_ERASE_FAILED.value[0]			: str = "FT_EEPROM_ERASE_FAILED"			
		elif status == Device_status.FT_EEPROM_NOT_PRESENT.value[0]				: str = "FT_EEPROM_NOT_PRESENT"			
		elif status == Device_status.FT_EEPROM_NOT_PROGRAMMED.value[0]			: str = "FT_EEPROM_NOT_PROGRAMMED"			
		elif status == Device_status.FT_INVALID_ARGS.value[0]					: str = "FT_INVALID_ARGS"					
		elif status == Device_status.FT_NOT_SUPPORTED.value[0]					: str = "FT_NOT_SUPPORTED"					
		elif status == Device_status.FT_OTHER_ERROR.value[0]					: str = "FT_OTHER_ERROR"					
		elif status == Device_status.FT_DEVICE_LIST_NOT_READY.value[0]			: str = "FT_DEVICE_LIST_NOT_READY"			

		return str


