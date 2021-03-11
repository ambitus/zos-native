#! /usr/bin/env python
# Copyright 2020 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""
This utility converts (byte-swaps) "tensor_content" field of the protobuf from LE to BE and vice versa.
Usage : python pb_endian_convert_utility.py -i <protobuf> -o <outfile>
"""

import tensorflow as tf
from tensorflow.core.framework.node_def_pb2 import NodeDef
from tensorflow.python.framework import tensor_util
from collections.abc import Iterable
from argparse import ArgumentParser
import logging
import shutil

def walk_single_proto(proto,i):
    tc = 0
    if isinstance(proto,NodeDef):
        logging.debug(f"   {proto.name}")
        for attr_name in proto.attr:
            attr_value = proto.attr[attr_name]
            if attr_value.HasField("tensor"):
                tensor_value = attr_value.tensor
                if len(tensor_value.tensor_content) > 0:
                    ndarr = tensor_util.MakeNdarray(tensor_value)
                    logging.debug(f"       Before: {tensor_value} => {ndarr}")
                    ndarr.byteswap(inplace=True)
                    swapped_proto = tensor_util.make_tensor_proto(ndarr)
                    tensor_value.CopyFrom(swapped_proto)
                    logging.debug(f"       After: {tensor_value} => {ndarr}")
                    tc+=1

    elif hasattr(proto, "DESCRIPTOR"):
        for f in proto.DESCRIPTOR.fields:
            if f.name != "type_spec_value":
                sub = getattr(proto,f.name)

                tc+=walk_proto(sub,i+1)
    return tc

def walk_proto(proto,i=0):
    if isinstance(proto, str):
        return 0
    elif isinstance(proto, Iterable):
        tc=0
        for p in proto:
            tc+= walk_single_proto(p,i)
        return tc
    else:
        return walk_single_proto(proto,i)


def convert_endian(pb_file_name, output_file_name):
    with open(pb_file_name, "rb") as f:
        binary_data = f.read()

    saved_model_proto = saved_model_pb2.SavedModel.FromString(binary_data)

    tc_count = walk_proto(saved_model_proto)

    logging.debug(f"{tc_count} tensor_content entries found!")
    if tc_count == 0:
        logging.debug(f"Output file is same as input file as no tensor_content field found.")
        shutil.copyfile(pb_file_name, output_file_name)
    else:
        binary_saved_model_proto = saved_model_proto.SerializeToString()
        with open(output_file_name, "wb") as f:
            f.write(binary_saved_model_proto)

if __name__ == "__main__":
    parser = ArgumentParser(description="Protobuf Endian Convert Utility")
    parser.add_argument("-i", "--input", dest="pb_file_name", required=True,
                            help="Input protobuf file including path", metavar="FILE")
    parser.add_argument("-o", "--output", dest="rewritten_file_name", default="rewritten_saved_model.pb",
                            help="Output protobuf file including path", metavar="FILE")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                            action="store_true")
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    vers = [int(x) for x in tf.__version__.split('.')]
    if vers[0] < 2:
        logging.debug(f"Tensorflow 2.x is needed for this tool!!!")
        exit(1)
    if vers[1] < 2:
        from tensorflow_core.core.protobuf import saved_model_pb2
    else:
        from tensorflow.core.protobuf import saved_model_pb2

    convert_endian(args.pb_file_name, args.rewritten_file_name)
