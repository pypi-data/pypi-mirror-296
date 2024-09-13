# Copyright (c) 2023-2024 Huawei Technologies Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

from components.utils.parser import BaseCommand
from components.debug.compare.msquickcmp.adapter_cli.args_adapter import CmpArgsAdapter
from components.debug.compare.msquickcmp.cmp_process import cmp_process
from components.debug.compare.msquickcmp.common.args_check import (
    check_model_path_legality, check_om_path_legality, check_weight_path_legality, check_input_path_legality,
    check_cann_path_legality, check_output_path_legality, check_dict_kind_string, check_device_range_valid,
    check_number_list, check_dym_range_string, check_fusion_cfg_path_legality, check_quant_json_path_legality,
    safe_string, str2bool, check_path_exit
)
from msquickcmp.common.utils import logger
from components.debug.compare.msquickcmp.dump.dump_process import dump_process
from msquickcmp.dump.args_adapter import DumpArgsAdapter

CANN_PATH = os.environ.get('ASCEND_TOOLKIT_HOME', "/usr/local/Ascend/ascend-toolkit/latest")


class CompareCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser = None

    def add_arguments(self, parser):
        parser.add_argument(
            '-gm',
            '--golden-model',
            required=False,
            dest="golden_model",
            type=check_model_path_legality,
            help='The original model (.onnx or .pb or .prototxt or .om) file path')
        parser.add_argument(
            '-om',
            '--om-model',
            required=False,
            dest="om_model",
            type=check_om_path_legality,
            help='The offline model (.om or .mindir) file path')
        parser.add_argument(
            '-w',
            '--weight',
            dest="weight_path",
            type=check_weight_path_legality,
            help='Required when framework is Caffe (.cafemodel)')
        parser.add_argument(
            '-i',
            '--input',
            default='',
            dest="input_data_path",
            type=check_input_path_legality,
            help='The input data path of the model. Separate multiple inputs with commas(,).'
                 ' E.g: input_0.bin,input_1.bin')
        parser.add_argument(
            '-c',
            '--cann-path',
            default=CANN_PATH,
            dest="cann_path",
            type=check_cann_path_legality,
            help='The CANN installation path')
        parser.add_argument(
            '-o',
            '--output',
            dest="out_path",
            default='',
            type=check_output_path_legality,
            help='The output path')
        parser.add_argument(
            '-is',
            '--input-shape',
            type=check_dict_kind_string,
            dest="input_shape",
            default='',
            help="Shape of input shape. Separate multiple nodes with semicolons(;)."
                 " E.g: \"input_name1:1,224,224,3;input_name2:3,300\"")
        parser.add_argument(
            '-d',
            '--device',
            type=check_device_range_valid,
            dest="device",
            default='0',
            help='Input device ID [0, 255].')
        parser.add_argument(
            '-outsize',
            '--output-size',
            type=check_number_list,
            dest="output_size",
            default='',
            help='The size of output. Separate multiple sizes with commas(,). E.g: 10200,34000')
        parser.add_argument(
            '-n',
            '--output-nodes',
            type=check_dict_kind_string,
            dest="output_nodes",
            default='',
            help="Output nodes designated by user. Separate multiple nodes with semicolons(;)."
                 " E.g: \"node_name1:0;node_name2:1;node_name3:0\"")
        parser.add_argument(
            '--advisor',
            action='store_true',
            dest="advisor",
            help='Enable advisor after compare.')
        parser.add_argument(
            '-dr',
            '--dym-shape-range',
            type=check_dym_range_string,
            dest="dym_shape_range",
            default='',
            help="Dynamic shape range using in dynamic model, "
                 "using this means ignore input_shape"
                 " E.g: \"input_name1:1,3,200\~224,224-230;input_name2:1,300\"")
        parser.add_argument(
            '--dump',
            dest="dump",
            default=True,
            type=str2bool,
            help="Whether to dump all the operations' ouput.")
        parser.add_argument(
            '--convert',
            dest="bin2npy",
            default=False,
            type=str2bool,
            help='Enable npu dump data conversion from bin to npy after compare.Usage: --convert True')
        parser.add_argument(
            '--locat',
            default=False,
            dest="locat",
            type=str2bool,
            help='Enable accuracy interval location when needed.E.g: --locat True')
        parser.add_argument(
            '-cp',
            '--custom-op',
            type=safe_string,
            dest="custom_op",
            default='',
            help='Op name witch is not registered in onnxruntime, only supported by Ascend')
        parser.add_argument(
            '-ofs',
            '--onnx-fusion-switch',
            dest="onnx_fusion_switch",
            default=True,
            type=str2bool,
            help='Onnxruntime fusion switch, set False for dump complete onnx data when '
                 'necessary.Usage: -ofs False')
        parser.add_argument(
            '--fusion-switch-file',
            dest="fusion_switch_file",
            type=check_fusion_cfg_path_legality,
            help='You can disable selected fusion patterns in the configuration file')
        parser.add_argument(
            "-single",
            "--single-op",
            default=False,
            dest="single_op",
            type=str2bool,
            help='Comparision mode:single operator compare.Usage: -single True')
        parser.add_argument(
            "-max",
            "--max-cmp-size",
            dest="max_cmp_size",
            default=0,
            type=int,
            help="Max size of tensor array to compare. Usage: --max-cmp-size 1024")
        parser.add_argument(
            '-q',
            '--quant-fusion-rule-file',
            type=check_quant_json_path_legality,
            dest="quant_fusion_rule_file",
            default='',
            help="the quant fusion rule file path")
        parser.add_argument(
            '--saved_model_signature',
            dest="saved_model_signature",
            default='serving_default',
            help="Enter the signature of the model")
        parser.add_argument(
            '--saved_model_tag_set',
            dest="saved_model_tag_set",
            default='',
            help="Enter the tagSet of the model. For example: --saved_model_tag_set ['serve', 'general_parser']")
        # alone compare parameters
        parser.add_argument(
            '-mp',
            '--my-path',
            required=False,
            dest="my_path",
            type=check_path_exit,
            help='The npu dump data path')
        parser.add_argument(
            '-gp',
            '--golden-path',
            required=False,
            dest="golden_path",
            type=check_path_exit,
            help='The cpu(golden) dump data path')
        parser.add_argument(
            '--ops-json',
            required=False,
            dest="ops_json",
            type=check_path_exit,
            help='The npu and cpu ops matching rule json')
        self.parser = parser

    def handle(self, args):
        if not args.golden_model and not args.golden_path:
            logger.error("The following args are required: -gm/--golden-model or -gp/--golden-path")
            self.parser.print_help()
            return
        cmp_args = CmpArgsAdapter(args.golden_model, args.om_model, args.weight_path, args.input_data_path,
                                  args.cann_path, args.out_path,
                                  args.input_shape, args.device, args.output_size, args.output_nodes, args.advisor,
                                  args.dym_shape_range,
                                  args.dump, args.bin2npy, args.custom_op, args.locat,
                                  args.onnx_fusion_switch, args.single_op, args.fusion_switch_file,
                                  args.max_cmp_size, args.quant_fusion_rule_file, args.saved_model_signature,
                                  args.saved_model_tag_set, args.my_path, args.golden_path, args.ops_json)
        cmp_process(cmp_args, True)


class DumpCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser = None

    def add_arguments(self, parser):
        parser.add_argument(
            '-m',
            '--model',
            required=True,
            dest="model_path",
            type=check_model_path_legality,
            help='The original model (.onnx or .pb or saved_model) file path')
        parser.add_argument(
            '-w',
            '--weight',
            dest="weight_path",
            type=check_weight_path_legality,
            help='Required when framework is Caffe (.cafemodel)')
        parser.add_argument(
            '-i',
            '--input',
            default='',
            dest="input_data_path",
            type=check_input_path_legality,
            help='The input data path of the model. Separate multiple inputs with commas(,).'
                 ' E.g: input_0.bin,input_1.bin')
        parser.add_argument(
            '-c',
            '--cann-path',
            default=CANN_PATH,
            dest="cann_path",
            type=check_cann_path_legality,
            help='The CANN installation path')
        parser.add_argument(
            '-o',
            '--output',
            dest="out_path",
            default='',
            type=check_output_path_legality,
            help='The output path')
        parser.add_argument(
            '-is',
            '--input-shape',
            type=check_dict_kind_string,
            dest="input_shape",
            default='',
            help="Shape of input shape. Separate multiple nodes with semicolons(;)."
                 " E.g: \"input_name1:1,224,224,3;input_name2:3,300\"")
        parser.add_argument(
            '-d',
            '--device',
            type=check_device_range_valid,
            dest="device",
            default='0',
            help='Input device ID [0, 255].')
        parser.add_argument(
            '-dr',
            '--dym-shape-range',
            type=check_dym_range_string,
            dest="dym_shape_range",
            default='',
            help="Dynamic shape range using in dynamic model, "
                 "using this means ignore input_shape"
                 " E.g: \"input_name1:1,3,200\~224,224-230;input_name2:1,300\"")
        parser.add_argument(
            '-ofs',
            '--onnx-fusion-switch',
            dest="onnx_fusion_switch",
            default=True,
            type=str2bool,
            help='Onnxruntime fusion switch, set False for dump complete onnx data when '
                 'necessary.Usage: -ofs False')
        parser.add_argument(
            '--saved_model_signature',
            dest="saved_model_signature",
            default='serving_default',
            help="Enter the signature of the model")
        parser.add_argument(
            '--saved_model_tag_set',
            dest="saved_model_tag_set",
            default='',
            help="Enter the tagSet of the model. For example: --saved_model_tag_set ['serve', 'general_parser']")
        parser.add_argument(
            '-dp',
            '--device-pattern',
            required=True,
            dest="device_pattern",
            help="Enter inference in npu or cpu device. For example: -dp cpu")
        parser.add_argument(
            '--tf-json',
            required=False,
            dest="tf_json_path",
            help="When dump saved_model, you need provide tf-ops-json file path.")
        self.parser = parser

    def handle(self, args):
        cmp_args = DumpArgsAdapter(args.model_path, args.weight_path, args.input_data_path,
                                   args.cann_path, args.out_path, args.input_shape, args.device,
                                   args.dym_shape_range, args.onnx_fusion_switch,
                                   args.saved_model_signature, args.saved_model_tag_set,
                                   args.device_pattern, args.tf_json_path)
        dump_process(cmp_args, True)


def get_compare_cmd_ins():
    help_info = "one-click network-wide accuracy analysis of golden models."
    compare_instance = CompareCommand("compare", help_info)
    return compare_instance


def get_dump_cmd_ins():
    help_info = "one-click dump model ops inputs and outputs."
    dump_instance = DumpCommand("dump", help_info)
    return dump_instance
