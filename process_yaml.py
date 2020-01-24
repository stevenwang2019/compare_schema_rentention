import yaml
import os
import subprocess
import sys, traceback
import re
from yaml_ordered_dict import *

switcher = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
        'y': 31536000,
    }
wsp_root = '/mnt/data/whisper'
output_dir = 'output/'
diff_dir = 'diff.txt'
if(len(sys.argv) > 1):
    wsp_root = str(sys.argv[1])
diff_list = []

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

def write_to_file(path, list):
    f = open(path, "w+")
    for value in list:
        f.write(value+"\n")
    f.close()

def build_subdir_from_pattern(pattern):
    replaced = re.sub('\\\.','/',pattern)
    if(pattern[0] == '^'):
        replaced = "^"+wsp_root+"/"+replaced[1:]
    else:
        replaced = wsp_root+"/"+replaced
    return replaced

def compare_wsp_retention(wspout, list):
    counter = 0
    prevline = ""
    for line in wspout.split('\n'):
        if 'secondsPerPoint:' in line:
            if(counter == len(list)):
                return 1
            new_duration, new_freq = list[counter].split(' ')
            if prevline.split(':')[1].strip()!= new_duration or line.split(':')[1].strip() != new_freq:
                return 1
            counter+=1
        prevline = line
    if(counter != len(list)):
        return 1
    return 0

class Archive:
    def __init__(self, schema, pattern, rentention_list):
        self.schema = schema
        self.pattern = pattern
        self.rlist = rentention_list

def match_file_path(filepath, archives):
    for arch in archives:
        if re.search(arch.pattern, filepath):
            return arch
    return "not found"

def compare_whisper_info(archives):
    cmd = []
    cmd.append('find')
    cmd.append(wsp_root)
    cmd.append('-name')
    cmd.append('*.wsp')
    # print(cmd)
    try:
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        findout,finderr = out.communicate()
        # print(findout)
        for file in findout.split('\n'):
            if(len(file) == 0):
                continue
            archive = match_file_path(file, archives)
            if(archive == "not found" ):
                continue
            wsp_info_cmd = []
            wsp_info_cmd.append('whisper-info')
            wsp_info_cmd.append(file)
            # print(wsp_info_cmd)
            wsp_out = subprocess.Popen(wsp_info_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            wspout,wsperr = wsp_out.communicate()
            # print(wspout)
            if compare_wsp_retention(wspout, archive.rlist) == 1:
                print("found different retention "+file)
                diff_list.append(file)
    except Exception as ex:
        print(ex)
        traceback.print_exc()
        return

def get_baseline_archives():
    archives = []
    with open(r'type_graphite_storage.yaml') as file:
        content = yaml.load(file, OrderedDictYAMLLoader)
        schemas = content['bigcommerce_graphite_gcp::roles::storage::graphite_schemas']
        create_dir(output_dir)
        for schema, info in schemas.items():
            retentions = info['retentions']
            list = []
            for retention in retentions:
                output_string = convert_retention_to_string(retention)
                list.append(output_string)
            archives.append(Archive(schema, build_subdir_from_pattern(info['pattern']), list))
            #compare_whisper_info(schema, info['pattern'], list)
            write_to_file(output_dir + schema, list)
    return archives

def main():
    archives = get_baseline_archives()
    compare_whisper_info(archives)
    if len(diff_list) > 0:
        print("writing difference to "+diff_dir)
        write_to_file(diff_dir, diff_list)

if __name__== "__main__":
    main()
