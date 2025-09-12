def strip_unreal_type_prefixes(source_type_id: str) -> str:
    if source_type_id[0] in {'T', 'U', 'C', 'F', 'E'}:
        return source_type_id[1:]
    else: 
        return source_type_id
    
def opt_param_list(functions: list[str], param_ids: list[str]):
    pass

def inline_link(label, link):
    return f'[{label}]({link})'

def gen_bp_img_name(img_label: str) -> str:
    return img_label.lower().replace(' ', '-')

def img_link(label: str, parent_path: str, file_name: str) -> str:
    return f'![{label}]({parent_path}/{file_name}.png)'

def bp_img(label: str, bp_section: str) -> str:
    #return f'![{label}](img/bp/{bp_section}/{gen_bp_img_name(label)}.png){{ loading=lazy }}'

    #@GUIDANCE: We removed lazy loading for now, this is because the first time you switch between tabs it will abruptly put your scrollbar in an unrelated area. Very annoying! Not worth the performance "gains".
    parent_path = f'img/bp/{bp_section}'
    file_name = gen_bp_img_name(label)
    return img_link(label, parent_path, file_name)

def img_install(label: str, file_name: str, section: str) -> str:
    parent_path = f'img/{section}'
    return img_link(label, parent_path, file_name)

def abs_link_coreapi():
    return '/core-api'

def abs_link_special_types():
    return '/core-api/special-types'

def abs_link_adv():
    return '/advanced'

def abs_link_adv_special_types():
    return f'{abs_link_adv()}/special-types'

def link_under(base_link, child_link, subsec: str|None = None):
    if subsec is None:
        return f'{base_link}/{child_link}/'
    else:
        return f'{base_link}/{child_link}/#{subsec}'

def link_under_coreapi(child_link, subsec: str|None = None):
    return link_under(abs_link_coreapi(), child_link, subsec)

def link_under_special_types(child_link, subsec: str|None = None):
    return link_under(abs_link_special_types(), child_link, subsec)

def link_under_special_types(child_link, subsec: str|None = None):
    return link_under(abs_link_special_types(), child_link, subsec)

def cpp_incl(relative_path):
    return f'#include "CakeIO/{relative_path}.h"'
    
def source_block_base(title, body, header_path):
    return f"""
??? info "Source Location: {title}"
    {body}
    ```c++
    #include "{header_path}"
    ```
"""
def gen_header_path(file_name: str, rel_loc: str|None) -> str:
    result = 'CakeIO/'
    if rel_loc:
        result += f'{rel_loc}/'
    result += f'{file_name}.h'
    return result

def source_loc_single(type_id: str, file_name: str, rel_loc: str|None = None) -> str:
    header_path = gen_header_path(file_name, rel_loc)
    body = f'{type_id} is defined in `{header_path}`'
    return source_block_base(type_id, body, header_path)

def source_loc_custom(id: str, file_name: str, body: str, rel_loc: str|None = None):
    header_path = gen_header_path(file_name, rel_loc)
    return source_block_base(id, body, header_path)

def source_loc_group(group_id, file_name, rel_loc: str|None = None):
    body = f'The following types are all defined in the following header:'
    return source_loc_custom(group_id, file_name, body, rel_loc)

def missing_content(content_id, note=None):
    result = f"""
??? failure "Missing Content: [{content_id}]"
    Content __[{content_id}]__ must be added before the docs are considered complete.
    """
    if note:
        result += f"""

    NOTE: _{note}_
"""
    return result

