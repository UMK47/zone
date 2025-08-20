module MRX_top(
	input	wire			MRCK,
	input 	wire			PCK,
	input 	wire			RSTN,
	input	wire			SYNC_VLOCK,
	output  				iMIPI_RX0_CLEAR,
	input   wire	[3:0]   iMIPI_RX0_HSYNC,					// 4Bits for Virtual Ch
	input   wire	[3:0]   iMIPI_RX0_VSYNC,					// 4Bits for Virtual Ch
	input   wire	[3:0]   iMIPI_RX0_CNT,
	input   wire			iMIPI_RX0_VALID,
	input   wire	[5:0]   iMIPI_RX0_TYPE,
	input   wire	[63:0]  iMIPI_RX0_DATA,
	input   wire	[1:0]   iMIPI_RX0_VC,
	output	reg		[9:0] 	MRX_OUT,
	output	reg				MRX_FLAG_RE,
	input   			[14:0]	MAD,
    input  				[31:0]	MDI,
    input  				[31:0]	MBE,
    input  						MWE,
    input   					MCK,
    output   			[31:0]	MDO_MRX_TOP
);



// {{ENX_WREG_BEGIN
	`m12_MRX_WR_HW
	`m12_MRX_R_HTW
	`m12_MRX_R_VTW
	`m12_MRX_R_HW 
	`m12_MRX_R_VW 
	`m12_MRX_R_HSP
	`m12_MRX_R_VSP

	`wMRX_TOP
//}}ENX_WREG_END
assign  MDO_MRX_TOP = W_MRX_TOP;


// parameter MRX_WR_HW = 480;

// parameter MRX_R_HTW = 2200;
// parameter MRX_R_VTW = 1125;
// parameter MRX_R_HW = 1920;
// parameter MRX_R_VW = 1080;
// parameter MRX_R_HSP = 10;
// parameter MRX_R_VSP = ;

wire [63:0] READ_DATA;
reg [8:0] 	WR_ADDRESS_CNT;


