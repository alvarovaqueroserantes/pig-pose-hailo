### Instalación (PC y Raspberry Pi 5)

```bash
git clone https://github.com/tu-usuario/pig-pose-hailo.git
cd pig-pose-hailo
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt


### Run commands

# ─────────────────────────────────────────────────────────────
# 0. Entrar en la carpeta del proyecto
# ─────────────────────────────────────────────────────────────
cd ~/pig-pose-hailo          # ajusta si tu repo está en otra ruta

# ─────────────────────────────────────────────────────────────
# 1. Crear (o recrear) el entorno virtual con Python 3.11
# ─────────────────────────────────────────────────────────────
python -m venv .venv
source .venv/bin/activate

# ─────────────────────────────────────────────────────────────
# 2. Instalar paquetes públicos de PyPI
#    *requirements.txt* NO debe tener la línea hailort==…
# ─────────────────────────────────────────────────────────────
pip install --upgrade pip            # buena costumbre
pip install -r requirements.txt

# ─────────────────────────────────────────────────────────────
# 3. Instalar HailoRT 4.21 desde el wheel ARM64
# ─────────────────────────────────────────────────────────────
pip install /home/mensoft/Downloads/hailort-4.21.0-cp311-cp311-linux_aarch64.whl

# ─────────────────────────────────────────────────────────────
# 4. Verificar que la librería carga
# ─────────────────────────────────────────────────────────────
python - <<'PY'
import hailort, platform, sys
print("OK!  HailoRT version:", hailort.__version__)
print("Python:", sys.version.split()[0], "  Arch:", platform.machine())
PY

# ─────────────────────────────────────────────────────────────
# 5. Ejecutar la demo
#    --src 0      → webcam USB (Video4Linux)
#    --video ...  → ruta a un .mov, .mp4, etc.
# ─────────────────────────────────────────────────────────────
python -m src.app --src 0
#  ó, para un archivo
# python -m src.app --video samples/pig.mov
