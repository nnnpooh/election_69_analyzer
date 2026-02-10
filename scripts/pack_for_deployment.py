import os
import shutil
from pathlib import Path

def pack_site():
    # Define paths
    root_dir = Path(__file__).parent.parent
    docs_dir = root_dir / "docs"
    data_dir = root_dir / "data"
    
    # Files to copy from rawdata/ to docs/data/
    rawdata_files = ["focused-area.json"]
    rawdata_dir = root_dir / "rawdata"
    
    # Ensure docs directory exists
    if not docs_dir.exists():
        docs_dir.mkdir()
    
    # Copy data files
    docs_data_dir = docs_dir / "data"
    if not docs_data_dir.exists():
        docs_data_dir.mkdir()
    
    # Copy from rawdata
    for filename in rawdata_files:
        src = rawdata_dir / filename
        dst = docs_data_dir / filename
        if src.exists():
            shutil.copy2(src, dst)
            print(f"✅ Copied {filename} to {docs_data_dir}/")
        else:
            print(f"⚠️ Source file not found: {src}")

    # Create .nojekyll
    (docs_dir / ".nojekyll").touch()
    print(f"✅ Created .nojekyll")
    
    print("\n📦 Site updated in 'docs/' folder!")

if __name__ == "__main__":
    pack_site()
