import os, platform, subprocess, socket, shutil, time, urllib.request, datetime

def read_file(path):
    try: return open(path).read().strip()
    except: return None

def get_dmi(field):
    val = read_file(f'/sys/devices/virtual/dmi/id/{field}')
    if val and val != 'None': return val
    try: return subprocess.check_output(['dmidecode', '-s', field], stderr=subprocess.DEVNULL).decode().strip()
    except: return None

def get_cpu_usage():
    try:
        with open('/proc/stat') as f: line = f.readline()
        cpu_times = list(map(int, line.strip().split()[1:]))
        idle, total = cpu_times[3], sum(cpu_times)
        time.sleep(0.1)
        with open('/proc/stat') as f: line2 = f.readline()
        cpu_times2 = list(map(int, line2.strip().split()[1:]))
        idle2, total2 = cpu_times2[3], sum(cpu_times2)
        usage = 100.0 * (1.0 - (idle2 - idle) / (total2 - total)) if (total2-total) else 0
        return f"{usage:.1f}%"
    except: return "N/A"

def get_mem():
    try:
        lines = open('/proc/meminfo').readlines()
        total = int([x for x in lines if x.startswith("MemTotal")][0].split()[1])
        free = int([x for x in lines if x.startswith("MemAvailable")][0].split()[1])
        used, percent = total - free, (total - free) / total * 100
        return f"{(used/1024/1024):.1f} GB / {(total/1024/1024):.1f} GB ({percent:.0f}%)"
    except: return "N/A"

