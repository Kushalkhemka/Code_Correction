#!/usr/bin/env python3
import os
from pathlib import Path
from dotenv import load_dotenv

print(f"Current directory: {os.getcwd()}")
print(f"Script directory: {Path(__file__).parent}")

env_files = [
    Path(".env"),
    Path("../.env"),
    Path(__file__).parent / ".env",
    Path(__file__).parent.parent / ".env"
]

print("\nChecking for .env files:")
for env_file in env_files:
    if env_file.exists():
        print(f"✓ Found: {env_file.absolute()}")
        try:
            with open(env_file, 'r') as f:
                content = f.read().strip()
                if 'OPENAI_API_KEY' in content:
                    lines = content.split('\n')
                    for line in lines:
                        if line.startswith('OPENAI_API_KEY='):
                            key_value = line.split('=', 1)[1]
                            if len(key_value) > 10:
                                print(f"    {line.split('=')[0]}={key_value[:10]}...{key_value[-4:]}")
                            else:
                                print(f"    {line}")
        except Exception as e:
            print(f"    Error reading: {e}")
    else:
        print(f"✗ Not found: {env_file.absolute()}")

project_env = Path(__file__).parent / ".env"
print(f"\nLoading from: {project_env.absolute()}")
load_dotenv(project_env)

api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print(f"✓ API key loaded: {api_key[:10]}...{api_key[-4:]} (length: {len(api_key)})")
    
    try:
        import openai
        print("✓ OpenAI library imported successfully")
        
        client = openai.OpenAI(api_key=api_key)
        print("✓ OpenAI client created successfully")
        
    except Exception as e:
        print(f"✗ Error with OpenAI: {e}")
        
else:
    print("✗ API key not found in environment variables")
    print("Available environment variables containing 'API' or 'OPENAI':")
    for key in os.environ.keys():
        if 'openai' in key.lower() or 'api' in key.lower():
            print(f"  - {key}: {os.environ[key][:10]}...")

print("\nEnvironment variable OPENAI_API_KEY:")
print(f"Value: {repr(os.getenv('OPENAI_API_KEY'))}")
