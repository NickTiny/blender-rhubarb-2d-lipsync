import os
import requests
import shutil
import zipfile
import re
import glob


def download_latest_rhubarb_releases(bin_folder="bin"):
    """
    Downloads all assets from the latest stable release of Rhubarb Lip Sync
    and saves them into the specified bin folder.
    Skips downloading if the zip files already exist and match the latest release.
    """
    api_url = (
        "https://api.github.com/repos/DanielSWolf/rhubarb-lip-sync/releases/latest"
    )
    response = requests.get(api_url)
    response.raise_for_status()
    release = response.json()

    # Ensure bin folder exists
    os.makedirs(bin_folder, exist_ok=True)

    # Get set of zip names already in bin_folder
    existing_zips = set(f for f in os.listdir(bin_folder) if f.endswith(".zip"))

    # Get set of zip asset names in latest release
    latest_zip_assets = set(
        asset["name"]
        for asset in release.get("assets", [])
        if asset["name"].endswith(".zip")
    )

    # If all latest zips are present, skip downloading
    if latest_zip_assets.issubset(existing_zips):
        print(
            "All latest Rhubarb zip assets already present in bin folder. Skipping download."
        )
        return

    for asset in release.get("assets", []):
        asset_name = asset["name"]
        download_url = asset["browser_download_url"]
        if asset_name.endswith(".zip"):
            dest_path = os.path.join(bin_folder, asset_name)
            if os.path.exists(dest_path):
                print(f"{asset_name} already exists, skipping download.")
                continue
            print(f"Downloading {asset_name}...")
            asset_response = requests.get(download_url, stream=True)
            asset_response.raise_for_status()
            with open(dest_path, "wb") as f:
                for chunk in asset_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Saved to {dest_path}")


def prepare_bin_folder(bin_folder="bin"):
    if os.path.exists(bin_folder):
        for filename in os.listdir(bin_folder):
            if filename.endswith(".zip"):
                continue  # Skip zip files
            file_path = os.path.join(bin_folder, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    else:
        os.makedirs(bin_folder, exist_ok=True)


def unzip_rhubarb_zips(bin_folder="bin"):
    # Unzip all zip files into bin_folder
    for filename in os.listdir(bin_folder):
        if filename.endswith(".zip"):
            zip_path = os.path.join(bin_folder, filename)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(bin_folder)
            print(f"Unzipped {filename} into {bin_folder}")

    # Reset permissions for all files and folders in bin_folder
    for root, dirs, files in os.walk(bin_folder):
        for d in dirs:
            dir_path = os.path.join(root, d)
            os.chmod(dir_path, 0o777)
        for f in files:
            file_path = os.path.join(root, f)
            os.chmod(file_path, 0o777)

    # Rename extracted folders to 'windows', 'mac', or 'linux'
    for entry in os.listdir(bin_folder):
        entry_path = os.path.join(bin_folder, entry)
        if os.path.isdir(entry_path):
            lower_entry = entry.lower()
            if "windows" in lower_entry:
                new_name = "windows"
            elif "mac" in lower_entry or "osx" in lower_entry:
                new_name = "mac"
            elif "linux" in lower_entry:
                new_name = "linux"
            else:
                continue  # Skip folders that don't match
            new_path = os.path.join(bin_folder, new_name)
            os.rename(entry_path, new_path)
            print(f"Renamed {entry} to {new_name}")


def get_version():
    """Extract version from __init__.py"""
    with open("__init__.py", "r") as f:
        content = f.read()
        match = re.search(r'__version__ = ["\']([0-9\.]+)["\']', content)
        if match:
            return match.group(1)
    raise ValueError("Could not find version in __init__.py")


def create_distribution_packages():
    """Create distribution packages similar to package.sh"""
    version = get_version()
    dist_folder = "dist"

    # Clean and create dist folder
    if os.path.exists(dist_folder):
        shutil.rmtree(dist_folder)

    # Create directory structure
    os.makedirs(dist_folder)
    os.makedirs(os.path.join(dist_folder, "linux"))
    os.makedirs(os.path.join(dist_folder, "windows"))
    os.makedirs(os.path.join(dist_folder, "osx"))

    # Create blender addon folders
    linux_addon = os.path.join(dist_folder, "linux", "blender-rhubarb-lipsync")
    windows_addon = os.path.join(dist_folder, "windows", "blender-rhubarb-lipsync")
    osx_addon = os.path.join(dist_folder, "osx", "blender-rhubarb-lipsync")

    os.makedirs(linux_addon)
    os.makedirs(windows_addon)
    os.makedirs(osx_addon)

    # Copy Python files to each addon folder
    python_files = glob.glob("*.py")
    for py_file in python_files:
        if py_file != "package.py":  # Don't include the packaging script
            shutil.copy2(py_file, linux_addon)
            shutil.copy2(py_file, windows_addon)
            shutil.copy2(py_file, osx_addon)
            print(f"Copied {py_file} to all addon folders")

    # Copy OS-specific bin folders
    bin_folder = "bin"
    if os.path.exists(bin_folder):
        # Copy linux bin
        linux_bin_src = os.path.join(bin_folder, "linux")
        if os.path.exists(linux_bin_src):
            linux_bin_dest = os.path.join(linux_addon, "bin")
            shutil.copytree(linux_bin_src, linux_bin_dest)
            print(f"Copied linux bin to {linux_bin_dest}")

        # Copy windows bin
        windows_bin_src = os.path.join(bin_folder, "windows")
        if os.path.exists(windows_bin_src):
            windows_bin_dest = os.path.join(windows_addon, "bin")
            shutil.copytree(windows_bin_src, windows_bin_dest)
            print(f"Copied windows bin to {windows_bin_dest}")

        # Copy mac bin
        mac_bin_src = os.path.join(bin_folder, "mac")
        if os.path.exists(mac_bin_src):
            osx_bin_dest = os.path.join(osx_addon, "bin")
            shutil.copytree(mac_bin_src, osx_bin_dest)
            print(f"Copied mac bin to {osx_bin_dest}")

    # Create zip files
    original_dir = os.getcwd()

    try:
        # Linux zip
        os.chdir(os.path.join(dist_folder, "linux"))
        linux_zip = f"../blender-rhubarb-lipsync-linux-{version}.zip"
        with zipfile.ZipFile(linux_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk("blender-rhubarb-lipsync"):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path)
        print(f"Created {linux_zip}")

        # Windows zip
        os.chdir(original_dir)
        os.chdir(os.path.join(dist_folder, "windows"))
        windows_zip = f"../blender-rhubarb-lipsync-windows-{version}.zip"
        with zipfile.ZipFile(windows_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk("blender-rhubarb-lipsync"):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path)
        print(f"Created {windows_zip}")

        # OSX zip
        os.chdir(original_dir)
        os.chdir(os.path.join(dist_folder, "osx"))
        osx_zip = f"../blender-rhubarb-lipsync-osx-{version}.zip"
        with zipfile.ZipFile(osx_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk("blender-rhubarb-lipsync"):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path)
        print(f"Created {osx_zip}")

    finally:
        os.chdir(original_dir)

    print(f"Distribution packages created in {dist_folder} folder")


if __name__ == "__main__":
    prepare_bin_folder()
    download_latest_rhubarb_releases()
    unzip_rhubarb_zips()
    create_distribution_packages()
