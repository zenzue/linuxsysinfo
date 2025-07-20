import os
import platform
import subprocess
import time

def read_file(path):
    try:
        with open(path) as f:
            return f.read().strip()
    except:
        return None

def get_dmi(field):
    val = read_file(f'/sys/devices/virtual/dmi/id/{field}')
    if val and val != 'None':
        return val
    try:
        output = subprocess.check_output(['dmidecode', '-s', field], stderr=subprocess.DEVNULL)
        return output.decode().strip()
    except:
        return None

def get_cpu_usage():
    try:
        with open('/proc/stat') as f:
            line = f.readline()
        cpu_times = list(map(int, line.strip().split()[1:]))
        idle = cpu_times[3]
        total = sum(cpu_times)
        time.sleep(0.1)
        with open('/proc/stat') as f:
            line2 = f.readline()
        cpu_times2 = list(map(int, line2.strip().split()[1:]))
        idle2 = cpu_times2[3]
        total2 = sum(cpu_times2)
        idle_delta = idle2 - idle
        total_delta = total2 - total
        usage = 100.0 * (1.0 - idle_delta / total_delta) if total_delta else 0
        return f"{usage:.1f}%"
    except:
        return "N/A"

def get_mem():
    try:
        with open('/proc/meminfo') as f:
            lines = f.readlines()
        total = int([x for x in lines if x.startswith("MemTotal")][0].split()[1])
        free = int([x for x in lines if x.startswith("MemAvailable")][0].split()[1])
        used = total - free
        total_gb = total / 1024 / 1024
        used_gb = used / 1024 / 1024
        percent = (used / total) * 100
        return f"{used_gb:.1f} GB / {total_gb:.1f} GB ({percent:.0f}%)"
    except:
        return "N/A"

def get_uptime():
    try:
        with open('/proc/uptime') as f:
            seconds = float(f.readline().split()[0])
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        result = []
        if days > 0:
            result.append(f"{days} day{'s' if days>1 else ''}")
        if hours > 0:
            result.append(f"{hours} hour{'s' if hours>1 else ''}")
        if minutes > 0:
            result.append(f"{minutes} min")
        return ', '.join(result) if result else f"{int(seconds)} sec"
    except:
        return "N/A"

def get_temp():
    paths = [
        '/sys/class/thermal/thermal_zone0/temp',
        '/sys/class/hwmon/hwmon0/temp1_input'
    ]
    for path in paths:
        val = read_file(path)
        if val:
            try:
                temp = float(val) / 1000 if len(val) > 3 else float(val)
                return f"{temp:.1f}°C"
            except:
                continue
    try:
        out = subprocess.check_output(['sensors'], stderr=subprocess.DEVNULL).decode()
        for line in out.splitlines():
            if 'temp1:' in line or 'Core 0:' in line:
                p = [t for t in line.split() if '°C' in t]
                if p:
                    return p[0]
    except:
        pass
    return "N/A"

sys_vendor = get_dmi('sys_vendor') or "N/A"
sys_model = get_dmi('product_name') or "N/A"
board_vendor = get_dmi('board_vendor') or "N/A"
board_name = get_dmi('board_name') or "N/A"
kernel = platform.release()
arch = platform.machine()
cpu_model = "N/A"
try:
    with open('/proc/cpuinfo') as f:
        for line in f:
            if 'model name' in line:
                cpu_model = line.strip().split(":", 1)[1].strip()
                break
except:
    try:
        out = subprocess.check_output(['lscpu'], stderr=subprocess.DEVNULL).decode()
        for line in out.splitlines():
            if "Model name" in line:
                cpu_model = line.split(":", 1)[1].strip()
                break
    except:
        pass

cpu_usage = get_cpu_usage()
mem_usage = get_mem()
uptime = get_uptime()
temp = get_temp()

line = "─" * 58
print(line)
print("   Linux System Overview             |         Powered by w01f")
print(line)
print(f" System   : {sys_vendor} {sys_model}")
print(f" Board    : {board_vendor} {board_name}")
print(f" Kernel   : {kernel} {arch}")
print()
print(f" CPU      : {cpu_model}")
print(f" Usage    : {cpu_usage}")
print(f" Temp     : {temp}")
print()
print(f" Memory   : {mem_usage}")
print(f" Uptime   : {uptime}")
print(line)
