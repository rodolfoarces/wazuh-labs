#!/bin/bash

# Wazuh EPS Counter v3.0
# Wazuh Inc. https://wazuh.com
# Hernan Matias Villan <hernan.villan@wazuh.com>

if [ -z "$1" ]; then
  echo -e "Error: Parameter missing!\nUsage: $0 <filename>"
  exit 1
fi

file="$1"
if [ ! -f "$file" ]; then
  echo "Error: File not found!"
  exit 1
fi

run_for_secs=600  # 6h=21600 12h=43200 24h=86400
interval=10       # seconds between checks
logFile="/var/ossec/logs/eps-counter.log"

lines_now=$(wc -l < "$file")
lines_added_total=0
seconds=0
loop_cycles=$((run_for_secs / interval))

echo "[INFO] - $(date +%Y-%m-%dT%H:%M:%S) - EPS Counter started (found $lines_now lines in $file, interval=${interval}s, will run for=${run_for_secs}s)" >> "$logFile"

for ((i=1; i<=$loop_cycles; i++)); do
    seconds=$((seconds + interval))
    new_total=$(wc -l < "$file")

    if [ "$new_total" -lt "$lines_now" ]; then
        echo "[INFO] - $(date +%Y-%m-%dT%H:%M:%S) - Log rotated (lines dropped from $lines_now to $new_total)." >> "$logFile"
        lines_added=$new_total
    else
        lines_added=$((new_total - lines_now))
    fi

    lines_added_total=$((lines_added_total + lines_added))
    lines_now=$new_total

    eps=$(echo "scale=2; $lines_added_total / $seconds" | bc)

    echo "[INFO] - $(date +%Y-%m-%dT%H:%M:%S) - STATS = $lines_added_total added, $lines_now total, $seconds seconds passed, EPS(avg): $eps" >> "$logFile"

    sleep "$interval"
done
