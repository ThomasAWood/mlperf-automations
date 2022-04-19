﻿# Collective Mind artifact

import os

from cmind import utils

class Artifact:
    ############################################################
    def __init__(self, cmind, path):
        """
        Initialize artifact class
        """

        self.cmind = cmind

        self.cfg = cmind.cfg

        self.path = path

        self.original_meta = {} # without inheritance
        self.meta = {}          # with inheritance

    ############################################################
    def load(self, ignore_inheritance = False, base_recursion = 0):
        """
        Load artifact

        """

        import copy
        
        path_artifact_meta = os.path.join(self.path, self.cfg['file_cmeta'])

        r = utils.is_file_json_or_yaml(path_artifact_meta)
        if r['return'] >0 : return r

        if not r['is_file']:                      
            return {'return':16, 'error': 'CM artifact not found in path {}'.format(self.path)}
        
        # Search if there is a repo in this path
        r = utils.load_yaml_and_json(file_name_without_ext = path_artifact_meta)
        if r['return'] >0: return r

        original_meta = r['meta']
        self.original_meta = copy.deepcopy(original_meta)

        meta = original_meta

        if not ignore_inheritance:
            automation_uid = meta.get('automation_uid', '')
            automation_alias = meta.get('automation_alias', '')
            automation = automation_alias
            if automation_uid!='': automation+=','+automation_uid

            # Check inheritance
            r = utils.process_meta_for_inheritance({'automation':automation, 
                                                    'meta':meta, 
                                                    'cmind':self.cmind, 
                                                    'base_recursion':base_recursion})
            if r['return']>0: return r

            meta = r['meta']

        self.meta = meta

        return {'return':0}

    ############################################################
    def update(self, meta, append_lists = True):
        """
        Update artifact

        """

        from cmind import utils
        
        # Without inheritance
        current_meta = self.original_meta

        if len(meta)>0:
        
            r = utils.merge_dicts({'dict1':current_meta, 'dict2':meta, 'append_lists':append_lists})
            if r['return'] >0: return 

            self.original_meta = r['dict1']

        # Save file with orignal meta without inheritance
        
        # Updates are always in JSON (on top of YAML if needed or only JSON)
        path_artifact_meta_json = os.path.join(self.path, self.cfg['file_cmeta'] + '.json')

        r = utils.save_json(file_name = path_artifact_meta_json, meta=self.original_meta)
        if r['return'] >0: return r

        # Reload with inheritance
        r = self.load()

        return r
