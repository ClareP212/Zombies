#import modules
import random

#create agents and define their behaviours
class Agent() :
    def __init__ (self,zombies,humans):
        """
        Function to initiate the agent, sets x, y and store, feeds in environment, humans and zombies lists, neighbourhood from model.
        If there are no more x and y variables to ude form the html, it assigns random ones.
        Params:
            environment - environment list of lists from model.
            zombies - zombie class agent list
            humans - humans class agent list
            neighbourhood - neighbourhood variable from model.
            y - y variable from html in model.
            x - x variable from html in model.
            store - variable representing food storage in agent
        """
        self.y = random.randint(0,299)
        self.x = random.randint(0,299)
        #read in lists
        self.humans = humans
        self.zombies = zombies
        self.strength = random.randint(1,5)
          
    def fence_halt(self):
        """
        Function to act as a fence in moving agents back into area,
        if x and y are out of defined area limits
        
        Params:
            x - x coordinate of agent
            y - y coordinate of agent
        """
        if self.x < 0: self.x = 0
        if self.x > 299: self.x = 299         
        if self.y < 0: self.y = 0
        if self.y > 299: self.y = 299 
         
    def random_move(self):
        """
        Function to move agents randomly
        
        Params:
            x - x coordinate of agent
            y - y coordinate of agent
            move_speed - number x or y changes by each iteration

        """
        if random.random() < 0.5: self.x = (self.x + self.move_speed)
        else: self.x = (self.x - self.move_speed)
        if random.random() < 0.5: self.y = (self.y + self.move_speed)
        else: self.y = (self.y - self.move_speed) 
    
    def move_towards(self):
        """
        Function to move towards specific agent at certain speed
        
        Params:
            closest_agent - list containing [x, y, distance] for closest agent (distance calculated with distance_between function)
            move_speed - number x or y changes by each iteration
        """
        if self.x - self.closest_agent[0] == 0:
            pass
        if self.x - self.closest_agent[0] >= 0:
            self.x = self.x - self.move_speed
        else:
            self.x = self.x + self.move_speed
        if self.y - self.closest_agent[1] == 0:
            pass
        if self.y - self.closest_agent[1] >= 0:
            self.y = self.y - self.move_speed
        else:
            self.y = self.y + self.move_speed 
     
   
    def distance_between(self,a):
        """
        Function to calculate distance between two inputted points, distance based on pythagoras
        
        Params:
            x - x coordinate.
            y - y coordinate.
            a - item inputted into function.
        """
        return (((self.x - a.x)**2) + ((self.y - a.y)**2))**0.5
    
    
class Human(Agent):
    def move (self):
        """
        Function to move humans away from the closest wolf if within sight distance,
        randomly if not
        
        Params:
            zombies - wolf class agent list (containing x and y of each).           
            wolf_dist - list of the x and y coordinates for each wolf and distance between self and each wolf.
            closest_agent - list containing x, y and distance between self and closest wolf.
            move_speed - x and y change with each movement.
        """
        #create a list of all the zombies, calculate distance between self and every wolf, sort the list by distance
        zombie_dist = []
        for i in range(len(self.zombies)):
            distance = self.distance_between(self.zombies[i])
            zombie_dist.append([distance,self.zombies[i].x,self.zombies[i].y],)
        zombie_dist.sort()
        #define closest_agent - first item in wolf_dist list because of sort
        self.closest_agent = [zombie_dist[0][1],zombie_dist[0][2], zombie_dist[0][0]]
        if self.closest_agent[2] < 80:
            self.move_speed = -3
            self.move_towards()
            self.fence_halt()            
        else:
            self.move_speed = 1
            self.random_move()
            self.fence_halt()
           
class Zombie(Agent):
    def __init__ (self,zombies,humans,x,y):
        """
        Function to initiate wolf, sets x, y and store, feeds in humans list from model.
        
        Params:
            environment - environment list of lists from model.
            zombies - wolf list from model.
            humans - humans list from model.
            neighbourhood - neighbourhood variable from model.
            y - y variable from html in model.
            x - x variable from html in model.
        """
        if (y == None): self._y = random.randint(0,49) 
        else: self.y = y
        if (x == None): self._x = random.randint(250,299)
        else: self.x = x
        self.humans = humans
        self.zombies = zombies
        self.type = random.randint(1,3) #1 is crawler, 2 is walker, 3 is runner
        
    def chase(self):
        """
        Function to move zombies towards the closest humans unless store is "full",
        then randomly
        
        Params:
            humans - humans class agent list (containing x and y of each).    
            prey_dist - list of the x and y coordinates for each humans and distance between self and each humans.
            closest_agent - list containing x, y and distance between self and closest humans.
            move_speed - x and y change with each movement.
        """
        human_dist = []
        for i in range(len(self.humans)):
            distance = self.distance_between(self.humans[i])
            human_dist.append([distance,self.humans[i].x,self.humans[i].y],)
        human_dist.sort()
        self.closest_agent = [human_dist[0][1],human_dist[0][2], human_dist[0][0]]  
        self.move_speed = 2 * self.type
        self.move_towards()
        self.fence_halt()
         
            
    def eat(self):
        """
        Function for zombies to 'eat' humans, if humans are within the defined distance
        and the wolf is hungry (store below defined value).
        
        
        Params:
            humans - humans class agent list (containing x and y of each).
            closest_agent - list containing x, y and distance between self and closest humans.
            store - variable representing food storage in agent.
        """
        if len(self.humans) > 0:
            if self.closest_agent[2] < 10: #if distance of closest prey is less than 20
                for human in self.humans: #for every humans in humans list
                    if human.x == self.closest_agent[0] and human.y == self.closest_agent[1]:
                        human_x = human.x
                        human_y = human.y
                        self.zombies.append(Zombie(self.zombies,self.humans,human_x,human_y))
                        self.humans.remove(human)
                        
    def attack(self):
        """
        function for zombies to attack human, and eat if they win
        
        Params:
            humans - humans class agent list (containing x and y of each).
            closest_agent - list containing x, y and distance between self and closest humans.
            store - variable representing food storage in agent.
        """
        if len(self.humans) > 0:
            if self.closest_agent[2] < 10: #if distance of closest prey is less than 10
                for human in self.humans: #for every humans in humans list
                    if human.x == self.closest_agent[0] and human.y == self.closest_agent[1]:
                        pass
                

                        
                        
