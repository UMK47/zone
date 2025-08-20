//*****************************************************************************
//  File Name           : iic_if.v
//  Description         :
//  Date                : 2022.07.15
//  Created by          : HJ Jung
//  Revision History    :
//      1.  2012.06.08  : Created by HJ Jung
//      2.  2022.07.15  : Modified MAD 16bit, MDI 32bit (fix)
//*****************************************************************************


module		iic_if
(
	input			RSTN,
	input			MCK,

	input			iSCL,
	input			iSDA,
	output	reg		SDO,				// SDA Output 0 : Write(0), 1 : Read(Pull up)
	input	[ 6:0]	SLAVE,				// Slave Address

	input	[ 3:0]	SDO_MARGIN,			// SDO Delay(MCK)
	output	[ 5:0]	TEST_OUT,
	// output	[ 7:0]	TEST_OUT1,
	output	reg		SLAVE_EN,

	// output			SCL,
	// output			SDA,

	input	[31:0]	MDO,
	output	[15:0]	MAD,
	output	[31:0]	MDI,
	output	[31:0]	MBE,
	output			MWE,
	output			MRE

);

	reg				SCL;
	always @(posedge MCK or negedge RSTN) begin
		if(!RSTN)			SCL <= 1'd1;
		else				SCL <= iSCL;
	end

	reg				SDA;
	always @(posedge MCK or negedge RSTN) begin
		if(!RSTN)			SDA <= 1'd0;
		else				SDA <= iSDA;
	end




//=====================================================================================================
//	START
//=====================================================================================================

//-----------------------------------------------------------------------------------------------------
//	Start


	reg				SP_T1;
	always @(negedge SDA or negedge RSTN) begin
		if(!RSTN)		SP_T1 <= 1'd0;
		else if(SCL)	SP_T1 <= 1'd1;
		else			SP_T1 <= 1'd0;
	end

	reg				SP_T2;
	always @(posedge SCL or negedge RSTN) begin
		if(!RSTN)		SP_T2 <= 1'd0;
		else			SP_T2 <= SP_T1;
	end

	wire			SP = SP_T1 & ~SP_T2;

//-----------------------------------------------------------------------------------------------------
//	End

	reg				EP;
	always @(posedge SDA or negedge RSTN) begin
		if(!RSTN)		EP <= 1'd1;
		else if(SCL)	EP <= 1'd1;
		else			EP <= 1'd0;
	end

//-----------------------------------------------------------------------------------------------------
//	i2c Enable

	wire			SDA_EN = ~EP | SP_T1;

//-----------------------------------------------------------------------------------------------------
//	Counter

	reg		[ 3:0]	SDA_CNT;			// 0D from SDA @ SCL
	wire			SDA_CNT_RS = SDA_CNT == 4'h8;
	always @(posedge SCL or negedge RSTN) begin
		if(!RSTN)			SDA_CNT <= 4'h0;
		else if(SP)			SDA_CNT <= 4'h0;
		else if(SDA_EN)		begin
			if(SDA_CNT_RS)	SDA_CNT <= 4'h0;
			else			SDA_CNT <= SDA_CNT + 4'h1;
		end
		else 				SDA_CNT <= 4'h0;
	end
	wire			SDA_CNTE = SDA_CNT == 4'd7;

	reg		[ 2:0]	DCNT;				// 0D from SDA @ SCL
	wire			DCNT_INC = SDA_CNT_RS & (~&DCNT);
	always @(posedge SCL or negedge RSTN) begin
		if(!RSTN)			DCNT <= 3'd0;
		else if(SP)			DCNT <= 3'd0;
		else if(DCNT_INC)	DCNT <= DCNT + 3'd1;
	end

//=====================================================================================================
//	Input Data
//=====================================================================================================

	reg		[ 7:0]	SDA_SFT;			// 7D from SDA @ SCL
	always @(posedge SCL or negedge RSTN) begin
		if(!RSTN)			SDA_SFT <= 8'hFF;
		else if(~SDA_CNTE)	SDA_SFT <= {SDA_SFT[6:0], SDA};
	end

