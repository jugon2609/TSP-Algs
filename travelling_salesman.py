import random as rand
import copy
import time
class Route:
    def __init__(self, l):
        ''' l is a list of Cities (ordered)'''
        self.route = l
        self.length = len(l)

    def score(self):
        ret = 0
        for x in range(self.length):
            if x == self.length - 1:
                ret += distance(self.route[0], self.route[x])
            else:
                ret += distance(self.route[x] , self.route[x+1])
        return ret
    
    def mutate(self):
        rate = rand.randint(0,4)
        mutts = []
        n = int(rate*self.length/100)
        for i in range(n):
            mutts.append(rand.choice(range(self.length)))
        #mutation
        for mutt in mutts:
            swap = rand.choice([1,1,1,2,2,3,-1,-1,-1,-2,-2,-3])
            if mutt + swap >= 0 and mutt + swap < self.length:
                self.route[mutt], self.route[mutt+swap] = self.route[mutt + swap], self.route[mutt]

    def cop(self):
        copyroute = copy.deepcopy(self.route)
        cop = Route(copyroute)
        return cop

    def random_copy(self):
        indexes = [i for i in range(self.length)]
        newroute = []
        while indexes:
            choice = rand.choice(indexes)
            indexes.remove(choice)
            newroute.append(self.route[choice])
        return Route(newroute)

    def load_file(self, file):
        coords = []
        with open(file) as f:
            for i in f:
                i = i.strip()
                i = i.split(',')
                x = float(i[0])
                y = float(i[1])
                coords.append((x,y))
        self.route = coords
        self.length = len(coords)


    def export_file(self, filename):
        filename = f"{filename}_{round(self.total_score())}.txt"
        with open(filename, 'w') as f:
            for i in self.route:
                f.write(f"{i[0]},{i[1]}")

    
def distance(city1, other):
    d = ((city1[0] - other[0])**2 + (city1[1] - other[1])**2) ** (1/2)
    return d

def crossover(mother, father):
    E = set()
    newroute = []
    i=0
    while len(E) != mother[1].length:
        flag = True
        p = rand.choice(['M', 'F'])
        #print(f' len = {len(E)}')
        if p == 'M':
            x = i
            while flag:
                #print(x, i)
                if str(mother[1].route[x]) not in E:
                    newroute.append(mother[1].route[x])
                    E.add(str(mother[1].route[x]))
                    flag = False
                
                if x == mother[1].length - 1:
                    x=-1
                x += 1
                    
        if p == 'F':
            x = i
            while flag:
                if str(father[1].route[x]) not in E:
                    newroute.append(father[1].route[x])
                    E.add(str(father[1].route[x]))
                    flag = False
                if x == mother[1].length - 1:
                    x=-1
                x += 1
        if i == mother[1].length -1:
            i = -1
        i += 1
        #print(i)
    child = Route(newroute)
    #print(child)
    return child

def two_point_appender(childroute, E, parentroute, endpoint):
    posx = len(childroute)
    negx = len(childroute)
    while len(childroute) < endpoint:
        if parentroute[posx] not in E:
            E.add(parentroute[posx])
            childroute.append(parentroute[posx])
            if posx < len(parentroute) -1 :
                posx+=1
            else:
                posx = 0
        else:
            if posx < len(parentroute) - 1:
                posx+=1
            else:
                posx = 0
        if parentroute[negx] not in E:
            E.add(parentroute[negx])
            childroute.append(parentroute[negx])
            if negx  > 0:
                negx -=1
            else:
                negx = len(parentroute) -1
        else:
            if -1* negx  < 0:
                negx -=1
            else:
                negx = len(parentroute) -1
    return (childroute, E)

def two_point(mother, father):
    point1 = rand.choice(range(mother[1].length - 2))
    point2 = rand.choice(range(point1, mother[1].length - 1))
    p = rand.choice(['M', 'F']) 
    childroute = []
    E = set()
    if p == 'M':
        childroute , E = two_point_appender(childroute, E, mother[1].route, point1)
        childroute , E = two_point_appender(childroute, E, father[1].route, point2)
        childroute , E = two_point_appender(childroute, E, mother[1].route, len(mother[1].route))
    if p == 'F':
        childroute , E = two_point_appender(childroute, E, father[1].route, point1)
        childroute , E = two_point_appender(childroute, E, mother[1].route, point2)
        childroute , E = two_point_appender(childroute, E, father[1].route, len(mother[1].route))
    child = Route(childroute)
    return child

def roulette_selection(pop):
    parent1 = rand.choices([i for i in range(0,len(pop))], weights = [i for i in range(len(pop), 0 , -1)], k=1)
    parent2 = rand.choices([i for i in range(0,len(pop))], weights = [i for i in range(len(pop), 0, -1)], k=1)
    father = pop[parent1[0]]
    mother = pop[parent2[0]]
    return (mother, father)

def export_graph(bests, mutation, genetype, selectiontype, name):
    ret =  open(name, 'w') 
    ret.write(f"{mutation}, {genetype}, {selectiontype}")
    for time, score in bests:
        ret.write('\n')
        ret.write(f"{time, score}")
    ret.close()

def export_evo(evolist, filename):
    ret = open(filename, 'w')
    for route in evolist:
        for city in route:
            ret.write(f"{city[0]},{city[1]};")
        ret.write('\n')
    ret.close()

def hill_climb(routee):
    for i in range(routee.length):
        for x in range(routee.length):
            ogscore = routee.score()
            routee.route[i], routee.route[x] = routee.route[x], routee.route[i]
            if ogscore < routee.score():
                routee.route[i], routee.route[x] = routee.route[x], routee.route[i]
    return routee

#population generation
luca = Route([])
luca.load_file('cities1.txt')
print(luca.route)
pop = []
for i in range(200):
    new = luca.random_copy()
    scor = new.score()
    pop.append((scor, new))

#genetic 

gen = 0 
start = time.time()
bests = [float('inf')]
bestss = []
evo = []
while time.time() - start < 600:
    newpop = []
    pop.sort(key = lambda x:x[0])
    bests.append(pop[0][0])
    if bests[-1] < bests[-2]:
        evo.append(pop[0][1].route)
        bestss.append((bests[-1], time.time() - start))
    if gen%10 == 0:
        print(gen , pop[0][0])
    possbest = pop[0][1].cop()
    possbest.mutate()
    #if bests[-1] < bests[-2]:
        #possbest = hill_climb(possbest)
    if possbest.score() < pop[0][0]:
        newpop.append((possbest.score(), possbest))
    else:
        newpop.append((pop[0]))
    for i in range(1, len(pop)):
        mother, father = roulette_selection(pop)
        new = two_point(mother, father)
        new.mutate()
        #mut = rand.choices([True, False], weights= [1, 200], k=1)
        if gen == 1000:
            new = hill_climb(new)
            new = hill_climb(new)
        newpop.append((new.score(), new))
    pop = newpop
    gen += 1
print('done')
export_evo(evo, 'route_evolution120.txt')
export_graph(bestss, '2', 'crossover + 1/200 2xhillclimb', 'roulette', 'cities1_7.txt')
        
    