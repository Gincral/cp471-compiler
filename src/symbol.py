
class SymbolTable:
    def __int__(self):
        self.dataList = []

    def appendData(self, data):
        self.append(data)

    def searchData(self, name):
        for data in self.dataList:
            if data.name == name: return data
        return None
    
    def updateDataValue(self, name, value):
        for data in self.dataList:
            if data.name == name: 
                data.value = value
                return data
        return None
    

class Data:
    def __int__(self, name, type, value, location):
        self.name = name
        self.type = type
        self.value = value
        self.location = location
