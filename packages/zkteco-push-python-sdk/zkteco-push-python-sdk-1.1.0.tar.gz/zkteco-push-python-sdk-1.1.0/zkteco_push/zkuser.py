class ZKUser:
    def __init__(self, user_id, name, password, privilege, faces):
        
        self.user_id = user_id
        self.name = name
        self.password = password
        self.card = None
        self.finger = None
        self.faces = faces
        self.privilege = privilege
        
        
        #TODO #1 implement groups managements
        self.group = 0
        self.timezone = 2
        self.verification_mode = 0