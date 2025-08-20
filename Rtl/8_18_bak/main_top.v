module  main_top(
	// input   wire			iRSTN,
	input   wire			MRCK,
	input   wire			MTCK,
	input   wire			PCK,
	input   wire			MCK,

	input	wire			MIPI_CAL_CLK,
	input	wire			MIPI_ESC_CLK,

	input   wire			PLL_TR0_LOCKED,
	input   wire			PLL_TL0_LOCKED,

	output  wire		 	oMIPI_RX0_DPHY_RSTN,				//
	output  wire		 	oMIPI_RX0_RSTN,						//
	output  wire	[3:0]	oMIPI_RX0_VC_ENA,					//MIPI_RX Virtual Chanel Default 4'b0001
	output  wire	[1:0]	oMIPI_RX0_LANES,					// 2'b00: 1 lane 2'b01: 2lane 2'b10,11 : 4lane

	input   wire	[3:0]   iMIPI_RX0_HSYNC,					// 4Bits for Virtual Ch
	input   wire	[3:0]   iMIPI_RX0_VSYNC,					// 4Bits for Virtual Ch
	input   wire	[3:0]   iMIPI_RX0_CNT,
	input   wire			iMIPI_RX0_VALID,
	input   wire	[5:0]   iMIPI_RX0_TYPE,
	input   wire	[63:0]  iMIPI_RX0_DATA,
	input   wire	[1:0]   iMIPI_RX0_VC,
	output  				iMIPI_RX0_CLEAR,
	input   wire	[17:0]  iMIPI_RX0_ERROR,					// Error BIt
	input   wire			iMIPI_RX0_ULPS_CLK,					//Not used
	input   wire	[3:0]   iMIPI_RX0_ULPS,						//Not used

	output	wire			oMIPI_TX0_DPHY_RSTN,
	output	wire			oMIPI_TX0_RSTN,
	output	wire	[ 1:0]	oMIPI_TX0_LANES,					// 2'b00: 1 lane 2'b01: 2lane 2'b10,11 : 4lane
	output	wire	   		oMIPI_TX0_FRAME_MODE,				// 1'b1: Line Start,end Packet Add
	output	wire	[15:0]	oMIPI_TX0_HRES,						// Horizontal PIXEL COUNT

	output	wire			oMIPI_TX0_HSYNC,
	output	wire			oMIPI_TX0_VSYNC,
	output	wire			oMIPI_TX0_VALID,
	output	wire	[ 5:0]	oMIPI_TX0_TYPE,						// DATA Type
	output	wire	[63:0]	oMIPI_TX0_DATA,
	output	wire	[ 1:0]	oMIPI_TX0_VC,						// Virtual CH

	output	wire			oMIPI_TX0_ULPS_CLK_ENTER,			//Not used
	output	wire			oMIPI_TX0_ULPS_CLK_EXIT,			//Not used
	output	wire	[ 3:0]	oMIPI_TX0_ULPS_ENTER,				//Not used
	output	wire	[ 3:0]	oMIPI_TX0_ULPS_EXIT,				//Not used

	input   wire			iHIIC_SCL,
	input	wire			iHIIC_SDA,
	output	wire			dHIIC_SDA,

	output	wire			dSIIC_SCL,
	input	wire			iSIIC_SDA,
	output	wire			dSIIC_SDA,
	output	wire			oSS_RSTN
);

	wire				RSTN = PLL_TR0_LOCKED & PLL_TL0_LOCKED;
//=====================================================================================================
// MAIN TOP wire
//=====================================================================================================
////	abt_top
	wire			MWE;
	wire	[15:0]	MAD_16;
	wire	[14:0]	MAD = MAD_16[14:0];
	wire	[31:0]	MDI;
	wire	[31:0]	MBE;
	wire	[31:0]	RDAT;

	wire			VLOCK;
	wire			HLOCK;


//=====================================================================================================
// REG WR
//=====================================================================================================

	wire	[ 5:0]	MIPI_RX0_TYPE = iMIPI_RX0_TYPE;
	wire	[17:0]	MIPI_RX0_ERROR = iMIPI_RX0_ERROR;
	wire	[ 1:0]	MIPI_RX0_VC = iMIPI_RX0_VC;

	

