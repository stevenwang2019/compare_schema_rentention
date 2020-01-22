import yaml
import os

switcher = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
        'y': 31536000,
    }
wsp_root = '/mnt/data/whisper/'

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

def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def convert_retention_to_string(retention):
    freq_str, duration_str = retention.split(':')
    freq = convert_retention_to_int(freq_str)
    duration = convert_retention_to_int(duration_str)
    # output_string = "retention: {} secondsPerPoint: {}\n".format(duration, freq)
    return "{} {}".format(duration, freq)

def write_to_file(path, pattern ,list):
    f = open(path, "w+")
    for value in list:
        f.write(value+"\n")
    f.close()

def extract_subdir_from_pattern(pattern):
    return pattern[1:].split('\.')[0]

def compare_whisper_info(schema, pattern, list):
    subdir = extract_subdir_from_pattern(pattern)
    #cmd = 'wc -l my_text_file.txt > out_file.txt'
    #os.system(cmd)

with open(r'type_graphite_storage.yaml') as file:
    content = yaml.full_load(file)
    schemas = content['bigcommerce_graphite_gcp::roles::storage::graphite_schemas']
    directory = 'output/'
    create_dir(directory)
    for schema, info in schemas.items():
        retentions = info['retentions']
        list = []
        for retention in retentions:
            output_string = convert_retention_to_string(retention)
            list.append(output_string)
        compare_whisper_info(schema, info['pattern'], list)
        # write_to_file(directory + schema, info['pattern'], list)

