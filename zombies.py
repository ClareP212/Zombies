# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 13:24:46 2019

@author: gy15cep
Student number 200931617
"""


#importing libraries
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot
import matplotlib.animation 
import tkinter
import agentframework

#define number of iterations and neighbourhood size
num_of_iterations = 1000
neighbourhood = 20 #single number variable defining the distance in which agents can run the share_with_neighbour function.

def setup(): 
    """
    Function which defined the number of humans and zombies based on the GUI,
    initialises agents and feeds in the relevant lists and variables to the agentframework module

    Returns:
        prints number of humans and number of zombies selected
    """
    global num_of_humans
    num_of_humans = humanscale.get() #global variable defining the number of humans, updated from GUI humans slider.
    print ("Number of Humans = " + str(num_of_humans))
    global num_of_zombies 
    num_of_zombies = zombiescale.get() #global variable defining the number of zombies, updated from GUI zombie slider.
    print ("Number of zombies = " + str(num_of_zombies))  
    
    #create agent lists, declate as global variables
    global zombies
    zombies = [] #list, then populated using the wolf class of agent framework.
    global humans
    humans = [] #list, then populated using the humans class of agent framework.
    
    #initialise agents, feeding in relevant variables (e.g. html x and y, environment) to the humans and wolf classes
    #creates lists of agents with variables defined in agentframework module
    for i in range(num_of_humans):
        humans.append(agentframework.Human(zombies, humans, neighbourhood))
        
    for i in range(num_of_zombies): 
        create_zombie()

def create_zombie():
    zombies.append(agentframework.Zombie(humans))


carry_on = True
def update(frame_number):
    """
    Function to run agent behaviours, and plot the enviornment and humans and wolf agents onto animation,
    for the number of iterations defined by the generator function (gen_function).
    
    Params:
        frame_number - number of iteratations the model will run for, as defined by the generator function (gen_function).
    """
    fig.clear() #clear the figure for every frame/update of the animation

    #uncomment below to check the number of frames/iterations run
    #print(frame_number)
    global carry_on  #boolean toggle for the generator function.
    #plot environment and fix x and y axis limits
    matplotlib.pyplot.xlim([0,300]) 
    matplotlib.pyplot.ylim([300,0])
    
    ##Agent behaviours
    
    #Wolf behaviours
    #wolf agent list populated by wolf class in agentframework
    for i in range(len(zombies)): 
            zombies[i].chase()
            zombies[i].eat()
            #if there are no more humans, stop the model via the generator function
            if len(humans) == 0:
                carry_on = False
                print("Stopping condition: All humans have been eaten! :o")
                break
            
    #humans behaviours
    #humans agent list populated by humans class in agentframework. 
    for i in range(len(humans)): 
            humans[i].move()
    
    #plot agents on GUI graph/animation        
    for i in range(len(humans)):
        matplotlib.pyplot.scatter(humans[i].x,humans[i].y, c='Pink', edgecolors='black') #humans are white circles with black outline
    for i in range(len(zombies)):
        matplotlib.pyplot.scatter(zombies[i].x,zombies[i].y, c='Green', edgecolors='black') # zombies are black circle


def gen_function():
    """
    Function to keep running the model as long as the stopping conditions are not met.
    Stopping conditions are:
        maxiumum number of interatison reached OR
        there are no humans left (zombies have eaten them all)
    """
    a = 0
    global carry_on 
    while (a < num_of_iterations) & (carry_on) : #keep going as long as carry on = true (there are still humans) and we still have iterations to go
        yield a			
        a = a + 1            
     
###GUI
#set figure size
fig = matplotlib.pyplot.figure(figsize=(5, 5))
ax = fig.add_axes([0, 0, 1, 1])
 
##GUI functions
def run():
    """
    Function to run the model (agent behaviours) and animation       
    """
    animation = matplotlib.animation.FuncAnimation(fig, update, repeat=False, frames=gen_function)
    canvas.draw()
#on stop function call, close the animation window
def stop():
    """
    Function to top the model running and close the model window
    """
    root.destroy()

#build main GUI window
root = tkinter.Tk() # build main window
root.wm_title("Model") # set title
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

#GUI slider bars
humanscale = tkinter.Scale(root, label = "Number of Humans", from_=1, to=100, orient = 'horizontal')
humanscale.pack()
zombiescale = tkinter.Scale(root, label = "Number of Zombies", from_=1, to=5, orient = 'horizontal')
zombiescale.pack()

#GUI menu bar
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run) 
model_menu.add_command(label="Stop model", command=stop) 

#GUI buttons
confirm_setup = tkinter.Button(root,text="Confirm Setup",fg="red", command=setup)
confirm_setup.pack(padx=5, pady=20,side='left')
run_butt = tkinter.Button(root,text="RUN",fg="red", command=run)
run_butt.pack(padx=5, pady=10,side='left')
run_butt = tkinter.Button(root,text="QUIT",fg="red", command=stop)
run_butt.pack(padx=5, pady=0,side='left')

#keep animation window running
tkinter.mainloop()


"""
https://www.informs-sim.org/wsc18papers/includes/files/020.pdf
Step 1.  Model Purpose and Value-added of Agent-based Modeling: 
    We seek to understand what the outcome of a zombie invasion could be.
    How many people will be turned into zombies and ow fast will this occur?
    What intervention could quell the outbreak and prevent the zombies from taking over?
    Agent-based modeling can uniquely consider the spatial location of individual agents and  zombies, 
    and  well  as  consider  individual  characteristics  of  humans  to  defend  themselves against a zombie attack,
    as well as the abilities of individual zombies, and their natural diversity of zombies to overcome humans.
    
Step 2.  All About Agents:  The agents in the model should be humans and zombies.
    Note as an added complication for the model, the identities of the agents are not fixed,
    humans can be turned into zombies.  
    
Step 3.  Agent Data:  The zombie genre of movies and literature provides a rich source of
    possible zombie behaviors and characteristics.  For example, some zombie movies feature slow zombies,
    others fast zombies.  Development of valid zombie models could entail watching many zombie movies and
    shows and categorizing zombie behaviors for many different situations, such as George Romers’s movie Night
    of  the  Living  Dead (https://www.imdb.com/title/tt0063350/) and AMC-TV’s series Walking Dead
    (https://www.amc.com/shows/the-walking-dead).
    
Step 4.  Agent Behaviors:  Humans make decisions consisting of where to move to at any given time,
    and whether to fight or flee when encountering a zombie.  Zombies also has behaviors consisting of where
    to go next in search of humans.  We assume that zombies always attack when confronting a human.
    Technically, this is a behavior that could be altered in the model.  Behaviors for humans could come from
    imagining what one would do in certain situations when encountering or avoiding zombies.  We might want to
    consider alternate schemes for human behavior and see which one works best and under what circumstances.
    
Step 5.  Agent Interactions:  Humans and zombies interact when co-located.  Humans and zombies visually see and
    recognize each other.  If a zombie successfully bites a human, the human turns into a zombie after a transition
    period.  On the other hand, a human may flee from a zombie or kill a zombie to avoid being bitten.
    
Step 6.  Agent States:  A critical piece of information or the model is the state of the agents.  Humans are in
    normal, transition to zombie, or dead state.  Zombies are in normal or dead states.
    
Step 7.  Agent Recap:  We consider some interventions designed to change the outcome of human-zombie encounters. 
    Specifically, we consider the effects of better pre-training to increase the odds
"""









