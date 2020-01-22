import yaml
import os
import subprocess
import sys, traceback

switcher = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
        'y': 31536000,
    }
wsp_root = '/mnt/data/whisper/'
diff_list = []
checked = []
if(len(sys.argv) > 1):
    wsp_root = str(sys.argv[1])

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

def extract_subdir_from_pattern(pattern):
    return pattern[1:].split('\.')[0]

def compare_wsp_retention(wspout, list):
    counter = 0
    prevline = ""
    for line in wspout.split('\n'):
        if 'secondsPerPoint:' in line:
            new_duration, new_freq = list[counter].split(' ')
            if prevline.split(':')[1]!= new_duration and line.split(':')[1] != new_freq:
                return 1
        prevline = line
    return 0

def compare_whisper_info(schema, pattern, list):
    subdir = extract_subdir_from_pattern(pattern)
    if(subdir in checked):
        print('previously checked: '+subdir)
        return
    checked.append(subdir)
    cmd = 'find '+wsp_root+subdir+" -name *.wsp"
    print(cmd)
    try:
        out = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout,stderr = out.communicate()
        print(stdout)
        for file in stdout.split('\n'):
            wsp_info_cmd = 'whisper-info '+ file
            wsp_out = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            wspout,wsperr = wsp_out.communicate()
            if compare_wsp_retention(wspout, list) == 1:
                diff_list.append(file)
    except Exception as ex:
        print(ex)
        traceback.print_exc()
        return

with open(r'type_graphite_storage.yaml') as file:
    content = yaml.full_load(file)
    schemas = content['bigcommerce_graphite_gcp::roles::storage::graphite_schemas']
    directory = 'output/'
    create_dir(directory)
    create_dir('diff/')
    for schema, info in schemas.items():
        retentions = info['retentions']
        list = []
        for retention in retentions:
            output_string = convert_retention_to_string(retention)
            list.append(output_string)
        compare_whisper_info(schema, info['pattern'], list)
        # write_to_file(directory + schema, list)
    print("diff_list is :")
    for diff in diff_list:
        print(diff)
    write_to_file('diff/'+schema, diff_list)
