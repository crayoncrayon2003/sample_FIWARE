import ckan.plugins.toolkit as tk


@tk.auth_allow_anonymous_access
def sample_get_sum(context, data_dict):
    return {"success": True}


def get_auth_functions():
    return {
        "sample_get_sum": sample_get_sum,
    }
