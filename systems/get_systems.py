from flask import Blueprint, jsonify, request
from db.auth import token_required
import platform
import psutil
import socket
import time

systems_bp = Blueprint('systems', __name__, url_prefix='/systems')

# --- System Routes ---
def safe(callable_):
    try:
        return callable_()
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        return None

# --- System Routes ---
def get_all_system_info():
    return {
        "hostname": socket.gethostname(),
        "fqdn": socket.getfqdn(),

        "platform": {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },

        "boot_time": psutil.boot_time(),
        "uptime_seconds": int(time.time() - psutil.boot_time()),

        "cpu": {
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "usage_percent": psutil.cpu_percent(interval=0.1),
            "per_cpu_percent": psutil.cpu_percent(interval=0.1, percpu=True),
            "frequency": safe(lambda: psutil.cpu_freq()._asdict()),
            "times": psutil.cpu_times()._asdict(),
            "stats": psutil.cpu_stats()._asdict(),
        },

        "memory": {
            "virtual": psutil.virtual_memory()._asdict(),
            "swap": psutil.swap_memory()._asdict(),
        },

        "disk": {
            "partitions": {
                part.device: {
                    "mountpoint": part.mountpoint,
                    "fstype": part.fstype,
                    "usage": safe(lambda: psutil.disk_usage(part.mountpoint)._asdict())
                }
                for part in psutil.disk_partitions(all=False)
            },
            "io": psutil.disk_io_counters()._asdict(),
        },

        "network": {
            "io": psutil.net_io_counters()._asdict(),
            "adapters": {
                iface: [addr._asdict() for addr in addrs]
                for iface, addrs in psutil.net_if_addrs().items()
            },
        }
    }

@systems_bp.route("/", methods=["GET"])
@token_required
def get_system_info():
    return get_all_system_info(), 200

@systems_bp.route("/hostname", methods=["GET"])
@token_required
def system_hostname():
    return {"hostname": get_all_system_info()["hostname"]}, 200

@systems_bp.route("/fqdn", methods=["GET"])
@token_required
def system_fqdn():
    return {"fqdn": get_all_system_info()["fqdn"]}, 200

@systems_bp.route("/platform", methods=["GET"])
@token_required
def system_platform():
    return get_all_system_info()["platform"], 200

@systems_bp.route("/boot_time", methods=["GET"])
@token_required
def system_boot_time():
    return {"boot_time": get_all_system_info()["boot_time"]}, 200

@systems_bp.route("/uptime_seconds", methods=["GET"])
@token_required
def system_uptime():
    return {"uptime_seconds": get_all_system_info()["uptime_seconds"]}, 200

@systems_bp.route("/cpu", methods=["GET"])
@token_required
def system_cpu():
    return get_all_system_info()["cpu"], 200

@systems_bp.route("/memory", methods=["GET"])
@token_required
def system_memory():
    return get_all_system_info()["memory"], 200

@systems_bp.route("/disks", methods=["GET"])
@token_required
def system_disk():
    return get_all_system_info()["disk"], 200

@systems_bp.route("/disks/<path:partition>", methods=["GET"])
@token_required
def system_disk_partition(partition):
    disks = get_all_system_info()["disk"]["partitions"]

    if partition not in disks:
        return {"error": f"Partition {partition} not found"}, 404

    return disks[partition], 200

@systems_bp.route("/networks", methods=["GET"])
@token_required
def system_network():
    return get_all_system_info()["network"], 200

@systems_bp.route("/networks/<adapter>", methods=["GET"])
@token_required
def system_network_adapter(adapter):
    adapters = get_all_system_info()["network"]["adapters"]

    if adapter not in adapters:
        return {"error": f"Network adapter {adapter} not found"}, 404

    return {
        "adapter": adapter,
        "addresses": adapters[adapter]}, 200


# Ensure sub-modules are loaded
from . import post_systems, delete_systems