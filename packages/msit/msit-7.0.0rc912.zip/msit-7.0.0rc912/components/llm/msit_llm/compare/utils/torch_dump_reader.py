import os 
import re 
import json 

from typing import Optional
import torch 

from msit_llm.compare.utils.base_dump_reader import DumpFileReader


class TorchDumpFileReader(DumpFileReader):
    def __init__(self, cpu_path: str, json_path: str):
        self.path = cpu_path
        self.json_path = json_path 
        self.key_to_folder = self._map_keys_to_folders()

    def _filter_keys(self, key_to_fold: dict) -> dict:
        keys = list(key_to_fold.values())
        keys.sort(key=len, reverse=True)
        filtered_keys = set()
        for key in keys:
            is_contained = any(other_key.startswith(key + '.') for other_key in keys if other_key != key)
            if not is_contained:
                filtered_keys.add(key)
            
        filtered_key_to_folder = {fusion_op: key for fusion_op, key in key_to_fold.items() if key in filtered_keys}

        return filtered_key_to_folder
    
    def _map_keys_to_folders(self) -> dict:
        key_to_folder = {}
        key_to_id = {}
        json_path = os.path.join(self.json_path, 'op_map_updated.json')

        with open(json_path, 'r') as f:
            data = json.load(f)
            for fusion_op, details in data.items():
                id_ = details.get('id', float('inf'))
                jit_node = details.get('jit_node', '')
                if jit_node:
                    key = self._extract_key_from_jit_node(jit_node)
                    if key is not None:
                        key_to_folder[fusion_op] = key
                        key_to_id[key] = id_

        key_to_folder = self._filter_keys(key_to_folder)
        self.key_to_id = key_to_id

        return key_to_folder
    
    def _extract_key_from_jit_node(self, jit_node: str) -> Optional[str]:
        match = re.search(r'scope:.*__module\.([^#\s]+)(?=\s*#)', jit_node)
        key_none = None
        if match:
            key = match.group(1)
            return key 
        else:
            return key_none

    def _get_keys(self) -> set:
        return set(self.key_to_folder.keys())
    
    def get_tensor(self, key: str) -> torch.Tensor:
        cpu_tensor = None 
        folder_name = self.key_to_folder[key]
        key_with_root = f'root.{folder_name}'
        folder_path = os.path.join(self.path, key_with_root)
        for file_name in os.listdir(folder_path):
            if file_name.startswith('output'):
                key_path = os.path.join(folder_path, file_name)
                cpu_tensor = torch.load(key_path)
                return cpu_tensor
            else:
                continue 

        return cpu_tensor
    