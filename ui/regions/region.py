class Region() :
    def __init__(self, x,y,w,h) :
        self.region = (x,y,w,h)

class TitledRegion(Region) :
    def __init__(self, x,y,w,h, title):
        super(Region, self).__init__(x,y,w,h)
        self.title = title

class TitledRegionGroupSequence() :
    colors = ["black", "red", "blue", "green", "orange", "purple", "brown"]
    def __init__(self, *titles):
        self.region_groups = [[] for _ in range(len(titles))]
        self.index = 0
        self.titles = list(titles)
        self.nb_groups = len(self.titles)

    def getColor(self) :
        return self.colors[self.getGroupIndex()]

    def addRegion(self, region) :
        region = (region[0], region[1], region[2], region[3])
        self.region_groups[self.index].append(region)

    def removeLast(self) :
        if len(self.region_groups[self.index]) > 0 :
            self.region_groups[self.index].pop()
            return True
        elif self.index > 0 :
            self.index-=1
            return False

    def getIndex(self) :
        return len(self.region_groups[self.index])

    def getGroupIndex(self) :
        return self.index

    def nextRegionGroup(self):
        if self.index < self.nb_groups-1 :
            self.index+=1
            return False
        else :
            return True

    def lastRegionGroup(self):
        if self.index > 0 :
            self.index-=1

    def getTitle(self):
        return self.titles[self.index]

def getRegionsTitles():
    bases = ["Valeur et couleur de chaque carte du flop (3)",
             "Valeur et couleur du turn (1)",
             "Valeur et couleur de la river (1)",
             "Chaque joueur adverse (2-10)",
             "Valeur et couleur de chacune de vos cartes (2)",
             "Valeur du pot total et mise"]
    return bases