#!/usr/bin/env python3
"""
Script para instalar dependências em ordem correta
Use este script no lugar do pip install -r requirements.txt
"""
import subprocess
import sys
import os

def run_command(cmd, description):
    """Executa comando e mostra resultado"""
    print(f"🔧 {description}: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description}: OK")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}: FALHA")
        print(f"Erro: {e.stderr}")
        return False

def main():
    print("📦 Instalando dependências do osu!droid RX Server")
    print("=" * 55)

    # Passo 1: Instalar maturin primeiro
    if not run_command([sys.executable, "-m", "pip", "install", "maturin>=1.0.0"],
                      "Instalando maturin (build tool)"):
        return False

    # Passo 2: Instalar rosu-pp-py separadamente
    if not run_command([sys.executable, "-m", "pip", "install", "git+https://github.com/unclem2/rosu-pp-py"],
                      "Instalando rosu-pp-py (PP calculator)"):
        return False

    # Passo 3: Instalar resto das dependências (exceto rosu-pp-py)
    deps_to_install = [
        "aiohttp~=3.10.5",
        "asyncpg",
        "coloredlogs==15.0.1",
        "Hypercorn==0.17.3",
        "python-dotenv==1.0.1",
        "python-socketio~=5.11.4",
        "Quart~=0.19.6",
        "Werkzeug~=3.0.4",
        "discord-webhook[async]==1.3.1",
        "geoip2==4.8.1",
        "pytest~=8.3.4",
        "requests~=2.32.3",
        "javaobj-py3~=0.4.4",
        # "Mailgun==0.1.0",  # Removido por enquanto
    ]

    # Instalar em lotes menores para evitar problemas
    batch_size = 5
    for i in range(0, len(deps_to_install), batch_size):
        batch = deps_to_install[i:i+batch_size]
        if not run_command([sys.executable, "-m", "pip", "install"] + batch,
                          f"Instalando lote {i//batch_size + 1} de dependências"):
            return False

    print("\n🎉 Todas as dependências instaladas com sucesso!")
    print("🚀 Agora você pode executar: python main.py")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
