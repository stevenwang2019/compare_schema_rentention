import yaml
import os

switcher = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
        'y': 31536000,
    }

def convert_retention_to_int(retention):
    if(len(retention)== 0):
        raise Exception("Empty string")
    if retention.isdigit():
        return int(retention)
    unit = retention[-1]
    exception_msg = "Invalid date"
    multiplier = switcher.get(unit, exception_msg)
    if(multiplier == exception_msg):
        raise Exception(exception_msg)
    value = int(retention[0:-1])
    return value * multiplier

with open(r'type_graphite_storage.yaml') as file:
    content = yaml.full_load(file)
    schemas = content['bigcommerce_graphite_gcp::roles::storage::graphite_schemas']
    directory = 'output/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    for schema, info in schemas.items():
        retentions = info['retentions']
        path = directory + schema
        f = open(path, "w+")
        for retention in retentions:
            freq_str, duration_str = retention.split(':')
            freq = convert_retention_to_int(freq_str)
            duration = convert_retention_to_int(duration_str)
            output_string = "retention: {} secondsPerPoint: {}\n".format(duration, freq)
            f.write(output_string)
        f.close()
