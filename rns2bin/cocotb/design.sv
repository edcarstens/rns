// Code your design here
`include "structs.sv"
`include "rns2bin.sv"
module top(
  output logic [18:0] y,
  input logic [7:0] x8,
  input logic [8:0] x9,
  input logic [4:0] x5,
  input logic [6:0] x7,
  input logic [10:0] x11,
  input logic [12:0] x13,
  input logic [16:0] x17,
  input logic clk,
  input logic rst
);
  rns0 x;
  rns2bin i_rns2bin(
    .y(y),
    .x(x), // rns0 struct
    .clk(clk),
    .rst(rst));
  assign x.x8 = x8;
  assign x.x9 = x9;
  assign x.x5 = x5;
  assign x.x7 = x7;
  assign x.x11 = x11;
  assign x.x13 = x13;
  assign x.x17 = x17;
  
endmodule
