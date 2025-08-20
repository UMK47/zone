module Sync_top(
    input   wire        PCK,
    input   wire        RSTN,
    input   wire        MRX_FLAG_RE,
    input   [14:0]      MAD,
    input   [31:0]      MDI,
    input   [31:0]      MBE,
    input               MWE,
    input               MCK,    
    input   [9:0]       DI,
    output  [31:0]      MDO_SYNC_TOP,
    output  reg         HLOCK,
    output  reg         VLOCK,
    output  reg         SYNC_ACT,
    output  reg[9:0]    SYNC_DO
);

//{{ENX_WREG_BEGIN
	`m11_SYNC_HSP
	`m11_SYNC_VSP
	`m12_SYNC_HTW
	`m11_SYNC_VTW
	`m11_SYNC_HW
	`m11_SYNC_VW
    `m3_CH
    `m1_SYNC_UP
    `m12_DOT_H
    `m12_DOT_V
    `m12_DOT_W

	
	`wSYNC_TOP
//}}ENX_WREG_END

    assign  MDO_SYNC_TOP = W_SYNC_TOP;
// parameter SYNC_HSP = 4'd10;
// parameter SYNC_VSP = 4'd10;

// parameter SYNC_HTW = 12'd2200;
// parameter SYNC_VTW = 11'd1125;

// parameter SYNC_HW = 11'd1920;
// parameter SYNC_VW = 11'd1080;

reg [11:0] HCNT; //0~2199 4096개
reg [10:0] VCNT; //0~1124 2048개

wire ACT_H = (SYNC_HSP <= HCNT) & (HCNT < SYNC_HSP + SYNC_HW);
wire ACT_V = (SYNC_VSP <= VCNT) & (VCNT < SYNC_VSP + SYNC_VW);
wire ACT_T = ACT_H & ACT_V;

reg         SYNC_ON;
always @(posedge PCK or negedge RSTN) begin
    if(!RSTN)           SYNC_ON <= 1'd0;
    else if(aSYNC_UP)   SYNC_ON <= 1'd1;
    else if(MRX_FLAG_RE)   SYNC_ON <= 1'd0;
    //else                SYNC_ON <= SYNC_ON;
end

wire CNT_RST = SYNC_ON&MRX_FLAG_RE;

//HCNT
always @ (posedge PCK or negedge RSTN) begin
    if(!RSTN)
        HCNT <= 12'b0;
    else
        if(HLOCK | CNT_RST) HCNT <= 12'b0;
        else                HCNT <= HCNT + 12'b1;
end

//VCNT
always @ (posedge PCK or negedge RSTN) begin
    if(!RSTN)           VCNT <= 11'b0;
    else if(CNT_RST)    VCNT <= 11'b0;
    else if(HLOCK) begin
        if(VLOCK)       VCNT <= 11'b0;
        else            VCNT <= VCNT + 11'b1;
    end
end

//HLOCK
always @ (posedge PCK or negedge RSTN) begin
    if(!RSTN)
        HLOCK <= 1'b0;
    else begin
        if(HCNT == SYNC_HTW - 2'd2)
            HLOCK <= 1'b1;
        else
            HLOCK <= 1'b0;
    end
end

wire VLOCK_CON = (VCNT == SYNC_VTW -1)&(HCNT == SYNC_HTW -2);
//VLOCK
always @ (posedge PCK or negedge RSTN) begin
    if(!RSTN)
        VLOCK <= 1'b0;
    else begin
        if(VLOCK_CON)
            VLOCK <= 1'b1;
        else
            VLOCK <= 1'b0;
    end 
end

//SYNC_ACT 
always @ (posedge PCK or negedge RSTN) begin
    if(!RSTN)
        SYNC_ACT <= 1'b0;
    else 
        SYNC_ACT <= ACT_T;
end




//MOVING_H
reg [11:0] MOVING_H;
reg TURN_H;
wire [5:0] PIXEL_W = 6'd20;
wire [11:0] PIXEL_SPEED = 11'd15;

always @ (posedge PCK or negedge RSTN) begin
    if(!RSTN) begin
        MOVING_H <= SYNC_HSP;
        TURN_H <= 1'b1;
    end else if(VLOCK) begin
        if(MOVING_H >= SYNC_HSP + SYNC_HW - 1'b1- PIXEL_W)
            TURN_H <= 1'b0;
        else if(MOVING_H <= SYNC_HSP + PIXEL_W)
            TURN_H <= 1'b1;
        else
            TURN_H <= TURN_H;
        MOVING_H <= TURN_H ? (MOVING_H + PIXEL_SPEED) : (MOVING_H - PIXEL_SPEED);
    end else MOVING_H <= MOVING_H;
end

//MOVING_V
reg [11:0] MOVING_V;
reg TURN_V;
always @(posedge PCK or negedge RSTN) begin
    if(!RSTN) begin
        MOVING_V <= SYNC_VSP;
        TURN_V <= 1'b1;
    end else if(VLOCK) begin
        if(MOVING_V >= SYNC_VSP + SYNC_VW - 1'b1 - PIXEL_W)
            TURN_V <= 1'b0;
        else if(MOVING_V <= SYNC_VSP + PIXEL_W)
            TURN_V <= 1'b1;
        else
            TURN_V <= TURN_V;
        MOVING_V <= TURN_V ? (MOVING_V + PIXEL_SPEED) : (MOVING_V - PIXEL_SPEED);
    end else MOVING_V <= MOVING_V;
end

wire [7:0] PIXEL = (((MOVING_V - PIXEL_W <= VCNT)&
                (VCNT <= MOVING_V + PIXEL_W))&
                ((MOVING_H - PIXEL_W < HCNT)&
                (HCNT < MOVING_H + PIXEL_W))
                )?
                8'b11111111:8'b0;


//DOT
wire [7:0] DOT = (((DOT_V - DOT_W <= VCNT)&
                (VCNT <= DOT_V + DOT_W))&
                ((DOT_H - DOT_W < HCNT)&
                (HCNT < DOT_H + DOT_W))
                )?
                8'b11111111:8'b0;

//SYNC_DO
always @ (posedge PCK or negedge RSTN) begin
    if(!RSTN)
        SYNC_DO <= 10'b0;
    else begin
        if(ACT_T)
            case(CH)
                3'd0:
                    SYNC_DO <= {DI};
                3'd1:
                    SYNC_DO <= {PIXEL,2'b0};
                3'd2:
                    SYNC_DO <= {HCNT[7:0],2'b0};
                3'd3:
                    SYNC_DO <= {VCNT[7:0],2'b0};
                3'd4:
                    SYNC_DO <= {HCNT[7:0]^VCNT[7:0],2'b0};
                3'd5:
                    SYNC_DO <= {DI[7:0], 2'b0};
                4'd6:
                    SYNC_DO <= {DOT};
                default:
                    SYNC_DO <= {DI};
            endcase
        else
            SYNC_DO <= 10'b0;
    end
end
  

// always @ (posedge PCK or negedge RSTN) begin
//     if(!RSTN)
//         SYNC_DO <= 10'b0;
//     else begin
//         // if(((SYNC_HSP <= HCNT) & (HCNT < SYNC_HSP + SYNC_HW/2)
//         // )&ACT_T)
//         if(ACT_T)
//             SYNC_DO <= {HCNT[7:0],2'b0};
//         else
//             SYNC_DO <= 10'b0;
//     end
// end
endmodule