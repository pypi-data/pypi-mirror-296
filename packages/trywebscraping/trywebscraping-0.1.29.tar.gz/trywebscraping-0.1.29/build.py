import re
import subprocess
import sys
import os

def bump_version(version):
    major, minor, patch = map(int, version.split('.'))
    
    if patch < 99:
        patch += 1
    elif minor < 9:
        minor += 1
        patch = 0
    elif major < 9:
        major += 1
        minor = 0
        patch = 0
    else:
        print("Version limit reached: 9.9.99")
        sys.exit(1)
    
    return f"{major}.{minor}.{patch}"

def update_file(file_path, current_version, new_version):
    with open(file_path, 'r') as file:
        content = file.read()
    
    updated_content = content.replace(current_version, new_version)
    
    with open(file_path, 'w') as file:
        file.write(updated_content)

def get_current_version():
    with open('Cargo.toml', 'r') as file:
        content = file.read()
    
    match = re.search(r'version\s*=\s*"(\d+\.\d+\.\d+)"', content)
    if match:
        return match.group(1)
    else:
        print("Couldn't find version in Cargo.toml")
        sys.exit(1)

def main():
    current_version = get_current_version()
    new_version = bump_version(current_version)
    
    print(f"Bumping version from {current_version} to {new_version}")
    
    update_file('Cargo.toml', current_version, new_version)
    update_file('pyproject.toml', current_version, new_version)
    
    print("Building project...")
    
    # Use cibuildwheel to build wheels for multiple Python versions and OSes
    subprocess.run(["pip", "install", "cibuildwheel"], check=True)
    subprocess.run(["cibuildwheel", "--output-dir", "wheelhouse"], check=True)
    
    print("Uploading to PyPI...")
    subprocess.run(["twine", "upload", "--skip-existing", "wheelhouse/*"], check=True)
    
    print("Build and upload complete!")

if __name__ == "__main__":
    main()