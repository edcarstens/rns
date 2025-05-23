`ifndef ENCODER_DEFINED
`define ENCODER_DEFINED

module encoder #(parameter SZY=3, parameter SZX=8) (
	    output logic [SZY-1:0] y,
	    input logic [SZX-1:0] x
	    );

   bit				  done;

   always_comb begin
      done = 1'b0;
      for (int i=0; i<SZX; i=i+1) begin
	 if (!done && x[i]) begin
	    y = i[SZY-1:0];
	    done = 1'b1;
	 end
      end
   end
endmodule // encoder

`endif //  `ifndef ENCODER_DEFINED
