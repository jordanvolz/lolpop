def check_counts(obj, data, *args, **kwargs):
    target = obj._get_config("model_target")
    num_labels = data[target].nunique()
    return ( num_labels> 1, "Found %s unique labels" %num_labels)

