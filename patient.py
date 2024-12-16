class Patient:
    def setPriority(self, priority):
        self.priority = priority

    def getPriority(self):
        return self.priority

    def setToken(self, token):
        self.token = token
    
    def getToken(self):
        return self.token

    def setPatientNo(self, number):
        self.number = number
    
    def getPatientNo(self):
        return self.number

    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name
    
    def setAge(self, age):
        self.age = age

    def getAge(self):
        return self.age
    
    def setSex(self, sex):
        self.sex = sex

    def getSex(self):
        return self.sex
    
    def setBlood(self, blood):
        self.blood = blood

    def getBlood(self):
        return self.blood
    
    def getInfo(self):
        return f"Token: {self.token}\nPatient Number: {self.number}\nName: {self.name}\nAge: {self.age}\nSex: {self.sex}\nBlood Type: {self.blood}"

    def __str__(self):
        return f"{self.token},{self.number},{self.priority}"