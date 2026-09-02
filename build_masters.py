import os
import sys
import subprocess

ALLME_FILE = "allme.py"
SPEC_FILE = "Allme_v33.spec"

def build(exe_name, enable_dashboard):
    print(f"--- Building {exe_name} (Dashboard: {enable_dashboard}) ---")
    
    # 1. Modify allme.py to toggle ENABLE_DASHBOARD_BUILD
    with open(ALLME_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if enable_dashboard:
        content = content.replace("ENABLE_DASHBOARD_BUILD = False", "ENABLE_DASHBOARD_BUILD = True")
    else:
        content = content.replace("ENABLE_DASHBOARD_BUILD = True", "ENABLE_DASHBOARD_BUILD = False")
        
    with open(ALLME_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    # 2. Modify Spec File for the exe name
    with open(SPEC_FILE, 'r', encoding='utf-8') as f:
        spec_content = f.read()
        
    # Standardize replace (in case it was left as something else)
    spec_content = spec_content.replace("name='Allme_v33'", f"name='{exe_name}'")
    spec_content = spec_content.replace("name='AllMeD_v33'", f"name='{exe_name}'")
    
    # Also adjust the output folder to keep them separated or together
    
    temp_spec = f"{exe_name}.spec"
    with open(temp_spec, 'w', encoding='utf-8') as f:
        f.write(spec_content)
        
    # 3. Run PyInstaller
    if sys.platform == 'darwin':
        print(f"Running pyinstaller --windowed on macOS for {exe_name}...")
        subprocess.run(["pyinstaller", "--windowed", "-n", exe_name, "-y", ALLME_FILE])
    else:
        print(f"Running pyinstaller {temp_spec}...")
        subprocess.run(["pyinstaller", "-y", temp_spec])
    print(f"Finished {exe_name}.\n")

if __name__ == "__main__":
    # Create the v36 base spec from v35
    if sys.platform != 'darwin' and not os.path.exists("Allme_v36.spec"):
        with open("Allme_v35.spec", "r", encoding="utf-8") as f:
            c = f.read().replace("Allme_v35", "Allme_v36")
        with open("Allme_v36.spec", "w", encoding="utf-8") as f:
            f.write(c)

    # Build the non-dashboard master
    build("Allme_v36", False)
    
    # Build the dashboard master
    build("AllMeD_v36", True)
    
    print("Done! Check the /dist folder for both executables.")
