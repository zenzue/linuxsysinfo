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
─────────────────────────────────────────────────────────────
   Linux System Overview             |         Powered by w01f
─────────────────────────────────────────────────────────────
 System   : Dell Inc. XPS 13 9300
 Board    : Dell Inc. 077Y9N
 Kernel   : 6.12.38-1-MANJARO x86_64

 CPU      : Intel(R) Core(TM) i7-1065G7 CPU @ 1.30GHz
 Usage    : 5.7%
 Temp     : 54.0°C

 Memory   : 7.9 GB / 16.0 GB (49%)
 Uptime   : 2 days, 4 hours, 21 min
─────────────────────────────────────────────────────────────
```

If any value is unavailable, “N/A” will be shown.

---

## Requirements

* Python 3.x
* For temperature: `lm-sensors` utility (optional)

  * Install with: `sudo apt install lm-sensors`
  * Then run: `sensors-detect` and reboot

---

**Author:** w01f
