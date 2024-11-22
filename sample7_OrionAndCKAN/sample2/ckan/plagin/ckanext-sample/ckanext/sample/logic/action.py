import ckan.plugins.toolkit as tk
import ckanext.sample.logic.schema as schema


@tk.side_effect_free
def sample_get_sum(context, data_dict):
    tk.check_access(
        "sample_get_sum", context, data_dict)
    data, errors = tk.navl_validate(
        data_dict, schema.sample_get_sum(), context)

    if errors:
        raise tk.ValidationError(errors)

    return {
        "left": data["left"],
        "right": data["right"],
        "sum": data["left"] + data["right"]
    }


def get_actions():
    return {
        'sample_get_sum': sample_get_sum,
    }
