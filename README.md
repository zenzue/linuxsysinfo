# Linux System Info Script

A smart Python script that prints detailed, cleanly-formatted hardware and OS info on any Linux system—laptop, desktop, or VM.

---

## Features

- System vendor/model
- Motherboard/board info
- Kernel version & architecture
- CPU model and usage
- Memory usage (used/total/percent)
- CPU temperature (if available)
- System uptime
- Elegant, readable terminal output

---

## Usage

```bash
python3 sysinfo.py
````

---

## Sample Output

```
────────────────────────────────────────────────────────────────────────────────────────────────────
   Linux System Overview                |         Powered by w01f
────────────────────────────────────────────────────────────────────────────────────────────────────
 Hostname : r00t
 System   : Dell Inc. XPS 13 9300
 Board    : Dell Inc. 077Y9N
 Kernel   : 6.12.39-1-MANJARO x86_64

 CPU      : Intel(R) Core(TM) i7-1065G7 CPU @ 1.30GHz
 Usage    : 0.0%
 Temp     : 20.0°C
 Memory   : 7.7 GB / 15.2 GB (51%)
 Uptime   : 11 min
 Timezone : Asia/Bangkok (+07, +0700)

 Network  : wlp0s20f3: 192.168.x.xxx, br-d19aa134d2b9: 172.18.0.1, docker0: 172.17.0.1
 PublicIP : xxx.xx.xxx.xxx

 Disk     : 432.6 GB / 899.1 GB (48%)
 Disks    :
           - SSD:  Samsung SSD 990 PRO 1TB (931.5 GB) [nvme0n1]
 GPU      :
           - N/A
────────────────────────────────────────────────────────────────────────────────────────────────────
 Top 10 Running Processes
PID USER     %CPU %MEM COMMAND
   6597 root     45.4  0.0 systemd-timedat
   6593 w01f     20.0  0.1 python
   3989 w01f     14.5  2.1 code
   1824 w01f     13.6  2.2 brave
   4004 w01f     12.7  4.0 code
   4993 w01f     10.7  2.5 code
   2308 w01f      9.1  3.2 firefox
   1731 w01f      6.0  0.9 brave
   1684 w01f      5.4  3.1 brave
   2485 w01f      5.2  2.1 Isolated Web Co
────────────────────────────────────────────────────────────────────────────────────────────────────

```

If any value is unavailable, “N/A” will be shown.

---

## Requirements

* Python 3.x
* For temperature: `lm-sensors` utility (optional)

  * Install with: `sudo apt install lm-sensors` or `sudo pacman -Syu lm_sensors`
  * Then run: `sensors-detect` and reboot

---

**Author:** w01f
