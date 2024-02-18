﻿# Developer(s): Grigori Fursin

import cmind
import os
import misc

import streamlit.components.v1 as components

import streamlit as st

announcement = 'Under development - please get in touch via [Discord](https://discord.gg/JjWNWXKxwT) for more details ...'

initialized = False
external_module_path = ''
external_module_meta = {}

badges={
        'functional':{'url':'https://cTuning.org/images/artifacts_evaluated_functional_v1_1_small.png'},
        'reproduced':{'url':'https://cTuning.org/images/results_reproduced_v1_1_small.png'},
        'support_docker':{'url':'https://cTuning.org/images/docker_logo2_small.png'}
       }


def main():
    params = misc.get_params(st)

    # Set title
    st.title('Reproducibility studies')

    st.markdown(announcement)

    return page(st, params)




def page(st, params, action = ''):

    global initialized, external_module_path, external_module_meta

    end_html = ''


#    st.markdown('----')

    self_url = misc.make_url('', key='', action='reproduce', md=False)
    url_benchmarks = misc.make_url('', key='', action='howtorun', md=False)
    url_challenges = misc.make_url('', key='', action='challenges', md=False)

    # Some info
    x = '''
         <i>
         <small>
         This interface will help you find the <a href="{}">modular benchmarks' settings</a> 
         that <a href="{}">the community</a> have managed to successfully validate 
         across different models, data sets, software and hardware 
         based on the <a href="https://cTuning.org/ae">ACM/cTuning reproducibility methodology and badges</a> -
         please get in touch via <a href="https://discord.gg/JjWNWXKxwT">Discord</a> for more details.
         </small>
         </i>
          <br>
          <br>
        '''.format(url_benchmarks, url_challenges)

    st.write(x, unsafe_allow_html = True)
    
#    st.markdown(announcement)

    # Check if test is selected
    test_uid = ''
    x = params.get('test_uid',[''])
    if len(x)>0 and x[0]!='': test_uid = x[0].strip()


    ############################################################################################
    # Select target hardware
    compute_uid = ''
    compute_meta = {}
    compute_selection = []

    if test_uid == '':
        x = params.get('compute_uid',[''])
        if len(x)>0 and x[0]!='': compute_uid = x[0].strip()
    
    ii = {'action':'load_cfg',
          'automation':'utils',
          'tags':'benchmark,compute',
          'skip_files':False}

    if compute_uid!='':
        ii['prune']={'uid':compute_uid}

    r = cmind.access(ii)
    if r['return']>0: return r
    compute_selection = r['selection']

    if test_uid == '':
        r = misc.make_selection(st, r['selection'], 'compute', 'target hardware', compute_uid)
        if r['return']>0: return r
        compute_meta = r['meta']
        compute_uid = compute_meta.get('uid','')


    ############################################################################################
    # Select benchmark
    bench_meta = {}

    bench_name = ''
    x = params.get('bench_name',[''])
    if len(x)>0 and x[0]!='': bench_name = x[0].strip()

    if test_uid == '':
        ii = {'action':'load_cfg',
              'automation':'utils',
              'tags':'benchmark,run',
              'skip_files':True}

        if bench_name!='':
            ii['artifact']=bench_name

        r = cmind.access(ii)
        if r['return']>0: return r

        # Prune by supported compute
        selection = r['selection']
        pruned_selection = []

        if compute_uid == '':
            pruned_selection = selection
        else:
            for s in selection:
                add = True

                if compute_uid in s.get('supported_compute',[]):
                    pruned_selection.append(s)

        r = misc.make_selection(st, pruned_selection, 'benchmark', 'benchmark', bench_name)
        if r['return']>0: return r

        bench_meta = r['meta']

    ############################################################################################
    # Select tests
    if test_uid == '' and compute_uid == '' and len(bench_meta) == 0:
        st.markdown('*Please prune search by device and/or benchmark ...*')

    else:
        ii = {'action':'load_cfg',
              'automation':'utils',
              'tags':'benchmark,run',
              'key':'run-',
              'key_end':['-meta.json', '-meta.yaml'],
              'skip_files':False}

        if len(bench_meta)>0 or bench_name!='':
            if len(bench_meta)>0:
                ii['artifact']=bench_meta['uid']
            else:
                ii['artifact']=bench_name
        elif compute_uid !='' :
            ii['prune']={'meta_key':'supported_compute',
                         'meta_key_uid':compute_uid}

        if compute_uid != '':
            if 'prune' not in ii: ii['prune']={}
            ii['prune']['key'] = 'compute_uid'
            ii['prune']['key_uid'] = compute_uid

        if test_uid!='':
            if 'prune' not in ii: ii['prune']={}
            ii['prune']['uid']=test_uid

        r = cmind.access(ii)
        if r['return']>0: return r

        # Prune by supported compute
        selection = r['selection']

        if len(selection)==0:
            st.markdown('*WARNING: No tests found!*')
        else:
            if len(selection)==1:
                ###################################################################
                # Show individual test
                s = selection[0]

                full_path = s['full_path']
                test_uid = s['uid']

                st.markdown('---')
                st.markdown('**Test {}**'.format(test_uid))

                # Check badges
                x = ''

                for b in badges:
                    if s.get(b, False):
                        x += '<a href="http://cTuning.org/ae" target="_blank"><img src="{}" height="64"></a>\n'.format(badges[b]['url'])

                if x!='':
                    st.write(x, unsafe_allow_html = True)

                
                test_md = full_path[:-5]+'.md'
                if os.path.isfile(test_md):

                    r = cmind.utils.load_txt(test_md)
                    if r['return']>0: return r

                    x = r['string']

                    st.markdown('**Notes:**')
                    st.markdown(x)

                st.markdown('**Test meta (will be converted into table in the future):**')

                import json
                st.markdown("""
```json
{}
```
                            """.format(json.dumps(s, indent=2)))


            else:
                ###################################################################
                # Show tables
                
                for s in selection:
                    st.markdown('* {}'.format(s['full_path']))




















    if bench_name!='':
        self_url+='&bench_name='+bench_name
    if test_uid!='':
        self_url+='&test_uid='+test_uid    
    elif compute_uid!='':
        self_url+='&compute_uid='+compute_uid

    end_html='<center><small><i><a href="{}">Self link</a></i></small></center>'.format(self_url)

    
    return {'return': 0, 'end_html': end_html}



    

#    # If not initialized, find code for launch benchmark
#    if not initialized:
#        r = cmind.access({'action':'find',
#                          'automation':'script',
#                          'artifact':'5dc7662804bc4cad'})
#        if r['return']>0: return r
#
#        lst = r['list']
#
#        if len(lst)>0:
#            external_module_path = os.path.join(lst[0].path, 'dummy')
#            external_module_meta = lst[0].meta
#
#        if external_module_path =='':
#            st.markdown('Warning: can\'t find internal module!')
#            return {'return':0}
#
#        initialized = True
#
#    ii = {'streamlit_module': st,
#          'params': params,
#          'meta': external_module_meta,
#          'skip_title': True,
#          'misc_module': misc}
#
#    return cmind.utils.call_internal_module(None, external_module_path , 'customize', 'gui', ii)
