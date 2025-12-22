#!/usr/bin/env python3
"""
Script de setup automático para o osu!droid RX Server
Instala todas as dependências, incluindo Rust e maturin, e inicia o servidor
"""
import os
import sys
import subprocess
import platform
import urllib.request
import zipfile
import tarfile
import shutil

def run_command(cmd, check=True, shell=False):
    """Executa um comando e retorna o resultado"""
    print(f"🔧 Executando: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        result = subprocess.run(cmd, shell=shell, check=check, capture_output=True, text=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar comando: {e}")
        return False

def install_rust():
    """Instala Rust se não estiver instalado"""
    print("🔧 Verificando Rust...")

    # Verifica se rustc está instalado
    if run_command(["rustc", "--version"], check=False):
        print("✅ Rust já está instalado")
        return True

    print("📦 Instalando Rust...")

    # Download e instalação do rustup
    if platform.system() == "Windows":
        rustup_url = "https://win.rustup.rs/x86_64"
        rustup_installer = "rustup-init.exe"

        print(f"📥 Baixando rustup de {rustup_url}")
        urllib.request.urlretrieve(rustup_url, rustup_installer)

        # Executa o instalador
        if run_command([rustup_installer, "-y", "--default-toolchain", "stable"], shell=True):
            # Remove o instalador
            os.remove(rustup_installer)
            print("✅ Rust instalado com sucesso")
            return True
        else:
            os.remove(rustup_installer)
            return False
    else:
        # Para Linux/Mac
        rustup_script = "/tmp/rustup.sh"
        print("📥 Baixando rustup...")
        urllib.request.urlretrieve("https://sh.rustup.rs", rustup_script)

        # Torna executável e executa
        os.chmod(rustup_script, 0o755)
        if run_command([rustup_script, "-y", "--default-toolchain", "stable"]):
            os.remove(rustup_script)
            print("✅ Rust instalado com sucesso")
            return True
        else:
            os.remove(rustup_script)
            return False

def install_maturin():
    """Instala maturin via pip"""
    print("📦 Instalando maturin...")
    return run_command([sys.executable, "-m", "pip", "install", "maturin>=1.0.0"])

def install_dependencies():
    """Instala todas as dependências Python"""
    print("📦 Instalando dependências Python...")

    # Primeiro instala maturin separadamente
    if not install_maturin():
        print("❌ Falha ao instalar maturin")
        return False

    # Depois instala o resto
    return run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def setup_database():
    """Configura o banco de dados se necessário"""
    print("🗄️  Verificando banco de dados...")
    # Aqui poderia ter lógica para configurar PostgreSQL
    # Mas por enquanto vamos pular
    print("ℹ️  Configure o DATABASE_URL no painel do ShardCloud")
    return True

def create_env_file():
    """Cria arquivo .env se não existir"""
    if os.path.exists('.env'):
        print("✅ Arquivo .env já existe")
        return True

    print("📝 Criando arquivo .env...")

    # Copia do env-example.txt se existir
    if os.path.exists('env-example.txt'):
        shutil.copy('env-example.txt', '.env')
        print("✅ Arquivo .env criado a partir de env-example.txt")
        print("⚠️  Edite o arquivo .env com suas configurações!")
        return True
    else:
        # Cria um básico
        with open('.env', 'w') as f:
            f.write("""# Configure estas variáveis!

# Servidor
SERVER_PORT=8080
SERVER_IP=0.0.0.0
SERVER_DOMAIN=seu-dominio.shardcloud.app

# Banco (ShardCloud fornece)
DATABASE_URL=postgresql://usuario:senha@host:porta/database

# API do osu!
OSU_KEY=sua_api_key_aqui

# Email (Mailgun recomendado)
MAILGUN_API_KEY=sua_api_key_aqui
MAILGUN_DOMAIN=sandboxXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.mailgun.org

# Outras configurações...
""")
        print("✅ Arquivo .env básico criado")
        print("⚠️  Configure suas chaves API!")
        return True

def start_server():
    """Inicia o servidor"""
    print("🚀 Iniciando servidor...")
    print("ℹ️  Pressione Ctrl+C para parar")

    try:
        # Executa o main.py
        os.execv(sys.executable, [sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Servidor parado")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        return False

    return True

def main():
    """Função principal"""
    print("🎯 SETUP AUTOMÁTICO - osu!droid RX Server")
    print("=" * 50)

    steps = [
        ("Instalando Rust", install_rust),
        ("Instalando dependências", install_dependencies),
        ("Configurando banco", setup_database),
        ("Criando .env", create_env_file),
    ]

    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        if not step_func():
            print(f"❌ Falha em: {step_name}")
            print("🔧 Verifique os logs acima e tente novamente")
            sys.exit(1)

    print("\n✅ Setup completo!")
    print("🎮 Iniciar servidor agora? (s/N): ", end="")

    if input().lower().strip() in ['s', 'sim', 'y', 'yes']:
        start_server()
    else:
        print("ℹ️  Para iniciar depois: python main.py")
        print("ℹ️  Ou use: python setup.py (vai direto pro servidor)")

if __name__ == "__main__":
    # Se for chamado com argumentos, vai direto pro servidor
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        start_server()
    else:
        main()
