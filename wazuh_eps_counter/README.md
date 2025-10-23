# EPS Counter scripts

# EPS Counter (Python)

The script obtaines the amount of bytes a file has grown within a windows of time, counts how many "new line" characters are, and returns a value.

## Example usage

Measure for 60 seconds (window), and wazit 1 second in-between measurements (interval), the script will run for 24 hours (86400 seconds), the output values after each run will be saved to a file (output).

```
/var/ossec/framework/python/bin/python3 /path/to/script/eps_counter.py /var/ossec/logs/archives/archives.json --window 60 --interval 1 --run-seconds 86400 --output /var/ossec/logs/eps-counter.log
```

For more information

```
/var/ossec/framework/python/bin/python3 /path/to/script/eps_counter.py --help
```

# EPS Counter (Bash)

The scripts validates how many lines are added after a give time period. Configurations are made as variables within the file

## Example usage

Set the variables:

```
run_for_secs=86400  # 6h=21600 12h=43200 24h=86400
interval=60       # seconds between checks
logFile="/var/ossec/logs/eps-counter.log"
```

The script takes one parameter, the file to measure.

```
/bin/bash /path/to/script/eps_counter.sh /var/ossec/logs/archives/archives.json
```
