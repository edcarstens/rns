`ifndef DECODER_DEFINED
`define DECODER_DEFINED

module decoder #(parameter SZY=8, parameter SZX=3) (
	    output logic [SZY-1:0] y,
	     input logic [SZX-1:0] x
						    );
   always_comb begin
      y = 1 << x;
   end

endmodule // decoder

`endif //  `ifndef DECODER_DEFINED
