from transformers import AutoTokenizer, pipeline, AutoModel
from QuickDownload import QuickDownload

class QuickLoader:
    def __init__(self, repo="", local="", maxworkers=8, tokenizer_type=AutoTokenizer, model_type=AutoModel,
                 processor_type=None,device="cpu"):
        if repo != "" and local != "":
            self.local = QuickDownload(repo=repo, local=local).download(maxworkers)
        elif repo != "":
            self.local = QuickDownload(repo=repo).download(maxworkers)
        elif local != "":
            self.local = local
        elif repo=="" and local!="":
            print("Error ")
        self.tokenizer = tokenizer_type.from_pretrained(self.local,device = device)
        self.model = model_type.from_pretrained(self.local,device = device)
        if processor_type is not None:
            self.processor = processor_type.from_pretrained(self.local,device = device)

    def get_model_and_tokenizer(self):
        return self.model, self.tokenizer
    def get_processor(self):
        return self.processor
    def get_pipeline(self, type):
        return pipeline(type, model=self.model, tokenizer=self.tokenizer, image_processor=self.processor)
