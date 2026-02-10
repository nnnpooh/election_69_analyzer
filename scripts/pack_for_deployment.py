import os
import shutil
from pathlib import Path

def pack_site():
    # Define paths
    root_dir = Path(__file__).parent.parent
    docs_dir = root_dir / "docs"
    data_dir = root_dir / "data"
    
    # Files to copy from data/ to docs/data/
    # Note: Stats files are now generated directly to docs/data/
    # This list is now empty or reserved for static assets in data/ root if any
    data_files = []
    
    # Ensure docs directory exists
    if not docs_dir.exists():
        docs_dir.mkdir()
    
    # Copy data files
    docs_data_dir = docs_dir / "data"
    if not docs_data_dir.exists():
        docs_data_dir.mkdir()
        
    for filename in data_files:
        src = data_dir / filename
        dst = docs_data_dir / filename
        if src.exists():
            shutil.copy2(src, dst)
            print(f"✅ Copied {filename} to {docs_data_dir}/")
        else:
            print(f"⚠️  Warning: Source file {src} not found")

    # Create .nojekyll
    (docs_dir / ".nojekyll").touch()
    print(f"✅ Created .nojekyll")
    
    print("\n📦 Site updated in 'docs/' folder!")

if __name__ == "__main__":
    pack_site()
