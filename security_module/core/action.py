class Action(dict):
    def __init__(self, name: str, description: str):
        dict.__init__(self, name=name, description=description)