def define_env(env):
    """
    This is the hook for the variables, macros and filters.
    """
    @env.macro
    def src_loc_group(group_id: str, file_name:str, rel_loc: str|None=None):
        return source_loc_group(group_id, file_name, rel_loc)
    
    @env.macro
    def src_loc_ex(id: str, file_name:str, body: str, rel_loc: str|None=None):
        return source_loc_custom(id, file_name, body, rel_loc)

    @env.macro
    def src_loc_single(type_id, file_name: str, rel_loc: str|None=None):
        return source_loc_single(type_id, file_name, rel_loc)

    @env.macro
    def src_log_single_bp(type_id, rel_loc=None):
        bp_path = f'Blueprint'
        if rel_loc:
            bp_path += f'/{rel_loc}'
        return source_loc_single(type_id, bp_path)
    
    @env.macro
    def mark_missing(content_id, note=None):
        return missing_content(content_id, note)

    @env.macro
    def open_csv_by_typename(typename):
        return f'tables/csvmap_{typename}.csv'

    @env.macro
    def csv_policy(id):
        return open_csv_by_typename(f'ECakePolicy{id}')
    
    @env.macro
    def type_header(type_id, src_fn):
        return f"""{type_id}
{src_fn(type_id)}
"""
    @env.macro
    def bp_img_path(label):
        return bp_img(label, 'path')

    @env.macro
    def img_install_fab(label: str, file_name: str) -> str:
        return img_install(label, file_name, 'fab')

    @env.macro
    def bp_img_file_ext(label):
        return bp_img(label, 'file-ext')
    
    @env.macro
    def bp_img_file(label):
        return bp_img(label, 'file')

    @env.macro
    def bp_img_dir(label):
        return bp_img(label, 'dir')
    
    @env.macro
    def bp_file_query_func(label):
        return f"""
    { bp_img_file(label) }
    --8<-- "bp-warn-query-flag.md"
"""
    @env.macro
    def bp_img_error_handling(label):
        return bp_img(label, 'error-handling')

    @env.macro
    def bp_img_cakemix(label):
        return bp_img(label, 'cake-mix-library')

    @env.macro
    def bp_img_async(label):
        return bp_img(label, 'async')

    @env.macro
    def bp_img_ext_filter(label):
        return bp_img(label, 'ext-filter')

    @env.macro
    def bp_img_tour(label):
        return bp_img(label, 'tour')
    
    @env.macro
    def cpp_assumed_include(rel_path):
        return f"""
    All C++ examples in this section assume the following include statement:

    ```c++
    {cpp_incl(rel_path)}
    ```
"""
    @env.macro
    def cpp_impl_source(obj_id, type_name, relative_src_path):
        return f"""
    The native {obj_id} object in CakeFS is **{type_name}**, which is defined in `CakeIO/{relative_src_path}.h`.

{cpp_assumed_include(relative_src_path)}
"""

    @env.macro
    def bp_impl_source(obj_id, type_name, relative_src_path):
        return f"""
    The Blueprint {obj_id} object in CakeFS is **{type_name}**, which is defined in `CakeIO/Blueprint/{relative_src_path}.h`.
"""
    
    @env.macro
    def policy_link(policy_id):
        return f"""
[{policy_id}](/core-api/special-types/policies/#{policy_id.lower()})
"""
    
    @env.macro
    def link_cakepath(label='CakePath', subsec: str|None = None):
        return inline_link(label, link_under_coreapi('paths', subsec))

    @env.macro
    def link_cakefileext(label='CakeFileExt', subsec: str|None = None):
        return inline_link(label, link_under_coreapi('file-extensions', subsec))

    @env.macro
    def link_cakefile(label='CakeFile', subsec: str|None = None):
        return inline_link(label, link_under_coreapi('files', subsec))

    @env.macro
    def link_cakedir(label='CakeDir', subsec: str|None = None):
        return inline_link(label, link_under_coreapi('directories', subsec))

    @env.macro
    def link_policies(label='CakePolicies', subsec: str|None = None):
        return inline_link(label, link_under_special_types('policies', subsec))

    @env.macro
    def link_errormap(label='Error Maps', subsec: str|None = None):
        return inline_link(label, link_under_coreapi('error-maps', subsec))

    @env.macro
    def link_outcomes(label='Outcomes', subsec: str|None = None):
        return inline_link(label, link_under_special_types('outcomes', subsec))

    @env.macro
    def link_results(label='Results', subsec: str|None = None):
        return inline_link(label, link_under_special_types('results', subsec))

    @env.macro
    def link_extfilter(label='CakeExtFilter', subsec: str|None = None):
        return inline_link(label, link_under_special_types('cakeextfilter', subsec))

    @env.macro
    def link_cakemix(label='CakeMix', subsec: str|None = None):
        return inline_link(label, link_under_coreapi('cake-mix', subsec))

    @env.macro
    def link_cake_async(label='CakeFS Async', subsec: str|None = None):
        return inline_link(label, link_under_coreapi('async-io', subsec))

    @env.macro
    def link_cakeservices(label='CakeFS Services', subsec: str|None = None):
        return inline_link(label, link_under_coreapi('services', subsec))

    @env.macro
    def bp_currently_unsupported(feature_label: str):
        return f'''
    {feature_label} is not currently supported for Blueprint due to limitations inherent with UObjects and multi-threaded contexts. As Unreal Engine evolves CakeFS will be looking for opportunities to add this functionality to the Blueprint API.
'''