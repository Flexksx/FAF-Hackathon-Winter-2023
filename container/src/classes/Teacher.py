class Teacher:
    def __init__(self, _id:int,_name:str,_subject:int, _type:str, _days:list) -> None:
        self.id:int= _id
        self.name:str = _name
        self.subject:int = _subject
        self.type:str = _type
        self.days:list = _days
