import datetime


class Members(object):
    memberId: int
    name: str
    password: str 
    email: str
    role: int

    def __init__(self, memberId, name, password, email, role=1) -> None:
        self.memberId = memberId
        self.name = name
        self.password = password
        self.email = email
        self.role = role
        
