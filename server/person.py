class Person:
    def __init__(self, addr, client) -> None:
        self.addr = addr
        self.client = client
    
    def __repr__(self) -> str:
        return f"Person({self.addr}, {self.name})"
    
    def set_name(self, name) -> None:
        self.name = name