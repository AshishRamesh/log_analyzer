import time
import psutil
import GPUtil

# Log memory and CPU usage

def time_init():
    global start_time
    start_time = time.time()
def proc_util():
    process = psutil.Process()
    memory_usage = process.memory_info().rss / (1024 * 1024)  # in MB
    cpu_usage = process.cpu_percent(interval=1)  # CPU usage during the query
    print(f"Memory Usage: {memory_usage:.2f} MB")
    print(f"CPU Usage: {cpu_usage:.2f}%")
    
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        gpu_memory_usage = gpu.memoryUsed / 1024  # in GB
        gpu_utilization = gpu.load * 100  # GPU utilization in percentage
        print(f"GPU Memory Usage: {gpu_memory_usage:.2f} GB")
        print(f"GPU Utilization: {gpu_utilization:.2f}%")

def latency():
    end_time = time.time()
    latency = end_time - start_time
    print(f"Time taken {latency:.2f} seconds")

