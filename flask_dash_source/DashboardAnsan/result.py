from unicodedata import category


import json

class Result :
    def __init__(self,name, category, bbox, score ) :
        self.name = name 
        self.category = category
        self.bbox = bbox
        self.score = score  
    def toJSON(self):
        return json.dumps(self.__dict__)
             