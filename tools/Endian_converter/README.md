# model_endian_converters

This utility converts (byte-swaps) "tensor_content" field of the protobuf from LE to BE or vice versa.

Usage : python pb_endian_convert_utility.py -i <protobuf> {-o <outfile> -v} \
	- -i <protobuf> : Input Protobuf file to be converted. \
	- -o <outfile> : Optional output converted protobuf file. If not specified, creates a file named rewritten_saved_model.pb in the CWD. \
	- -v : Verbose 

