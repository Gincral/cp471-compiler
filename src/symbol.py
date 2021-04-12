
class SymbolTable:
    def __init__(self):
        self.dataList = []

    def appendData(self, data):
        self.dataList.append(data)

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

    def printTable(self):
        print("=====================")
        print("Symbol Table: ")
        print("{:10s}{:13s}{:10s}".format("id", "type", "value"))
        for data in self.dataList:
            print("{:10s}{:13s}{:10s}".format(data.name, data.type, data.value))
        print("=====================")
    

class Data:
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value