//-----------------------------------------------------------------------------------------------------
//	Address

	wire			ID_OK_T = SDA_SFT[7:1] == SLAVE;
	reg				ID_OK_T2;				// 8D from SDA @ SCL
	wire			SDA_SFT1_CT = SDA_CNTE & (DCNT == 3'd0);
	always @(posedge SCL or negedge RSTN) begin
		if(!RSTN)			ID_OK_T2 <= 1'd0;
		else if(SDA_SFT1_CT)ID_OK_T2 <= ID_OK_T;
		else if(SP)			ID_OK_T2 <= 1'd0;
	end
	wire			ID_OK = ID_OK_T2 | (SDA_SFT1_CT&ID_OK_T);	// 7D from SDA @ SCL

	reg				RW;					// 8D from SDA @ SCL
	wire			RW_END = RW & SDA_CNTE & SDA;
	always @(posedge SCL or negedge RSTN) begin
		if(!RSTN)			RW <= 1'd0;
		else if(SDA_SFT1_CT)RW <= SDA_SFT[0];
		else if(RW_END)		RW <= 1'd0;
	end

	reg				RW_1D;				// 9D from SDA @ SCL
	always @(posedge SCL or negedge RSTN) begin
		if(!RSTN)			RW_1D <= 1'd0;
		else 				RW_1D <= RW;
	end

	reg		[15:0]	SDA_SFT2;			// 8D from SDA @ SCL
	wire			ADDR_EN = (DCNT == 3'd1) | (DCNT == 3'd2);
	wire			SDA_SFT2_CT = SDA_CNTE & ADDR_EN;
	always @(posedge SCL or negedge RSTN) begin
		if(!RSTN)			SDA_SFT2 <= 16'd0;
		else if(SDA_SFT2_CT)SDA_SFT2 <= {SDA_SFT2[7:0],SDA_SFT};
	end

	wire	[15:0]	MAD_T = SDA_SFT2;
//-----------------------------------------------------------------------------------------------------
//	Write Data

	reg		[31:0]	SDA_SFT3;			// 8D from SDA @ SCL
	wire			DATA_EN = DCNT >= 3'd3;
	wire			SDA_SFT3_CT = SDA_CNTE & DATA_EN & (~RW);
	always @(posedge SCL or negedge RSTN) begin
		if(!RSTN)			SDA_SFT3 <= 32'd0;
		else if(~SDA_EN)	SDA_SFT3 <= 32'hFFFFFFFF;
		else if(SDA_SFT3_CT)SDA_SFT3 <= {SDA_SFT, SDA_SFT3[31:8]};
	end

	wire	[31:0]	MDI_T = {32{~RW}} & SDA_SFT3;


//=====================================================================================================
//	BUS OUT
//=====================================================================================================

//-----------------------------------------------------------------------------------------------------
//	Write Enable

	wire			WEN_T1 = DCNT == 3'd6;
	wire			WEN_T2 = SDA_CNT_RS & ~RW_1D & ID_OK;
	wire			WEN = WEN_T1 & WEN_T2;

	reg		[ 3:0]	MWE_T1;				// 1~4D from SDA_CNT_RS @ MCK
	always @(posedge MCK or negedge RSTN) begin
		if(!RSTN)			MWE_T1 <= 4'd0;
		else if(WEN)		MWE_T1 <= {MWE_T1[2:0], 1'd1};
		else if(EP)			MWE_T1 <= {MWE_T1[2:0], 1'd0};
	end

	wire			MWE_T = ~MWE_T1[2] & MWE_T1[3];

	reg				MWE8;				// 4D from SDA_CNT_RS @ MCK
	always @(posedge MCK or negedge RSTN) begin
		if(!RSTN)			MWE8 <= 1'd0;
		else				MWE8 <= MWE_T;
	end

//-----------------------------------------------------------------------------------------------------
//	Read Enable

	wire			MRE_T0 = (DCNT >= 2'd1) & RW_1D & ID_OK;
	wire			MRE_T1 = SDA_CNT_RS & MRE_T0;

	reg		[ 5:0]	MRE_T2;				// 1~4D from SDA_CNT_RS @ MCK
	always @(posedge MCK or negedge RSTN) begin
		if(!RSTN)			MRE_T2 <= 6'd0;
		else 				MRE_T2 <= {MRE_T2[4:0], MRE_T1};
	end

	wire			MRE_T = MRE_T2[4] & ~MRE_T2[5];

	wire			MREN_T0 = (DCNT == 2'd0) & RW & ID_OK;
	wire			MREN_T1 = SDA_CNT_RS & MREN_T0;
	reg		[ 3:0]	MREN_T2;				// 1~4D from SDA_CNT_RS @ MCK
	always @(posedge MCK or negedge RSTN) begin
		if(!RSTN)			MREN_T2 <= 4'd0;
		else 				MREN_T2 <= {MREN_T2[2:0], MREN_T1};
	end

	wire			MREN_T = MREN_T2[2] & ~MREN_T2[3];



//-----------------------------------------------------------------------------------------------------
//	Address

//	Address Catch
	wire			ADEN_T = DCNT == 2'd2;
	wire			ADEN = ADEN_T & SDA_CNT_RS & ID_OK & ~RW_1D;

	reg		[ 3:0]	ADE_T1;				// 1~4D from SDA_CNT_RS @ MCK
	always @(posedge MCK or negedge RSTN) begin
		if(!RSTN)			ADE_T1 <= 4'd0;
		else 				ADE_T1 <= {ADE_T1[2:0], ADEN};
	end
	wire			ADE = ADE_T1[2] & ~ADE_T1[3];

	reg				MRE8;				// 4D from SDA_CNT_RS @ MCK
	always @(posedge MCK or negedge RSTN) begin
		if(!RSTN)			MRE8 <= 1'd0;
		else				MRE8 <= (MREN_T) & RW ;
	end


	reg		[15:0]	MAD16;				// 4D from SDA_CNT_RS @ MCK
	always @(posedge MCK or negedge RSTN) begin
		if(!RSTN)			MAD16 <= 16'd0;
		else if(ADE)		MAD16 <= MAD_T;
	end

//-----------------------------------------------------------------------------------------------------
//	Write data

	reg		[31:0]	MDI32;				// 4D from SDA_CNT_RS @ MCK
	always @(posedge MCK or negedge RSTN) begin
		if(!RSTN)			MDI32 <= 32'd0;
		else if(MWE_T)		MDI32 <= MDI_T;
	end



// MICOM signal gen.----------------------------------------------------------------------------------------------------




	reg		[15:0]	MAD16_1D;
	reg		[31:0]	MDI32_1D;

	reg				MWE_TMP;
	always@(posedge MCK or negedge RSTN) begin
		if(!RSTN)	 	MWE_TMP <= 1'h0;
		else			MWE_TMP <= MWE8;
	end
	reg				MRE_TMP;
	always@(posedge MCK or negedge RSTN) begin
		if(!RSTN)	 	MRE_TMP <= 1'h0;
		else			MRE_TMP <= MRE8;
	end



	always@(posedge MCK or negedge RSTN) begin
		if(!RSTN)	 			MAD16_1D <= 16'hFFff;
		else if(MWE8 | MRE8)	MAD16_1D <= MAD16;
	end


	always@(posedge MCK or negedge RSTN) begin
		if(!RSTN)	 			MDI32_1D <= 32'hFFFFFFff;
		else if(MWE8 | MRE8)	MDI32_1D <= MDI32;
	end


	assign			MAD = 	MAD16_1D;
	assign			MDI = 	MDI32_1D;
	assign			MBE = 	{32{MWE_TMP}};
	assign			MWE = 	MWE_TMP;
	assign			MRE = 	MRE_TMP;


//=====================================================================================================
//	Output Data
//=====================================================================================================

//-----------------------------------------------------------------------------------------------------
//	Read Data

	reg		[31:0]	MDO32;
	always @(posedge MCK or negedge RSTN) begin
		if(!RSTN)			MDO32 <= 32'd0;
		else if(MRE)		MDO32 <= MDO;
		else if(MRE_T)		MDO32 <= {8'd0,MDO32[31:8]};
	end

	wire	[ 7:0]	MDO8 = MDO32[7:0];



	reg		[ 7:0]	SDO_SFT;			// 0D from SDA @ SCL
	// wire			RW_ID = RW & ID_OK;
	wire			REN_T = RW & (~SDA_CNTE);
	wire			REN = ID_OK & REN_T;
	always @(negedge SCL or negedge RSTN) begin
		if(!RSTN)			SDO_SFT <= 8'hFF;
		else if(SDA_CNT_RS)	SDO_SFT <= MDO8;
		else if(REN)		SDO_SFT <= {SDO_SFT[6:0], 1'd1};
	end

//-----------------------------------------------------------------------------------------------------
//	Ack

	wire			ACK_T1 = (~RW) & SDA_EN & SDA_CNTE;
	wire			ACK_T2 = ACK_T1 & ID_OK;
	reg				ACK;
	always @(negedge SCL or negedge RSTN) begin
		if(!RSTN)			ACK <= 1'd0;
		else 				ACK <= ACK_T2;
	end

//-----------------------------------------------------------------------------------------------------
//	SDO

	reg				REN_NT;
	always @(negedge SCL or negedge RSTN) begin
		if(!RSTN)			REN_NT <= 1'd0;
		else 				REN_NT <= REN;
	end
	wire			REN_N = REN_NT & ~EP;

	wire			SDO_T = SDO_SFT[7];
	wire			SDO_T2 = 	REN_N ? SDO_T :
								ACK ? 1'd0 : 1'd1;
	reg		[17:0]	SDO_D;
	always @(posedge MCK or negedge RSTN) begin
		if(!RSTN)			SDO_D <= 18'h3FFFF;
		else 				SDO_D <= {SDO_D[16:0],SDO_T2};
	end

	wire			SDO_DT = 	(SDO_MARGIN == 4'h0) ? SDO_D[2]  :
								(SDO_MARGIN == 4'h1) ? SDO_D[3]  :
								(SDO_MARGIN == 4'h2) ? SDO_D[4]  :
								(SDO_MARGIN == 4'h3) ? SDO_D[5]  :
								(SDO_MARGIN == 4'h4) ? SDO_D[6]  :
								(SDO_MARGIN == 4'h5) ? SDO_D[7]  :
								(SDO_MARGIN == 4'h6) ? SDO_D[8]  :
								(SDO_MARGIN == 4'h7) ? SDO_D[9]  :
								(SDO_MARGIN == 4'h8) ? SDO_D[10] :
								(SDO_MARGIN == 4'h9) ? SDO_D[11] :
								(SDO_MARGIN == 4'hA) ? SDO_D[12] :
								(SDO_MARGIN == 4'hB) ? SDO_D[13] :
								(SDO_MARGIN == 4'hC) ? SDO_D[14] :
								(SDO_MARGIN == 4'hD) ? SDO_D[15] :
								(SDO_MARGIN == 4'hE) ? SDO_D[16] : SDO_D[17];

	// reg				SDO;
	always @(posedge MCK or negedge RSTN) begin
		if(!RSTN)			SDO <= 1'd1;
		else 				SDO <= SDO_DT;
	end

	// reg				SLAVE_EN;
	always @(negedge SCL or negedge RSTN) begin
		if(!RSTN)			SLAVE_EN <= 1'd0;
		else 				SLAVE_EN <= (REN_T|ACK_T1)&(~ID_OK);
	end

//-----------------------------------------------------------------------------------------------------
//	TEST OUT

    reg		[15:0]  TEST_CNT;
    always@(posedge MCK or negedge RSTN)begin
        if(!RSTN)   TEST_CNT <= 16'd0;
        else        TEST_CNT <= TEST_CNT + 16'd1;
    end

    // assign          TEST_GPIO = TEST_CNT[15];


	reg				SCL_D;
	always @(posedge MCK or negedge RSTN) begin
		if(!RSTN)			SCL_D <= 1'd1;
		else				SCL_D <= SCL;
	end

	reg				SDA_D;
	always @(posedge MCK or negedge RSTN) begin
		if(!RSTN)			SDA_D <= 1'd0;
		else				SDA_D <= SDA;
	end




	// assign				TEST_OUT = {TEST_CNT[0],SCL_D,SDA_D,ACK,RW,ID_OK};
	assign				TEST_OUT = {SDA_CNT,SDA_SFT1_CT,ID_OK_T,SDA,iSCL,SP};
	// assign				TEST_OUT1 = SDA_SFT;

endmodule