reg FLAG_MRCK;
reg FLAG_PCK1;
reg FLAG_PCK2;
reg FLAG_PCK3;
reg [11:0] HCNT;
reg [10:0] VCNT;
wire ACT_H = (MRX_R_HSP <= HCNT)&(HCNT <= MRX_R_HSP + MRX_R_HW - 1'd1);
wire ACT_V = (MRX_R_VSP <= VCNT)&(VCNT <= MRX_R_VSP + MRX_R_VW - 1'd1);
wire ACT_T = ACT_H & ACT_V;

reg MRX_VLOCK;
reg MRX_VALID;

reg ACT_T_1D;
reg ACT_T_2D;

reg [10:0] T_CNT;
reg [10:0] T_CNT_1D;
wire [1:0] OUT_CNT = T_CNT_1D[1:0];
wire [8:0] R_ADDRESS_CNT = T_CNT[10:2];


tpsram 
#(
    .WordWidth	(64),
    .WordDepth	(480)
)
u1
(
	.QA(READ_DATA),
  	.CLKA(PCK),
  	.CLKB(MRCK),
  	.CENA(~ACT_T),
  	.CENB(~iMIPI_RX0_VALID),
  	.AA(R_ADDRESS_CNT),
  	.AB(WR_ADDRESS_CNT),
  	.DB(iMIPI_RX0_DATA)
);

reg HSYNC_1D;
wire HSYNC_NE = ~iMIPI_RX0_HSYNC & HSYNC_1D;
wire WR_ADDRESS_CNT_RST = HSYNC_NE;

//HSYNC_1D
always @(posedge MRCK or negedge RSTN) begin
	if(!RSTN)
		HSYNC_1D <= 1'd0;
	else
		HSYNC_1D <= iMIPI_RX0_HSYNC;	
end

//WR_ADDRESS_CNT;
always @ (posedge MRCK or negedge RSTN) begin
	if(!RSTN | WR_ADDRESS_CNT_RST) 
		WR_ADDRESS_CNT <= 1'b0;
	else if(iMIPI_RX0_VALID)
			WR_ADDRESS_CNT <= WR_ADDRESS_CNT + 1'd1;
	else
		WR_ADDRESS_CNT <= WR_ADDRESS_CNT;
end


/////////////////////////////////////////////////////////////////
//////////////////////////////READ///////////////////////////////////
///////////////////////////////////////////////////////////////////

wire VLOCK_CON = (VCNT == (MRX_R_VTW - 11'd1)) & (HCNT == (MRX_R_HTW - 12'd2));
//MRX_VLOCK
always @(posedge PCK or negedge RSTN) begin
	if(!RSTN)		MRX_VLOCK <= 1'd0;
	else 			MRX_VLOCK <= VLOCK_CON;
end


wire VSYNC_FLAG_RE = FLAG_PCK2 & ~FLAG_PCK3;


//FLAG_PCK1
always @ (posedge PCK or negedge RSTN) begin
	if(!RSTN) begin
		FLAG_PCK1 <= 1'd0;
	end else begin
		FLAG_PCK1 <= iMIPI_RX0_VSYNC;
	end
end

//FLAG_PCK2
always @ (posedge PCK or negedge RSTN) begin
	if(!RSTN) begin
		FLAG_PCK2 <= 1'd0;
	end else begin
		FLAG_PCK2 <= FLAG_PCK1;
	end
end

//FLAG_PCK3
always @ (posedge PCK or negedge RSTN) begin
	if(!RSTN) begin
		FLAG_PCK3 <= 1'd0;
	end else begin
		FLAG_PCK3 <= FLAG_PCK2;
	end
end

//MRX_FLAG_RE
always @(posedge PCK or negedge RSTN) begin
	if(!RSTN)	MRX_FLAG_RE <= 1'd0;	
	else		MRX_FLAG_RE <= VSYNC_FLAG_RE;
		
end

wire HCNT_RST = SYNC_VLOCK | (HCNT == MRX_R_HTW - 12'd1);
//HCNT
always @ (posedge PCK or negedge RSTN) begin
	if(!RSTN) begin
		HCNT <= 12'd0;
	end else begin
		if(HCNT_RST)
			HCNT <= 12'd0;
		else
			HCNT <= HCNT + 12'd1;
	end
end

wire VCNT_RST = SYNC_VLOCK | MRX_VLOCK;
//VCNT
always @ (posedge PCK or negedge RSTN) begin
	if(!RSTN)
		VCNT <= 11'd0;
	else if(VCNT_RST)
		VCNT <= 11'd0;
	else if(HCNT == MRX_R_HTW - 12'd1)
		VCNT <= VCNT + 11'd1;
	else
		VCNT <= VCNT;
end

//ACT_T_1D
always @ (posedge PCK or negedge RSTN) begin
	if(!RSTN) begin
		ACT_T_1D <= 1'd0;	
	end else begin
		ACT_T_1D <= ACT_T;
	end
end

//ACT_T_2D
always @ (posedge PCK or negedge RSTN) begin
	if(!RSTN) begin
		ACT_T_2D <= 1'd0;	
	end else begin
		ACT_T_2D <= ACT_T_1D;
	end
end


//T_CNT
always @ (posedge PCK or negedge RSTN) begin
	if(!RSTN) begin
		T_CNT <= 11'd0;
	end else if(ACT_T) begin
		T_CNT <= T_CNT + 11'd1;
	end else
		T_CNT <= 11'd0;
end


//T_CNT_1D
always @(posedge PCK or negedge RSTN) begin
	if(!RSTN)
		T_CNT_1D <= 11'd0;	
	else
		T_CNT_1D <= T_CNT;
end
 
//MRX_VALID
always @ (posedge PCK or negedge RSTN) begin
	if(!RSTN) begin
		MRX_VALID <= 1'd0;
	end else if(ACT_T_2D) begin
		MRX_VALID <= 1'd1;
	end else
		MRX_VALID <= 1'd0;
end


//MRX_OUT
always @(posedge PCK or negedge RSTN) begin
	if(!RSTN)
		MRX_OUT <= 1'd0;
	else if(ACT_T_1D) begin
		MRX_OUT <= {READ_DATA[8*(OUT_CNT+1)+:8],READ_DATA[2*OUT_CNT+:2]};
	end else
		MRX_OUT <= 1'd0;
end





endmodule