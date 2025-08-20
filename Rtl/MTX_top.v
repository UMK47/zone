module MTX_top(
	input 				PCK,
	input 				MTCK,
	input 				RSTN,
	input 				[9:0] 	DI,
	input 				SYNC_HLOCK,
	input 				SYNC_VLOCK,
	input				SYNC_ACT,
    input   			[14:0]	MAD,
    input  				[31:0]	MDI,
    input  				[31:0]	MBE,
    input  						MWE,
    input   					MCK,
    output   			[31:0]	MDO_MTX_TOP,
	output	reg			oMIPI_TX0_HSYNC,
	output	reg 		oMIPI_TX0_VSYNC,
	output	reg			oMIPI_TX0_VALID,
	output	reg	[63:0]	oMIPI_TX0_DATA
);

wire		FLAG_MTCK_RE;

//{{ENX_WREG_BEGIN
	`m11_MTX_HTW
	`m11_MTX_VTW
	`m11_MTX_HW
	`m11_MTX_VW
	`m11_MTX_HSP
	`m11_MTX_VSP
	`m5_HSYNC_WING
	`m5_VSYNC_WING
	`t1_MTX_ON

	`wMTX_TOP
//}}ENX_WREG_END

assign  MDO_MTX_TOP = W_MTX_TOP;

// parameter MTX_HTW = 11'd1100;
// parameter MTX_VTW = 11'd1125;

// parameter MTX_HW = 10'd480;
// parameter MTX_VW = 11'd1080;

// parameter MTX_HSP =10'd486;
// parameter MTX_VSP = 10'd10;

// parameter HSYNC_WING = 5'd30;
// parameter VSYNC_WING = 5'd5;


reg [9:0] DATA_1;
reg [9:0] DATA_2; 
reg [9:0] DATA_3; 
reg	 [63:0] DATA_WRITE;
wire [63:0] DATA_T = {DI[9:2], 8'h80, DATA_1[9:2], 8'h80, DATA_2[9:2], 8'h80, DATA_3[9:2], 8'h80};

reg T_CNT_START;
reg 	[10:0] 		T_CNT;
wire	[8:0] 		ADDRESS_CNT = T_CNT[10:2];
wire 	[1:0] 		DATA_CNT = T_CNT[1:0];

//READ 부분
reg FLAG_PCK;
reg FLAG_MTCK1;
reg FLAG_MTCK2; 
reg FLAG_MTCK3;

reg		[10:0]	R_HCNT;		//9비트, 1100까지
reg 	[10:0]	R_VCNT;	//11비트, 1125

wire 	[63:0] 	DATA_READ;	//MEM에서 읽은 값
reg		[8:0]	R_ADDRESS_CNT;

wire ACT_H = (MTX_HSP <= R_HCNT) & (R_HCNT < MTX_HSP + MTX_HW);
wire ACT_V = (MTX_VSP <= R_VCNT) & (R_VCNT < MTX_VSP + MTX_VW);
wire ACT_T = ACT_H & ACT_V;
reg ACT_T_1D;	//ACT_T에 R_ADDRESS 증가
reg ACT_T_2D;	//ACT_T_1D에 DATA_READ 나옴. ACT_T_2D에 mipi 출력하면 딱.

wire DATA_EN = DATA_CNT == 2'd3;


//tp: two ports, A:read, B:write
tpsram 
#(
    .WordWidth	(64),
    .WordDepth	(480)
)
u1
(
	.QA(DATA_READ),
  	.CLKA(MTCK),
  	.CLKB(PCK),
  	.CENA(~ACT_T),
  	.CENB(~DATA_EN),
  	.AA(R_ADDRESS_CNT),
  	.AB(ADDRESS_CNT),
  	.DB(DATA_WRITE)
);


//DATA_1
always @ (posedge PCK or negedge RSTN) begin
	if(!RSTN)		DATA_1 <= 10'b0;
	else			DATA_1 <= DI;
end

//DATA_2
always @ (posedge PCK or negedge RSTN) begin
	if(!RSTN)		DATA_2 <= 10'b0;
	else 			DATA_2 <= DATA_1;
end

//DATA_3
always @ (posedge PCK or negedge RSTN) begin
	if(!RSTN) 		DATA_3 <= 10'b0;
	else 			DATA_3 <= DATA_2;
end


