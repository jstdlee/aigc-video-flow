#!/usr/bin/env bash
# H3 v6 shots, guarded: run_shots6.sh <take> <shot...>
# The guard interrupts only this run's ComfyUI prompt when total memory passes 97 GiB (80 % cap).
cd "$(dirname "$0")"
take=$1; shift
mkdir -p logs
guard() { while true; do u=$(free -g | awk '/Mem/{print $3}'); if [ "$u" -gt 97 ]; then curl -s -X POST 127.0.0.1:8188/interrupt >/dev/null; echo "$(date +%T) interrupted at ${u} GiB" >> logs/watchdog6.txt; sleep 20; fi; sleep 3; done; }
monitor() { while true; do echo "$(date +%T) $(free -g | awk '/Mem/{print $3}') $(nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader)" >> logs/shots6_t${take}_mon.txt; sleep 10; done; }
guard & GUARD=$!
monitor & MON=$!
python3 gen_shot6.py --take "$take" "$@"
rc=$?
kill $GUARD $MON
echo "peak mem GiB: $(awk '{print $2}' logs/shots6_t${take}_mon.txt | sort -n | tail -1)  peak GPU C: $(awk '{print $3}' logs/shots6_t${take}_mon.txt | sort -n | tail -1)"
exit $rc
