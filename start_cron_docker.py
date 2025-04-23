import keyring
import logging
import os
import subprocess
import sys

from logging.handlers import RotatingFileHandler
from pathlib import Path
from keyring.backends import Windows

local_appdata = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
app_dir = local_appdata / "media-docker-credentials"
log_dir = app_dir / "logs"
log_file = log_dir / "inject_credentials.log"

log_dir.mkdir(parents=True, exist_ok=True)

max_bytes = 10 * 1024 * 1024  # 10 MB
backup_count = 5

log_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
log_format = '%(asctime)s %(levelname)s %(message)s'
log_datefmt = '%d-%m-%Y %H:%M:%S'
formatter = logging.Formatter(log_format, log_datefmt)

log_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)

DOCKER_CONTAINER_NAME = "freeboxos_select"

keyring.set_keyring(Windows.WinVaultKeyring())

USERNAME_MEDIASELECT = keyring.get_password("media-select", "email")
PASSWORD_MEDIASELECT = keyring.get_password("media-select", "password")
FREEBOX_SERVER_IP = keyring.get_password("freeboxos", "username")
ADMIN_PASSWORD = keyring.get_password("freeboxos", "password")

if not USERNAME_MEDIASELECT or not PASSWORD_MEDIASELECT or not FREEBOX_SERVER_IP or not ADMIN_PASSWORD:
    logging.error("Credentials not found by keyring.")
    sys.exit(1)

env_command = (
    f"export USERNAME_MEDIASELECT='{USERNAME_MEDIASELECT}' "
    f"PASSWORD_MEDIASELECT='{PASSWORD_MEDIASELECT}' "
    f"FREEBOX_SERVER_IP='{FREEBOX_SERVER_IP}' ADMIN_PASSWORD='{ADMIN_PASSWORD}' && "
    f"/home/seluser/.venv/bin/python3 /home/seluser/select-freeboxos/cron_docker.py "
    ">> /var/log/select_freeboxos/select_freeboxos.log 2>&1"
)

try:
    subprocess.run(
        ["docker", "exec", "-u", "seluser", DOCKER_CONTAINER_NAME, "bash", "-c", env_command],
        check=True
    )
    print("Credentials injected and script started successfully.")
except subprocess.CalledProcessError as e:
    print("Error injecting credentials:", e)
