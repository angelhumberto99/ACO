class Graph:
    def __init__(self, directed = False):
        self.__directed = directed
        self.graph = {}

    def Length(self):
        return len(self.graph)

    def IsEdge(self, origin, destiny):
        if self.graph.get(origin, False):
            if self.graph[origin].get(destiny, False):
                return True
            return False
        return False


    def CreateEdge(self, origin, destiny, cost):
        destinies = {}

        if self.__directed:
            if self.graph.get(origin, False):
                destinies = self.graph[origin]
            destinies[destiny] = cost
            self.graph[origin] = destinies

        else:
            o_d = {}
            d_o = {}

            if self.graph.get(origin, False):
                o_d = self.graph[origin]
            
            o_d[destiny] = cost

            if self.graph.get(destiny):
                d_o = self.graph[destiny]
            
            d_o[origin] = cost

            self.graph[origin] = o_d
            self.graph[destiny] = d_o


    def PrintData(self):
        size = len(self.graph)
        i = 0
        keys = list(self.graph.keys())

        for i in range(0, size):
            auxDict = dict(self.graph[keys[i]])
            subKeys = list(auxDict.keys()) 
            subSize = len(auxDict)
            for j in range(0, subSize):
                print("(", keys[i], ",", auxDict[subKeys[j]],
                      ",", subKeys[j], ")")


    def GetCost(self, origin, destiny):
        if not self.IsEdge(origin, destiny):
            print("The edge does not exist")
            return
        return self.graph[origin][destiny]

        
    def GetNeighbors(self, origin):
        if not self.graph.get(origin, False):
            print("The origin doesn't exist")
            return
        return self.graph[origin]


    def Contains(self, origin):
        if self.graph.get(origin, False):
            return True
        return False

    def EraseConnection(self, origin, destiny):
        if self.graph.get(origin, False):
            aux = self.GetNeighbors(origin)
            if aux.get(destiny):
                if not self.__directed:
                    del self.graph[destiny][origin]
                del self.graph[origin][destiny]
            else:
                print("There is not an edge between "
                    , origin, " and ", destiny)
