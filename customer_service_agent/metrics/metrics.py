import psutil
import os

def get_resource_usage():
    """
    Mengambil penggunaan resource proses Python saat ini
    """
    process = psutil.Process(os.getpid())

    cpu_percent = process.cpu_percent(interval=0.1)
    memory_info = process.memory_info()

    return {
        "cpu_percent": cpu_percent,
        "memory_mb": memory_info.rss / (1024 * 1024)
    }