def get_uptime():
    try:
        sec = float(open('/proc/uptime').read().split()[0])
        d, h, m = int(sec//86400), int((sec%86400)//3600), int((sec%3600)//60)
        s = int(sec%60)
        txt = []
        if d: txt.append(f"{d} day{'s' if d>1 else ''}")
        if h: txt.append(f"{h} hour{'s' if h>1 else ''}")
        if m: txt.append(f"{m} min")
        return ', '.join(txt) if txt else f"{s} sec"
    except: return "N/A"

def get_temp():
    try:
        out = subprocess.check_output(['sensors'], stderr=subprocess.DEVNULL).decode()
        temps = []
        cpu_temp = None
        for line in out.splitlines():
            line = line.strip()
            if 'Package id 0:' in line or 'Tdie:' in line:
                v = [t for t in line.split() if '°C' in t]
                if v:
                    cpu_temp = v[0]
                    break
            if 'Core 0:' in line or 'Tctl:' in line or 'Physical id 0:' in line:
                v = [t for t in line.split() if '°C' in t]
                if v:
                    temps.append(float(v[0].replace('°C','')))
        if cpu_temp:
            return cpu_temp
        if temps:
            return f"{max(temps):.1f}°C"
    except:
        pass
    paths = ['/sys/class/thermal/thermal_zone0/temp','/sys/class/hwmon/hwmon0/temp1_input']
    for p in paths:
        val = read_file(p)
        if val:
            try: 
                t = float(val)
                if t > 200: t = t / 1000
                if t > 0 and t < 130:
                    return f"{t:.1f}°C"
            except: continue
    return "N/A"


def get_hostname():
    try: return socket.gethostname()
    except: return "N/A"

def get_network():
    ip_info = []
    try:
        out = subprocess.check_output("ip -4 -o addr show".split()).decode().splitlines()
        for l in out:
            iface = l.split()[1]
            ip = l.split()[3].split('/')[0]
            if iface != "lo":
                ip_info.append(f"{iface}: {ip}")
    except: pass
    if not ip_info:
        try:
            ip = socket.gethostbyname(socket.gethostname())
            ip_info.append(f"default: {ip}")
        except: ip_info = ["N/A"]
    try:
        g = subprocess.check_output("ip route | grep default".split(), stderr=subprocess.DEVNULL).decode().split()
        gw = g[2] if len(g) > 2 else None
    except: gw = None
    return ip_info, gw

def get_public_ip():
    urls = ["https://api.ipify.org", "https://ifconfig.me/ip", "https://ipecho.net/plain"]
    for url in urls:
        try:
            with urllib.request.urlopen(url, timeout=5) as r:
                ip = r.read().decode().strip()
                if ip and len(ip.split(".")) == 4:
                    return ip
        except: continue
    return "N/A"

def get_disk_usage():
    try:
        t, u, f = shutil.disk_usage('/')
        total = t / (1024**3)
        used = (t-f) / (1024**3)
        percent = (t-f)/t*100
        return f"{used:.1f} GB / {total:.1f} GB ({percent:.0f}%)"
    except: return "N/A"

def get_disks():
    disks = []
    try:
        for d in os.listdir('/sys/block'):
            if d.startswith('loop') or d.startswith('ram'): continue
            model = read_file(f"/sys/block/{d}/device/model") or "N/A"
            vendor = read_file(f"/sys/block/{d}/device/vendor") or ""
            size = read_file(f"/sys/block/{d}/size")
            if size:
                gb = int(size)*512/(1024**3)
                size_s = f"{gb:.1f} GB"
            else:
                size_s = "N/A"
            typ = "SSD" if os.path.exists(f"/sys/block/{d}/queue/rotational") and read_file(f"/sys/block/{d}/queue/rotational") == '0' else "HDD"
            serial = read_file(f"/dev/disk/by-id/ata-{model}") or "N/A"
            disks.append(f"{typ}: {vendor} {model} ({size_s}) [{d}]")
    except: pass
    return disks if disks else ["N/A"]

def get_timezone():
    try:
        out = subprocess.check_output(["timedatectl"], stderr=subprocess.DEVNULL).decode()
        for line in out.splitlines():
            if "Time zone" in line:
                return line.split(":",1)[1].strip()
    except:
        try:
            tz = time.tzname
            return tz[0] if tz else "N/A"
        except: return "N/A"
    return "N/A"

def get_gpu_status():
    try:
        out = subprocess.check_output(["nvidia-smi", "--query-gpu=name,utilization.gpu,temperature.gpu,memory.used,memory.total", "--format=csv,noheader,nounits"], stderr=subprocess.DEVNULL).decode()
        gpus = []
        for line in out.strip().splitlines():
            n, util, temp, memu, memt = [x.strip() for x in line.split(",")]
            gpus.append(f"{n}: Load {util}% | Temp {temp}°C | Mem {memu}/{memt} MB")
        return gpus if gpus else ["N/A"]
    except: return ["N/A"]

def get_top_processes():
    try:
        out = subprocess.check_output("ps -eo pid,user,pcpu,pmem,comm --sort=-pcpu | head -n 11", shell=True, stderr=subprocess.DEVNULL).decode()
        lines = out.strip().splitlines()
        return lines
    except: return ["N/A"]

sys_vendor = get_dmi('sys_vendor') or "N/A"
sys_model = get_dmi('product_name') or "N/A"
board_vendor = get_dmi('board_vendor') or "N/A"
board_name = get_dmi('board_name') or "N/A"
kernel = platform.release()
arch = platform.machine()
cpu_model = "N/A"
try:
    for line in open('/proc/cpuinfo'):
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
    except: pass

cpu_usage = get_cpu_usage()
mem_usage = get_mem()
uptime = get_uptime()
temp = get_temp()
hostname = get_hostname()
ip_info, gateway = get_network()
public_ip = get_public_ip()
disk_usage = get_disk_usage()
disks = get_disks()
timezone = get_timezone()
gpu_status = get_gpu_status()
top_procs = get_top_processes()

line = "─" * 100
print(line)
print("   Linux System Overview                |         Powered by w01f")
print(line)
print(f" Hostname : {hostname}")
print(f" System   : {sys_vendor} {sys_model}")
print(f" Board    : {board_vendor} {board_name}")
print(f" Kernel   : {kernel} {arch}\n")
print(f" CPU      : {cpu_model}")
print(f" Usage    : {cpu_usage}")
print(f" Temp     : {temp}")
print(f" Memory   : {mem_usage}")
print(f" Uptime   : {uptime}")
print(f" Timezone : {timezone}\n")
print(f" Network  : {', '.join(ip_info)}")
print(f" PublicIP : {public_ip}")
if gateway: print(f" Gateway  : {gateway}\n")
else: print()
print(f" Disk     : {disk_usage}")
print(f" Disks    :")
for d in disks: print(f"           - {d}")
print(f" GPU      :")
for g in gpu_status: print(f"           - {g}")
print(line)
print(" Top 10 Running Processes")
if top_procs and isinstance(top_procs, list):
    for idx, p in enumerate(top_procs):
        print(p)
print(line)
