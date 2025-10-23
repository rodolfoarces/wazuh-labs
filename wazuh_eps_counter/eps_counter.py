import argparse
import os
import time
from collections import deque

#!/usr/bin/env python3
"""
EPS Counter (Python) v.1.0
Wazuh Inc.
Rodolfo "Rolf" Arce Sannemann <rodolfo.arce@wazuh.com>

--

Realtime log-line counter with rotation/truncation handling.

Usage:
    python3 log_rate.py /path/to/log --window 60 --interval 1

Default behavior is to "tail" the file (start at its end) and every interval
seconds print how many complete lines were added during the last `window` seconds.

Notes:
- Efficient: only reads newly-appended bytes.
- Detects rotation (inode change) and truncation (size < last_offset) and adapts.
- Counts lines by counting newline bytes (b'\n').
"""


def stat_id(st):
        # Return a stable identity for the file if available (inode+device), otherwise use None
        try:
                return (st.st_ino, st.st_dev)
        except AttributeError:
                return None

def open_log(path, start_at_end=True):
        f = open(path, "rb")
        if start_at_end:
                f.seek(0, os.SEEK_END)
        else:
                f.seek(0, os.SEEK_SET)
        st = os.fstat(f.fileno())
        return f, stat_id(st), f.tell()

def safe_stat(path):
        try:
                return os.stat(path)
        except FileNotFoundError:
                return None

def main():
        parser = argparse.ArgumentParser(description="Realtime lines-per-window counter for a log file.")
        parser.add_argument("path", help="Path to log file to follow")
        parser.add_argument("--window", "-w", type=float, default=60.0, help="Sliding window in seconds (default 60)")
        parser.add_argument("--interval", "-i", type=float, default=1.0, help="Output/update interval in seconds (default 1)")
        parser.add_argument("--from-start", action="store_true", help="Start counting from beginning of file instead of tailing")
        parser.add_argument("--output", "-o", type=str, default=None, help="Output file path (default: stdout)")
        parser.add_argument("--run-seconds", "-r", type=float, default=None, help="Run for a limited number of seconds (default: run indefinitely)")
        args = parser.parse_args()

        path = args.path
        window = float(args.window)
        interval = float(args.interval)
        start_at_end = not args.from_start

        # deque of (timestamp, count_of_new_lines)
        history = deque()
        start_date_time = time.time()

        f = None
        fid = None
        offset = 0

        while True:
                st = safe_stat(path)
                if st is None:
                        # File missing: close if open and wait
                        if f:
                                try:
                                        f.close()
                                except Exception:
                                        pass
                                f = None
                                fid = None
                                offset = 0
                        time.sleep(max(0.1, interval/4.0))
                        continue

                # If not open yet, open file
                if f is None:
                        try:
                                f, fid, offset = open_log(path, start_at_end)
                        except Exception:
                                time.sleep(max(0.1, interval/4.0))
                                continue

                # Check current file identity and size
                try:
                        cur_st = os.stat(path)
                except FileNotFoundError:
                        # disappeared in the meantime
                        time.sleep(max(0.1, interval/4.0))
                        continue

                cur_id = stat_id(cur_st)

                # Rotation detection: different id (inode/dev) -> reopen
                if fid is None or (cur_id is not None and cur_id != fid):
                        # File rotated or replaced. Close and reopen new file.
                        try:
                                f.close()
                        except Exception:
                                pass
                        try:
                                f, fid, offset = open_log(path, start_at_end=False)
                        except Exception:
                                f = None
                                fid = None
                                offset = 0
                        # Continue to next loop to attempt reading newly-opened file
                        continue

                # Truncation detection: size < offset
                cur_size = cur_st.st_size
                if cur_size < offset:
                        # file truncated: seek to start
                        f.seek(0, os.SEEK_SET)
                        offset = 0

                # Read newly appended bytes
                try:
                        f.seek(offset, os.SEEK_SET)
                        new_bytes = f.read()
                except Exception:
                        # On any I/O error, try to reopen on next iteration
                        try:
                                f.close()
                        except Exception:
                                pass
                        f = None
                        fid = None
                        offset = 0
                        time.sleep(max(0.1, interval/4.0))
                        continue

                if new_bytes:
                        # count newlines
                        new_lines = new_bytes.count(b"\n")
                        ts = time.time()
                        history.append((ts, new_lines))
                        offset = f.tell()

                # purge old entries outside the window
                cutoff = time.time() - window
                while history and history[0][0] < cutoff:
                        history.popleft()

                # sum counts in window
                total = sum(c for _, c in history)
                
                lines_per_second = total / window if window > 0 else 0

                # output result
                if args.output:
                        with open(args.output, "a") as out_f:
                                out_f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}  lines_in_last_{int(window)}s: {total}  lines_per_second: {lines_per_second:.2f}\n")
                                out_f.flush()
                else:
                    print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')}  lines_in_last_{int(window)}s: {total}  lines_per_second: {lines_per_second:.2f}", flush=True)

                # If run_seconds is specified, check if we should exit
                if args.run_seconds is not None:
                        if time.time() - start_date_time >= args.run_seconds:
                                f.close()
                                print("Finished running for specified duration. Exiting.")
                                break
                time.sleep(interval)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting on user interrupt.")
        exit(0)
