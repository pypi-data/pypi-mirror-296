import os 
import re 
import json 

import torch 

from msit_llm.compare.utils.base_dump_reader import DumpFileReader
from msit_llm.compare.torchair_acc_cmp import parse_torchair_dump_data, set_msaccucmp_path_from_cann
from components.utils.file_open_check import ms_open

IS_MSACCUCMP_PATH_SET = False
GLOBAL_TENSOR_CONVERTER = None


class GEDumpFileReader(DumpFileReader):
    def __init__(self, npu_path: str, json_path: str):
        self.path = npu_path
        self.json_path = json_path 
        self.process_json_files()
        self.key_to_folder = self._map_keys_to_folders()

    def process_json_files(self):
        with open(os.path.join(self.json_path, 'mindie_torch_op_mapping.json')) as f:
            torch_op_map = json.load(f)
        
        rt_jit_map = {item["rt_layer"]: item["jit_node"] for item in torch_op_map}

        with open(os.path.join(self.json_path, 'mindie_rt_op_mapping.json')) as f:
            op_map = json.load(f)
        
        op_map = sorted(op_map, key=lambda x: x["id"])

        cur_fuseop = ""
        id_ = 1
        new_op_map = {}

        for item in op_map:
            ge_op = item.get("ge_op")
            rt_layer = item.get("rt_layer")
            jit_node = rt_jit_map.get(rt_layer, None)
            fusion_op = item.get("fusion_op", ge_op)

            if cur_fuseop != fusion_op:
                if cur_fuseop in new_op_map:
                    new_op_map[cur_fuseop]["fuse_path"] = fuse_path 
                
                new_op_map[fusion_op] = {
                    "id": id_,
                    "jit_node": jit_node,
                    "fuse_path": [{"ge_op": ge_op, "jit_node": jit_node}]
                }
                id_ += 1 
                fuse_path = [{"ge_op": ge_op, "jit_node": jit_node}]
            else:
                new_op_map[fusion_op]["jit_node"] = jit_node 
                fuse_path.append({"ge_op": ge_op, "jit_node":jit_node})

            cur_fuseop = fusion_op

        if cur_fuseop in new_op_map:
            new_op_map[cur_fuseop]["fuse_path"] = fuse_path

        with ms_open(os.path.join(self.json_path, 'op_map_updated.json'), mode="w") as f:
            json.dump(new_op_map, f, indent=4)
        
    def _map_keys_to_folders(self) -> dict:
        key_to_folder = {}
        json_path = os.path.join(self.json_path, 'op_map_updated.json')

        with open(json_path, 'r') as f:
            data = json.load(f)
            for fusion_op, details in data.items():
                jit_node = details.get('jit_node', '')
                if jit_node:
                    key_to_folder[fusion_op] = jit_node 
        
        return key_to_folder

    def _get_keys(self) -> set:
        return set(self.key_to_folder.keys())

    def get_tensor(self, key: str) -> torch.Tensor:
        folder_name = key
        folder_path = self.path 
        files = os.listdir(folder_path)
        pattern = re.compile(rf'{re.escape(folder_name)}\.\d')
        matching_files = [file for file in files if pattern.search(file)]
        tensor_file_path = os.path.join(folder_path, matching_files[0])
        bin_dump_data = parse_torchair_dump_data(tensor_file_path)
        npu_tensor = bin_dump_data[1][0]
        
        return npu_tensor