//{{ENX_WREG_BEGIN
	`m1_MIPI_RX0_DPHY_RSTN
	`m1_MIPI_RX0_RSTN
	`m4_MIPI_RX0_VC_ENA
	`m2_MIPI_RX0_LANES
	`m1_MIPI_RX0_CLEAR

	`m1_MIPI_TX0_DPHY_RSTN
	`m1_MIPI_TX0_RSTN
	`m2_MIPI_TX0_LANES
	`m1_MIPI_TX0_FRAME_MODE
	`t16_MIPI_TX0_HRES

	`m6_MIPI_TX0_TYPE
	`m2_MIPI_TX0_VC
	`m1_MIPI_TX0_ULPS_CLK_ENTER
	`m1_MIPI_TX0_ULPS_CLK_EXIT
	`m4_MIPI_TX0_ULPS_ENTER
	`m4_MIPI_TX0_ULPS_EXIT

	`m1_SS_RSTN
	
	`wMAIN_TOP
//}}ENX_WREG_END

//{{ENX_RREG_BEGIN
	`m6_MIPI_RX0_TYPE
	`m18_MIPI_RX0_ERROR
	`m2_MIPI_RX0_VC

	`rMAIN_TOP
//}}ENX_RREG_END

	assign 			oMIPI_RX0_DPHY_RSTN		= MIPI_RX0_DPHY_RSTN;
	assign 			oMIPI_RX0_RSTN			= MIPI_RX0_RSTN;
	assign 			oMIPI_RX0_VC_ENA		= MIPI_RX0_VC_ENA;
	assign 			oMIPI_RX0_LANES			= MIPI_RX0_LANES;
	assign 			iMIPI_RX0_CLEAR			= MIPI_RX0_CLEAR;

	assign 			oMIPI_TX0_DPHY_RSTN	 	= MIPI_TX0_DPHY_RSTN;
	assign 			oMIPI_TX0_RSTN		  	= MIPI_TX0_RSTN;
	assign 			oMIPI_TX0_LANES		 	= MIPI_TX0_LANES;
	assign 			oMIPI_TX0_FRAME_MODE	= MIPI_TX0_FRAME_MODE;
	assign 			oMIPI_TX0_HRES		  	= MIPI_TX0_HRES;
	assign 			oMIPI_TX0_TYPE		  	= MIPI_TX0_TYPE;
	assign 			oMIPI_TX0_VC			= MIPI_TX0_VC;
	assign 			oMIPI_TX0_ULPS_CLK_ENTER= MIPI_TX0_ULPS_CLK_ENTER;
	assign 			oMIPI_TX0_ULPS_CLK_EXIT = MIPI_TX0_ULPS_CLK_EXIT;
	assign 			oMIPI_TX0_ULPS_ENTER	= MIPI_TX0_ULPS_ENTER;
	assign 			oMIPI_TX0_ULPS_EXIT		= MIPI_TX0_ULPS_EXIT;

	assign			oSS_RSTN 				= SS_RSTN;


	wire	[31:0]	MDO_MAIN_TOP = R_MAIN_TOP | W_MAIN_TOP;

