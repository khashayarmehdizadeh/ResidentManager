#class resident

class Resident:
    def __init__(self,id,first_name,last_name,num_people,floor,unit,phone,mobile):
        self.id=id
        self.first_name=first_name
        self.last_name=last_name
        self.num_people=num_people
        self.floor=floor
        self.unit=unit
        self.phone=phone
        self.mobile=mobile
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.num_people} - {self.floor}, {self.unit}"