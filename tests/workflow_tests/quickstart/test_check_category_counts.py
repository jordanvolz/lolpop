def test(obj, data, *args, **kwargs):
    target = obj._get_conf("model_target")
    return data[target].nunique() > 1

