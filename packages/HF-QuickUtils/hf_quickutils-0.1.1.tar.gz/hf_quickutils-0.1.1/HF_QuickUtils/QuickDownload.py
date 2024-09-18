import os
from huggingface_hub import snapshot_download

class QuickDownload:
    def __init__(self, repo, local="", name=""):
        if name == "":
            self.modelName = repo
        else:
            self.modelName = name
        self.repo = repo
        if local=="":
            self.local = os.environ["HF_HOME"] + "\\" + repo
        else:
            self.local = local

    def download(self, max_workers=8) -> str:
        print("Waiting for download...")
        snapshot_download(
            repo_id=self.repo,
            local_dir=self.local,
            max_workers=max_workers
        )
        return self.local

