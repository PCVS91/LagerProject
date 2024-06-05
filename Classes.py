# Define rack class
import random as rd
class Rack:
    labels = [11,21,22]
    def __init__(self, positions=1, distance=0):
        numbers = list(range(10))
        self.distance=distance
        rd.shuffle(numbers)
        self.positions = positions
        self.codes = {Rack.labels[0]:numbers[0]}
        if positions > 1:
            self.codes[Rack.labels[1]] = (numbers[0]+1) % 10
        if positions > 2:
            self.codes[Rack.labels[2]] = (numbers[0]+2) % 10
    def __str__(self):
        s=''
        for code in self.codes:
            s+= f'Shelf: {code}   Confirmation code: {self.codes[code]}\n'
        return s
    def __len__(self):
        return self.positions
# Define section class. codes cannot be repeated within each section.
class Section:
    
    # Check if codes are repeated
    def check(self):
        codes=[]
        for rack in self.racks:
            codes.extend(list(rack.codes.values()))
        self.good = True if len(set(codes)) == len(codes) else False
        return self.good
        
    # Generate new codes
    def fix(self):
        numbers = list(range(10))
        self.good=False
        while self.good==False:
            for rack in self.racks:
                rd.shuffle(numbers)
                id1=numbers[0]
                rack.codes[Rack.labels[0]] = id1
                if rack.positions > 1:
                    id2=(id1+1) % 10
                    rack.codes[Rack.labels[1]] = id2
                if rack.positions > 2:
                    id3 = (id2 + 1) % 10
                    rack.codes[Rack.labels[2]] = id3
            self.good=self.check()
    def set_distance(self, distance):
        d = 0
        for rack in self.racks:
            rack.distance = 3*distance + d
            d += 1
            
    def __init__(self, racks, distance=0):
        self.racks = []
        for rack in racks:
            self.racks.append(Rack(rack))
        self.check()
        self.ite=1
        self.distance = distance
        self.set_distance(self.distance)
        if not self.check():
            self.fix()


            
    def __str__(self):
        i=1
        s=''
        for rack in self.racks:
            f=f'Distance: {self.distance}\n'
            s+=f'\nRack: {i}' + f'{f:>26}'
            for code in rack.codes:
                s+= f'Shelf: {code}   Confirmation code: {rack.codes[code]}\n'
            i += 1
        return s
        return self.racks
    def __len__(self):
        return sum([len(rack) for rack in self.racks])
# Class Regal. There are 20 racks in each Regal
class Regal:
    def __init__(self, sections,initialDis=0):
    # sections is a list of sections
        self.sections = sections
        self.initialDis=initialDis
        dis=initialDis
        for section in self.sections:
            section.set_distance(dis)
            dis += 1
        self.make_tuples()
    def make_tuples(self):
        self.tuples = {}
        i = 1
        for section in self.sections:
            for rack in section.racks:
                for code in rack.codes:
                    self.tuples[i] = (rack.distance, rack.codes[code])
                    i += 1
    def __str__(self):
      return "\n".join(str(section) for section in self.sections)
    def __len__(self):
        return sum([len(section) for section in self.sections])
    def shuffle(self):
        for section in self.sections:
            section.fix()
        self.make_tuples()

            
# Class Corr. In each regal there are two 'Regals' of 20 racks.
class Corr:
    def __init__(self,regal1, regal2):
        self.regal1=regal1
        self.regal2=regal2
    def shuffle(self):
        regal1.shuffle()
        regal2.shuffle()