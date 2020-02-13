# compare_schema_rentention

whisper-info is only installed in integration and production, so run below before running the script locally.

pip install pyyaml


[integration][us-central1][infra_2275][root@graphite-storage-9b555cb4]:/home/steven.wang#

`python info-worker.py` for running multi-threaded


`nohup python info_worker.py & ` for running the task in the background. Also consider use >/dev/null 2>&1 so it would not generate a massive nohut.txt file.

upload python files to the server
`
C02Z15NGLVCG:compare_schema_rentention steven.wang$ scp -r *.py 10.128.1.13:/home/steven.wang
analyze_diff_txt.py                                                                                            100%  543     2.6KB/s   00:00    
info_worker.py                                                                                                 100% 1954    10.5KB/s   00:00    
process_yaml.py                                                                                                100% 4812    27.0KB/s   00:00    
shared_vars.py                                                                                                 100%  104     0.6KB/s   00:00    
test_process_yaml.py                                                                                           100% 4105    22.4KB/s   00:00    
yaml_ordered_dict.py                                                                                           100% 2007    11.2KB/s   00:00 
`