wire T_CNT_RST = (T_CNT == {MTX_HW, 2'd3})|SYNC_VLOCK;



// T_CNT
always @(posedge PCK or negedge RSTN) begin
    if (!RSTN)         T_CNT <= 11'd0;
    else if (SYNC_ACT)
        if (T_CNT_RST) T_CNT <= 11'd0;
        else           T_CNT <= T_CNT + 11'd1;
    else               T_CNT <= 11'd0;
end


//DATA_WRITE
always @ (posedge PCK or negedge RSTN) begin
	if(!RSTN) 					DATA_WRITE <= 64'b0;
	else if(DATA_CNT == 2'd3)	DATA_WRITE <= DATA_T;
	
end


///////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////READ 시작///////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////

//FLAG_PCK
always @ (posedge PCK or negedge RSTN) begin
	if(!RSTN) begin
		FLAG_PCK <= 1'b0;
	end else if(SYNC_VLOCK) begin
		FLAG_PCK <= ~FLAG_PCK;
	end
end

//FLAG_MTCK1
always @ (posedge MTCK or negedge RSTN) begin
	if(!RSTN)	FLAG_MTCK1 <= 1'b0;
	else		FLAG_MTCK1 <= FLAG_PCK;
end

//FLAG_MTCK2
always @ (posedge MTCK or negedge RSTN) begin
	if(!RSTN)	FLAG_MTCK2 <= 1'b0;
	else		FLAG_MTCK2 <= FLAG_MTCK1;
end

//FLAG_MTCK3
always @ (posedge MTCK or negedge RSTN) begin
	if(!RSTN)	FLAG_MTCK3 <= 1'b0;
	else		FLAG_MTCK3 <= FLAG_MTCK2;
end

assign FLAG_MTCK_RE = FLAG_MTCK2 ^ FLAG_MTCK3;


wire R_HCNT_RST = (R_HCNT == MTX_HTW-1)| FLAG_MTCK_RE;
//R_HCNT
always @ (posedge MTCK or negedge RSTN) begin
	if(!RSTN )
		R_HCNT <= 11'b0;
	else if(R_HCNT_RST)
		R_HCNT <= 11'b0;
	else
		R_HCNT <= R_HCNT + 11'b1;
end

//R_VCNT
always @ (posedge MTCK or negedge RSTN) begin
	if(!RSTN) 				R_VCNT <= 11'b0;
	else if(FLAG_MTCK_RE)	R_VCNT <= 11'b0;
	else if(R_HCNT == MTX_HTW-1)
		if(R_VCNT == MTX_VTW-1)	R_VCNT <= 11'b0;
		else					R_VCNT <= R_VCNT + 11'b1;
	else					R_VCNT <= R_VCNT;
end

//ACT_T_1D
always @ (posedge MTCK or negedge RSTN) begin
	if(!RSTN)		ACT_T_1D <= 1'b0;
	else			ACT_T_1D <= ACT_T;
end
 
//ACT_T_2D
always @ (posedge MTCK or negedge RSTN) begin
	if(!RSTN)		ACT_T_2D <= 1'b0;
	else			ACT_T_2D <= ACT_T_1D;
end


//R_ADDRESS_CNT
always @ (posedge MTCK or negedge RSTN) begin
	if(!RSTN)			R_ADDRESS_CNT <= 9'b0;
	else if(ACT_T)		R_ADDRESS_CNT <= R_ADDRESS_CNT + 9'b1;
	else				R_ADDRESS_CNT <= 9'b0;
end  	


//oMIPI_TX0_DATA
always @ (posedge MTCK or negedge RSTN) begin
	if(!RSTN)			oMIPI_TX0_DATA <= 64'b0;
	else if(ACT_T_1D)	oMIPI_TX0_DATA <= DATA_READ;
end

//oMIPI_TX0_VALID
always @ (posedge MTCK or negedge RSTN) begin
	if(!RSTN) 			oMIPI_TX0_VALID <= 1'b0;
	else if(MTX_ON)		oMIPI_TX0_VALID <= ACT_T_2D;
	else				oMIPI_TX0_VALID <= 1'b0;
end

wire HSYNC_RANGE = (MTX_HSP - HSYNC_WING <= R_HCNT) & 
					(R_HCNT < MTX_HSP + MTX_HW + HSYNC_WING) &
					ACT_V;
wire VSYNC_RANGE = (MTX_VSP - VSYNC_WING<= R_VCNT) & 
					(R_VCNT < MTX_VSP + MTX_VW + VSYNC_WING);
                                       
//oMIPI_TX0_HSYNC
always @ (posedge MTCK or negedge RSTN) begin
	if(!RSTN) 			oMIPI_TX0_HSYNC <= 1'b0;
	else if(MTX_ON)		oMIPI_TX0_HSYNC <= HSYNC_RANGE;
	else				oMIPI_TX0_HSYNC <= 1'b0;
end

//oMIPI_TX0_VSYNC
always @ (posedge MTCK or negedge RSTN) begin
	if(!RSTN) 			oMIPI_TX0_VSYNC <= 1'b0;
	else if(MTX_ON)		oMIPI_TX0_VSYNC <= VSYNC_RANGE;
	else				oMIPI_TX0_VSYNC <= 1'b0;
end


























// always @ (posedge MTCK or negedge RSTN) begin
// 	if(!RSTN) begin

// 	end else begin
		
// 	end
// end
endmodule