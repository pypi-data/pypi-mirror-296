from pathlib import Path

class ResourceManager:
    """
    A class to manage assets in the resources folder.
    Works locally and if installed.
    """
    def __init__(self, asset_folder: str):
        self.asset_dir = self._get_resource_path() / asset_folder
        
    def list(self):
        return [p.name for p in self.asset_dir.iterdir()]
    
    def get(self, asset_name: str):
        with open(self.asset_dir / asset_name, 'r') as f:
            return f.read()
        
    def update(self, asset_name: str, content: str):
        with open(self.asset_dir / asset_name, 'w') as f:
            f.write(content)

    def create(self, asset_name: str, content: str):
        if (self.asset_dir / asset_name).exists():
            raise FileExistsError(f"File {asset_name} already exists")
        with open(self.asset_dir / asset_name, 'w') as f:
            f.write(content)
    
    def delete(self, asset_name: str):
        (self.asset_dir / asset_name).unlink()
        
    def _get_resource_path(self) -> Path:
        base_dir = Path(__file__).parent.parent
        resource_dir = base_dir / "resources"
        return resource_dir
