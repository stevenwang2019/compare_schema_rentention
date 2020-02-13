# compare_schema_rentention

whisper-info is only installed in integration and production, so run below before running the script locally.

pip install pyyaml


[integration][us-central1][infra_2275][root@graphite-storage-9b555cb4]:/home/steven.wang#

`python info-worker.py` for running multi-threaded


`nohup python info_worker.py & ` for running the task in the background. Also consider use >/dev/null 2>&1 so it would not generate a massive nohut.txt file.
