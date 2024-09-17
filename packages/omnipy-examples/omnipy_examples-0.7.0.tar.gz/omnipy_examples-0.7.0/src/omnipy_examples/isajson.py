from omnipy.compute.flow import LinearFlowTemplate
from omnipy.modules.general.tasks import import_directory
from omnipy.modules.json.flows import (flatten_nested_json,
                                       transpose_dicts_of_lists_of_dicts_2_lists_of_dicts)
from omnipy.modules.json.tasks import convert_dataset_string_to_json
from omnipy.modules.pandas.tasks import convert_dataset_list_of_dicts_to_pandas


@LinearFlowTemplate(
    import_directory.refine(
        name='import_json_files_from_dir',
        fixed_params=dict(include_suffixes=('.json',)),
    ),
    convert_dataset_string_to_json,
    transpose_dicts_of_lists_of_dicts_2_lists_of_dicts,
    flatten_nested_json,
    convert_dataset_list_of_dicts_to_pandas,
)
def convert_isa_json_to_relational_tables(dir_path: str):
    ...
