#!/usr/bin/env python3
"""
Install dependencies for all microservices for testing.
"""
import subprocess
import sys
from pathlib import Path

def install_requirements(requirements_file):
    """Install requirements from a file."""
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file), "--quiet"
        ], check=True)
        print(f"✅ Installed dependencies from {requirements_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies from {requirements_file}: {e}")
        return False

def main():
    """Install all service dependencies."""
    backend_dir = Path(__file__).parent.parent
    
    # List of services and their requirements files
    services = [
        "orchestrator",
        "analytics", 
        "LLM",
        "rag",
        "sentiment",
        "stt",
        "tts",
        "feedback"
    ]
    
    print("🔧 Installing dependencies for all microservices...")
    
    success_count = 0
    total_count = 0
    
    for service in services:
        service_dir = backend_dir / service
        requirements_file = service_dir / "requirements.txt"
        
        if requirements_file.exists():
            total_count += 1
            if install_requirements(requirements_file):
                success_count += 1
        else:
            print(f"⚠️  No requirements.txt found for {service}")
    
    # Install common requirements
    common_requirements = backend_dir / "requirements-common.txt"
    if common_requirements.exists():
        total_count += 1
        if install_requirements(common_requirements):
            success_count += 1
    
    print(f"\n📊 Summary: {success_count}/{total_count} dependency files installed successfully")
    
    if success_count == total_count:
        print("✅ All dependencies installed successfully!")
        return 0
    else:
        print("⚠️  Some dependencies failed to install")
        return 1

if __name__ == "__main__":
    sys.exit(main())