//=====================================================================================================
// ABT
//=====================================================================================================
	wire	[31:0] 	MDO_SYNC_TOP;
	wire	[31:0] 	MDO_MTX_TOP;
	wire	[31:0]	MDO_MRX_TOP;
	wire	[31:0]	MDO = MDO_MAIN_TOP | MDO_MTX_TOP | MDO_SYNC_TOP | MDO_MRX_TOP;

    wire			SLAVE_EN;

    assign			dSIIC_SCL = ~iHIIC_SCL;
    assign			dSIIC_SDA = ~(SLAVE_EN | iHIIC_SDA);

	wire			SIIC_SDA  = iSIIC_SDA|(~SLAVE_EN);
	wire			HIIC_SDO;
	assign			dHIIC_SDA = ~(HIIC_SDO & SIIC_SDA);





	wire	[5:0]	TEST_OUT;
	iic_if	IIC_IF0	(
					.RSTN			(RSTN				),
					.MCK			(MCK				),
					.iSCL			(iHIIC_SCL			),
					.iSDA			(iHIIC_SDA			),
					.SDO			(HIIC_SDO			),
					.SLAVE			(7'h49				),
					.SDO_MARGIN		(4'd4				),
					.TEST_OUT		(TEST_OUT			),
					.SLAVE_EN		(SLAVE_EN			),

					.MAD			(MAD_16				),
					.MDI			(MDI				),
					.MBE			(MBE				),
					.MWE			(MWE				),
					.MRE			(					),
					.MDO			(MDO				)
					);

//=====================================================================================================
//	Sync top
//=====================================================================================================
wire [9:0] 	Sync_DO;
wire		SYNC_ACT;
wire [9:0] 	MRX_OUT;
wire 		MRX_VALID;
wire 		MRX_VLOCK;
Sync_top SYNC_TOP (	.PCK(PCK), 
					.RSTN(RSTN),
					.DI(MRX_OUT),
					.MRX_VLOCK(MRX_VLOCK),
					.MRX_VALID(MRX_VALID),
					.MRX_FLAG_RE(MRX_FLAG_RE),
					.MAD			(MAD				),
					.MDI			(MDI				),
					.MBE			(MBE				),
					.MWE			(MWE				),
					.MCK			(MCK				),
					.MDO_SYNC_TOP	(MDO_SYNC_TOP		),
					.SYNC_HLOCK		(HLOCK			),
					.SYNC_VLOCK		(VLOCK			),
					.SYNC_ACT		(SYNC_ACT			),
					.SYNC_DO		(Sync_DO			)
					);


//=====================================================================================================
//	MIPI RX TOP
//=====================================================================================================

MRX_top MRX_TOP (
		.MRCK             	(MRCK			),
		.PCK              	(PCK			),
		.RSTN             	(RSTN			),
		.SYNC_VLOCK			(VLOCK			),
		.iMIPI_RX0_CLEAR 	(iMIPI_RX0_CLEAR),
		.iMIPI_RX0_HSYNC  	(iMIPI_RX0_HSYNC),
		.iMIPI_RX0_VSYNC  	(iMIPI_RX0_VSYNC),
		.iMIPI_RX0_CNT    	(iMIPI_RX0_CNT	),
		.iMIPI_RX0_VALID  	(iMIPI_RX0_VALID),
		.iMIPI_RX0_TYPE   	(iMIPI_RX0_TYPE	),
		.iMIPI_RX0_DATA   	(iMIPI_RX0_DATA	),
		.iMIPI_RX0_VC     	(iMIPI_RX0_VC	),
		.MRX_OUT          	(MRX_OUT		),
		.MRX_VLOCK			(MRX_VLOCK		),
		.MRX_VALID			(MRX_VALID   	),
		.MRX_FLAG_RE		(MRX_FLAG_RE	),
		.MAD				(MAD			),
		.MDI				(MDI			),
		.MBE				(MBE			),
		.MWE				(MWE			),
		.MCK				(MCK			),
		.MDO_MRX_TOP		(MDO_MRX_TOP	)
	);


//=====================================================================================================
//	ISP
//=====================================================================================================


//=====================================================================================================
//	MIPI TX TOP
//=====================================================================================================

MTX_top MTX_TOP (
		.PCK(PCK), 
		.MTCK(MTCK), 
		.SYNC_ACT(SYNC_ACT), 
		.RSTN(RSTN), 
		.DI(Sync_DO), 
		.SYNC_HLOCK(HLOCK), 
		.SYNC_VLOCK(VLOCK), 
		.oMIPI_TX0_HSYNC(oMIPI_TX0_HSYNC), 
		.oMIPI_TX0_VSYNC(oMIPI_TX0_VSYNC), 
		.oMIPI_TX0_VALID(oMIPI_TX0_VALID), 
		.oMIPI_TX0_DATA(oMIPI_TX0_DATA),
		.MAD			(MAD			),
		.MDI			(MDI			),
		.MBE			(MBE			),
		.MWE			(MWE			),
		.MCK			(MCK			),
		.MDO_MTX_TOP	(MDO_MTX_TOP	)
	);


endmodule
