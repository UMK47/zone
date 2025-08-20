 //----------------------------------------Register	MAP---------------------------------------------
//	0x0000 ~ 0x01FF	:	Write Register
//	0x0200 ~ 0x02FF	:	Read Regsiter
//	0x0300 ~ 0x06FF	:	Defect Table
//	0x0700 ~ 0x07FF	:	Shading	Table
//	0x1000 ~ 0x17FF	:	Font ID
//	0x1800 ~ 0x1FFF	:	Font Attribute
//	0x2000 ~ 0x2FFF	:	Font Data
//-------------------------------------------------------------------------------------------------

//*************************************************************************************************
// clock definition
// clock name	:	reset,	clock,	write	byte	addr,	data	data
//									enable,	enable,			input,	output
//	clock name :=	<RST> <CLK>	<WEN> <BEN>	<ADDR> <DIN> <DOUT>
//	<RST>	:= id;
//	<CLK>	:= id;
//	<WEN>	:= id;
//	<BEN>	:= id;
//	<ADDR>	:= id;
//	<DIN>	:= id;
//	<DOUT>	:= id;
//-------------------------------------------------------------------------------------------------
//{{ENX_CLK_BEGIN
`CT 			:	RSTN, 	MTCK,	MCK,	MWE, 	MBE, 	MAD, 	MDI, 	MDO	
`CR 			:	RSTN, 	MRCK,	MCK,	MWE, 	MBE, 	MAD, 	MDI, 	MDO	
`CM				:	RSTN,	MCK,	MCK,	MWE,	MBE,	MAD,	MDI,	MDO 
`CA             :   RSTN,   ACK,    MCK,	MWE,	MBE,	MAD,	MDI,	MDO
//}}ENX_CLK_END

//*************************************************************************************************
// register	name:	clock,	address			 bits,		cond.,	init. value
// Rule:
//	register name := <CLOCK> <SIZE>	_ id
//	clock	:= C UPPER(<CLOCK>)
//	address	:= number `	<FORMAT> number
//	bits	:= [ number	]
//			|= [ <MSB> : <LSB>]
//	cond.	:= 1 | id
//	init. value	:= <SIZE> '	<FORMAT> number
//
//	<CLOCK>	:= a|b|...|z						// check with the above	defined	clock name				-> naming start	error
//	<SIZE>	:= number							// check <SIZE>	in btw register	name and init. value	-> naming bit error
//	<MSB>	:= number							// check with size										-> bit error
//	<LSB>	:= number							//	"
//	<FORMAT>:= b|B|o|O|d|D|h|H					// check												-> Unknown token error
//-------------------------------------------------------------------------------------------------
//{{ENX_WREG_BEGIN
//-------------------------------------------------------------------------------------------------


`m2_MIPI_RX0_VC					:	RO, CM,	15'h000b	[ 9: 8]
`m6_MIPI_RX0_TYPE				:	RO, CM,	15'h000b	[ 5: 0]
`m18_MIPI_RX0_ERROR				:	RO, CM,	15'h000c	[17: 0]

`m1_MIPI_RX0_CLEAR				:	WR,	CM,	15'h0010	[ 8: 8],	1			,	1'h1
`m2_MIPI_RX0_LANES				:	WR,	CM,	15'h0010	[ 7: 6],	1			,	2'b01//MIPI LANE							
`m4_MIPI_RX0_VC_ENA				:	WR,	CM,	15'h0010	[ 5: 2],	1			,	4'b0001//MIPI Virtual Ch
`m1_MIPI_RX0_RSTN				:	WR,	CM,	15'h0010	[	 1],	1			,	1'h1 					
`m1_MIPI_RX0_DPHY_RSTN			:	WR,	CM,	15'h0010	[	 0],	1			,	1'h1

`m1_MIPI_TX0_FRAME_MODE			:   WR,	CM,	15'h0011	[	 7],	1			,	1'b0
`m2_MIPI_TX0_VC					:   WR,	CM,	15'h0011	[ 5: 4],	1			,	2'b00
`m2_MIPI_TX0_LANES				:   WR,	CM,	15'h0011	[ 3: 2],	1			,	2'b11
`m1_MIPI_TX0_RSTN				:   WR,	CM,	15'h0011	[	 1],	1			,	1'h1
`m1_MIPI_TX0_DPHY_RSTN			:   WR,	CM,	15'h0011	[	 0],	1			,	1'h1

`m6_MIPI_TX0_TYPE				:   WR,	CM,	15'h0012	[21:16],	1			,	6'h1e
`t16_MIPI_TX0_HRES				:   WR,	CT,	15'h0012	[15: 0],	VLOCK		,	16'd1920

`m4_MIPI_TX0_ULPS_EXIT			:   WR,	CM,	15'h0013	[11: 8],	1			,	4'h0
`m4_MIPI_TX0_ULPS_ENTER			:   WR,	CM,	15'h0013	[ 7: 4],	1			,	4'h0
`m1_MIPI_TX0_ULPS_CLK_EXIT		:   WR,	CM,	15'h0013	[ 1: 1],	1			,	1'h0
`m1_MIPI_TX0_ULPS_CLK_ENTER		:   WR,	CM,	15'h0013	[ 0: 0],	1			,	1'h0

`m1_SS_RSTN						:   WR,	CM,	15'h001F	[	 0],	1			,	1'd1

`m12_SYNC_HTW					:   WR,	CM,	15'h0016	[11: 0],	1			,	12'd2200
`m11_SYNC_VTW					:   WR,	CM,	15'h0017	[10: 0],	1			,	11'd1125
`m11_SYNC_HW					:   WR,	CM,	15'h0018	[10: 0],	1			,	11'd1920
`m11_SYNC_VW					:   WR,	CM,	15'h0019	[10: 0],	1			,	11'd1080
`m11_SYNC_HSP					:   WR,	CM,	15'h0020	[10: 0],	1			,	11'd1
`m11_SYNC_VSP					:   WR,	CM,	15'h0021	[10: 0],	1			,	11'd28

`t1_MTX_ON						:   WR,	CT,	15'h0022	[	31],	FLAG_MTCK_RE,	1'd1
`m11_MTX_HTW					:   WR,	CM,	15'h0022	[10: 0],	1			,	11'd1100
`m11_MTX_VTW					:   WR,	CM,	15'h0023	[10: 0],	1			,	11'd1125
`m11_MTX_HW						:   WR,	CM,	15'h0024	[10: 0],	1			,	11'd480
`m11_MTX_VW						:   WR,	CM,	15'h0025	[10: 0],	1			,	11'd1080
`m11_MTX_HSP					:   WR,	CM,	15'h0026	[10: 0],	1			,	11'd481
`m11_MTX_VSP					:   WR,	CM,	15'h0027	[10: 0],	1			,	11'd28
`m5_HSYNC_WING					:   WR,	CM,	15'h0028	[ 9: 5],	1			,	5'd30
`m5_VSYNC_WING					:   WR,	CM,	15'h0029	[ 4: 0],	1			,	5'd5
`m3_CH							:   WR,	CM,	15'h002a	[ 2: 0],	1			,	3'd0
`m1_SYNC_UP						:   WR,	CM,	15'h002b	[	 0],	1			,	1'd0
`m12_MRX_R_HSP					:   WR,	CM,	15'h002c	[11: 0],	1			,	12'd0	
`m12_MRX_R_VSP					:   WR,	CM,	15'h002d	[11: 0],	1			,	12'd28	
`m12_MRX_WR_HW					:   WR,	CM,	15'h002e	[11: 0],	1			,	12'd480
`m12_MRX_R_HTW					:   WR,	CM,	15'h002f	[11: 0],	1			,	12'd2200
`m12_MRX_R_VTW					:   WR,	CM,	15'h003a	[11: 0],	1			,	12'd1125
`m12_MRX_R_HW 					:   WR,	CM,	15'h003b	[11: 0],	1			,	12'd1920	
`m12_MRX_R_VW 					:   WR,	CM,	15'h003c	[11: 0],	1			,	12'd1080	

`m12_DOT_H						:   WR,	CM,	15'h0030	[11: 0],	1			,	12'd960		
`m12_DOT_V						:   WR,	CM,	15'h0031	[11: 0],	1			,	12'd540	
`m12_DOT_W						:   WR,	CM,	15'h0032	[11: 0],	1			,	12'd10	


//}}ENX_WREG_END

//*************************************************************************************************
// register	name:	clock,	address			[ bits]
//-------------------------------------------------------------------------------------------------
//{{ENX_RREG_BEGIN


//}}ENX_RREG_END

