########################################################
# Imports 
# generate random location for all the objects & their velocities 
import random
# math imported which help w/ different functions such as finding distance 
import math

#########################################################
# Classes 
#asteroid object class
class Asteroid:
    #includes x,y coordinate and velocities in horizontal and vertical direction
    def __init__(self, x, y, Size, dx, dy):
        global img1, img2, img3, img4, img5, img6, img
        #randomly generated values using randint 
        self.x = x 
        self.y = y
        #size of asteroid 
        self.Size = Size
        #x,y velocites generated without being 0 
        self.dx = dx
        self.dy = dy
        #import images using random num
        self.num = random.randint(0,5)

        #radius of smaller asteroid 
        if self.Size == 'small':
            self.radius = random.randint(15,20)
        #radius of a large asteroid 
        if self.Size == 'medium':
            self.radius = random.randint(30,40)
        # radius of large asteroid 
        if self.Size == 'large':
            self.radius = random.randint(60,70)
            
    
    def draw(self):
        #image imported 
        global img1, img2, img3, img4, img5, img6
        
        #random image selected
        if self.num == 0:
            img = img1
        if self.num == 1:
            img = img2
        if self.num == 2:
            img = img3
        if self.num == 3:
            img = img4
        if self.num == 4:
            img = img5
        if self.num == 5:
            img = img6
        
        #draw from center
        imageMode(CENTER)
        #asteroid is drawn
        image(img, self.x, self.y, self.radius*2+10,  self.radius*2+10) 
    
    # move asteroid based on velocity subbed in 
    def move(self):
        #change x,y coordinates
        self.x += self.dx
        self.y += self.dy
        
        #if asteroid moves off screen put it at the other side
        if self.x > SCREEN_WIDTH:
            self.x = 0 
        if self.x < 0:
            self.x = SCREEN_WIDTH
            
        if self.y > SCREEN_LENGTH:
            self.y = 0
        if self.y < 0:
            self.y = SCREEN_LENGTH
    
    def collide(self, object):
        #returns distance between both objects 
        distance = find_distance(self, object)
        #checks if overlapping 
        if self.radius + object.radius >= distance:
            #returns bool whether or not an asteroid is colliding with the passed in object
            return True
        #returns false if not colliding 
        return False
    
    def split_asteroid(self):
        #size is smaller.. generate two new asteroid objects w/ same x and y
        if self.Size == "large":
            #splits asteroid in two
            #ensures that broken up asteroids do not overlap each other when broken and are not equal to zero
            while True:
                dx1 = random.randint(-15,15)/10
                dy1 = random.randint(-15,15)/10
                dx2 = random.randint(-15,15)/10
                dy2 = random.randint(-15,15)/10
                if dx1 != 0 and dy1!= 0 and dx2 != 0 and dy2!= 0 and ((dx1 != dx2) or (dy1 != dy2)):
                    break
            #create MEDIUM asteroids moving in different direction 
            for n in [[dx1,dy1],[dx2,dy2]]:
                asteroids_field.append(Asteroid(self.x, self.y,'medium', n[0], n[1]))
         #asteroid is broken into two small pieces        
        if self.Size == "medium":
            #ensures that smaller asteroids do not overlap
            while True:
                dx1 = random.randint(-15,15)/10
                dy1 = random.randint(-15,15)/10
                dx2 = random.randint(-15,15)/10
                dy2 = random.randint(-15,15)/10
                if dx1 != 0 and dy1!= 0 and dx2 != 0 and dy2!= 0 and ((dx1 != dx2) or (dy1 != dy2)):
                    break
            #smaller asteroid created 
            for n in [[dx1,dy1],[dx2,dy2]]:
                asteroids_field.append(Asteroid(self.x, self.y, 'small', n[0], n[1]))
    
    
    #returns size of asteroid and decides whether or not to destroy asteroid or split into smaller 
    def get_asteroidsize(self):
        return self.Size    
   
#ship class that is controlled by the user         
class Ship:
    # initalize start coordinates, speed and current rotation
    def __init__(self): 
        # moved by translation w/ pushMatrix 
        self.x = SCREEN_WIDTH//2
        self.y = SCREEN_LENGTH//2
    
        # default speed and rotation
        self.speed = 0
        
        #make ship facing upwards at start
        self.rotation = -90
        #temp rotation used ONLY for visual rotation & bullets.. does not affect direction determination with trig
        self.temp_rotation = -90
        
        #space dimensions from each side.. used mainly for collision detect
        self.radius = 12
        
        #contains bullets shot in bounds
        self.bullets_field = []
        
        #whehter or not object is thrusting 
        self.thrust = False
    
    def reset(self):
        #reset the ship to the center when it dies 
        self.x = SCREEN_WIDTH//2
        self.y = SCREEN_LENGTH//2
    
        # default speed and rotation
        self.speed = 0
        self.rotation = -90
        self.temp_rotation = -90
        
        #contains bullets shot in bounds
        self.bullets_field = []
        self.thrust = False

    #draw ship into screen
    def draw(self):  
        #move matrix with ship located at origin to point of ship then rotate on origin.. then restore matrix
        pushMatrix()
        translate(self.x, self.y)
        #rotation of physical ship is based on temp_rotation var
        #self.rotation is used w/ other functions such as finding the direction of a bullet, or where to move the ship 
        rotate(radians(self.temp_rotation))
        #white border, black inside 
        stroke(255)
        fill(0)
        #draw shape 
        beginShape()
        vertex(0,0)
        vertex(-26,-11)
        vertex(-20,-4)
        vertex(-20,4)
        vertex(-26,11)
        vertex(0,0)
        endShape()
        #triangle image shown at back when thursting 
        if self.thrust: 
            triangle(-20, 4, -20, -4, -30, 0)
        #reset matrix 
        popMatrix()
        fill(255) 
        
    #ship rotates right if key pressed is right
    def rotate_right(self):
        #if the ship is not accelerating and is turning right.. ie(moving on its own from previous move), only use the temp variable to rotate the ship around.. so that object is affected by inertia
        if self.thrust:
            #if the ship is accelerated and the ship is turning.. adjust self.rotation in case user decides to press UP button so it goes in the correct direction
            self.rotation = self.temp_rotation 
            if self.rotation == 360:
                self.rotation = 0
                temp_rotation = 0
            # rotate right 
            # make sure they are always the same 
            self.rotation+=10
            self.temp_rotation+=10
        else:
            #only temp_rotation is adjusted to show the viusal ship is turning
            self.temp_rotation +=10
    
    # ship rotates left if key is pressed left 
    def rotate_left(self):
        # if reaching -360 degrees.. reset. They are equivalent b/c of RAA
        #only change rotation to change direciton if you are thrusting.. otherwise ship will keep its momentum
        if self.thrust:
            self.rotation = self.temp_rotation
            if self.rotation == -360:
                self.rotation = 0
                self.temp_rotation = 0
            # rotates left
            self.rotation -= 10
            self.temp_rotation -= 10
        else: 
            #temp rotation used for visual rotation and bullets 
            self.temp_rotation -=10
                
    # slow down speed to zero if up key is not pressed
    def move(self):
       # update coordinates based on rotation... trig used here
        #dx and dy are changed only when the thrust is used.. ship will keep its momentum as long as you are not thrusting
        self.x += (cos(radians(self.rotation))*self.speed)
        self.y += (sin(radians(self.rotation))*self.speed)
        
        #over extends boundaries.. resets the location to the other side of the screen
        if self.x > SCREEN_WIDTH:
            self.x = 0
        if self.x < 0:
            self.x = SCREEN_WIDTH
        if self.y > SCREEN_LENGTH:
            self.y = 0 
        if self.y < 0:
            self.y = SCREEN_LENGTH
        
    # slow down speed to zero if up key is not pressed
    def slow_down(self):
        #slows down till reaching velocity of zero
        self.speed -= 0.025
        if self.speed < 0:
            slow = False 
            self.speed = 0
    
    def accelerate(self):
        #the rotation needs to be updated since changes are no longer visual 
        self.rotation = self.temp_rotation 
        #accelerates until reaching velocity of 4
        if self.speed < 4.5: 
            self.speed += 0.6 
            #thrusting is true... used to make sure that object experiences inertia 
            self.thrust = True 
        else:
            #if speed goes slightly over.. set at exactly 4
            self.speed = 4.5
    
    def stop_acceleration(self):
        #when up key is released player is no longer thrusting
        self.thrust = False 
    
    #adds bullets w/ ship information to ammo from ship  
    def generate_bullets(self):
        # makes sure that user cannot spam bullets 
        if len(self.bullets_field) != 7:
            self.bullets_field.append(Bullets(self, self.temp_rotation))

    #in main loop and will continue to run until the list of bullets is wiped
    def use_bullets(self):        
        #loops through bullets in 'ammo'
        for i in range (len(self.bullets_field)):
            self.bullets_field[i].move()
            self.bullets_field[i].draw()
            #if the bullets are not in its bounds remove them from the list 
            if self.bullets_field[i].bounds():
                self.bullets_field.pop(i)
                break
    
    #return current bullets to check for collision detection with other objects of seperate classes 
    def get_bullets(self):
        return self.bullets_field
    
    #check if the ship is colliding with enemy ships bullets 
    def collide(self, object):
        #return distance between ship and enemy ship 
        distance = find_distance(self, object)
        if self.radius + object.radius >= distance:
            #returns bool whether or not an enemy is colliding with the passed in object
            return True
        #not overlapping 
        return False

    #check if ship is thrusting
    def is_thrusting(self):
        return self.thrust
    
#enemy ship which is randomly generated 
class Enemy:
    #enemy ships random attributes 
    def __init__(self):
        #ship comes from either corner 
        self.x = random.choice([0, SCREEN_WIDTH])
        self.y = random.choice([0, SCREEN_LENGTH])   
        #object detection
        self.radius = 15
        #creates vars to change 
        self.dx = random.randint(1,2) 
        self.dy = random.randint(1,2) 
        #attribute to check points when you eliminate it 
        self.Size = "enemy"
       #depending on starting corner choose direction   
        if self.x == SCREEN_WIDTH:
            self.dx*=-1
        if self.y == SCREEN_LENGTH:
            self.dy*=-1
        #angle of bullets 
        self.angle = 0 
        #collection of all the bullets
        self.bullets_field = []
    
    #draws enenmy ship to screen
    def draw(self):
        global enemy
        imageMode(CENTER)
        image(enemy, self.x, self.y, self.radius*2, self.radius*2)
    
    #moves the ship based on its velocity
    def move(self):
        self.x += self.dx
        self.y += self.dy
    
    def out_bounds(self):
        #enemy is out of bounds.. remove it from list of enemies 
         if self.x > SCREEN_WIDTH+1:
             return True
         if self.x < -1:
             return True
         if self.y > SCREEN_LENGTH+1:
             return True 
         if self.y < -1:
             return True
         return False       
     
     #adding bullets to ammo
    def setup_bullets(self):
        #generate random bullets for ship in 360 direction
        self.angle += 20
        if self.angle == 360:
            self.angle = 0 
        #creates a bullet with objects current position and rotating angle of bullets
        if len(self.bullets_field) < 3:
            self.bullets_field.append(Bullets(self, self.angle))
    #using bullets 
    def use_bullets(self):        
        #always using bullets 
        for i in range (len(self.bullets_field)):
            #moving and drawing them to screen
            self.bullets_field[i].move()
            self.bullets_field[i].draw()
            #if out of bounds remove them
            if self.bullets_field[i].bounds():
                self.bullets_field.pop(i)
                break
    #checks whether enemy ship is colliding with another object
    def collide(self, object):
        distance = find_distance(self, object)
        if self.radius + object.radius >= distance:
            #returns bool whether or not an enemy is colliding with the passed in object
            return True
        return False
    
    #return bullets to compare with other objects 
    def get_bullets(self):
        return self.bullets_field 
        
#bullets shot by player or enemy ship             
class Bullets:
    def __init__(self, object, angle):
        # bullet generated starts at the object who's shooting it's location
        self.x = object.x
        self.y = object.y
        # default speed of bullet 
        self.speed = 5 
        #angle of object shooting 
        self.angle = angle 
        #size of a bullet.. repeated for reuse in other method
        self.radius = 2
    
    def draw(self):  
        #draw bullets based on curent trajectory
        fill(255)
        stroke(255)
        #circle drawn to screen
        circle (self.x, self.y, self.radius)     
        fill(0)
        stroke(0)
        
    def move(self):
        #goes in direction based on what angle was passed in by the object shooting
        self.x += (cos(radians(self.angle))*self.speed)
        self.y += (sin(radians(self.angle))*self.speed)
        
    def bounds(self):
        # returns if bullet is in screen bounds.. if so return True
        if self.x > SCREEN_WIDTH:
            return True
        if self.x < 0:
            return True
        if self.y > SCREEN_LENGTH:
            return True
        if self.y < 0:
            return True
        #in bounds
        return False
    

#game as an object.. containing num of lives, methods to control game ie. pausing or quitting 
class Game:
    #default num of lives, bools for ending the game, paused screen, or quitting, or screen 
    def __init__(self):
        #default starting screen
        self.mode = 'HOME'
        #number of starting lives
        self.lives = 5
        #temp points to keep enemy spawn in check 
        self.temp_points = 0
        self.points = 0
    
    #determines current screen 
    def run(self):
        if self.mode == "HOME":
            self.home_screen()
        if self.mode == "GAME":  
            self.game_screen()
        if self.mode == "INSTRUCT":
            self.instruct_screen()
        if self.mode == "END":
            self.end_screen()
    
    def instruct_screen(self):
        global instruct
        #draws instruction image for user
        background(0) 
        imageMode(CORNER) 
        image(instruct, 0,0, SCREEN_WIDTH, SCREEN_LENGTH)     
    
    def home_screen(self):
        global font, border
        #border in the background
        imageMode(CORNER)
        image(border, 0,0, SCREEN_WIDTH, SCREEN_LENGTH)
    
        #draws animated asteroids moving in bakc 
        for asteroid in home_field:
            asteroid.move()
            asteroid.draw()        
        
        #draw title to screen
        fill(255)
        textFont(font)
        textAlign(CENTER) 
        textSize(100)
        text("ASTEROIDS", SCREEN_WIDTH/2, SCREEN_LENGTH*0.45)
        
        textSize(50) 
        
        #if hovering over "play game" turn it to grey 
        if mouseX > 250 and mouseX < SCREEN_WIDTH-250 and mouseY > SCREEN_LENGTH*0.5 and mouseY < SCREEN_LENGTH*0.55:
           fill(200)        
        else:
            fill(255)
        
        #draws action item
        text("PLAY GAME", SCREEN_WIDTH/2, SCREEN_LENGTH*0.55)
        
        #if hovering over "instructions" turn it to grey
        if mouseX > 250 and mouseX < SCREEN_WIDTH-250 and mouseY > SCREEN_LENGTH*0.6 and mouseY < SCREEN_LENGTH*0.65:
           fill(200)        
        else:
            fill(255)
            
        #draws action item        
        text("INSTRUCTIONS", SCREEN_WIDTH/2, SCREEN_LENGTH*0.65)
        
    
    #return state of the current game 
    def get_gamestate(self):
        return self.mode 
    
    #adds points to the game 
    def gain_points(self, object):
        #depending on whether an asteroid is broken or an enemy ship, increase points 
        if object.Size == "large": 
            self.points += 25 
        if object.Size == "medium": 
            self.points += 50 
        if object.Size == "small":
            self.points += 75
        if object.Size == "enemy":
            self.points += 100
        self.temp_points = self.points
            
    #randomly spawns in asteroids and enemy ships 
    def spawner(self):
        #if points are multiple of 200 and not equal to zero spawn an enemy 
        if self.temp_points%200 == 0 and self.temp_points!= 0:
            self.temp_points+=1
            enemies_field.append(Enemy())
            #if points are above 1000 spawn two enemies at once
            if self.temp_points > 1000:
                enemies_field.append(Enemy())
        #if points are multiple of 100, not equal to zero, and there are 15 or less asteroids spawn two large asteroids 
        if self.temp_points%100 == 0 and self.temp_points!= 0 and len(asteroids_field)< 16:
            self.temp_points+=1
            #spawn two asteroids
            for n in range(2):
                asteroids_field.append(Asteroid(random.randint(20, SCREEN_WIDTH-20),random.randint(20, SCREEN_LENGTH-20), 'large', dx, dy))
    
    #show the number of lives of user using image 
    def display_lives(self):
        global live
        #draws adding one by one next to each other
        x = 0
        y = 70
        #draws to top left corner 
        for n in range(self.lives):
            x += 30
            image(live, x, y, 30, 30)
        
    #display user points 
    def display_points(self):
        global font
        #font imported 
        textFont(font)
        #text drawn 
        text(str(self.points), 40,40)
        
    #method to change game mode 
    def change_mode(self, mode):
        self.mode = mode
    
    #check if game is finished 
    def check_game(self):
        if self.lives == 0: 
            self.mode = "END"
            
    #end screen
    def end_screen(self):
        global font, border
        #import border image 
        imageMode(CORNER)
        image(border, 0,0, SCREEN_WIDTH, SCREEN_LENGTH)
        fill(255)
        textAlign(CENTER) 
        textFont(font)
        textSize(80)
        #game over text
        text("GAME OVER!", SCREEN_WIDTH/2, SCREEN_LENGTH/2)         
        textSize(40)
        #shows score
        text("Your final score was " + str(self.points), SCREEN_WIDTH/2, SCREEN_LENGTH*0.63)   
        #highlight in grey if user hovering over "return home"
        if mouseX > 250 and mouseX < SCREEN_WIDTH-250 and mouseY > SCREEN_LENGTH*0.68 and mouseY < SCREEN_LENGTH*0.77: 
            fill(200)
        else:
            fill(255) 
        #option to return home 
        text("RETURN HOME", SCREEN_WIDTH/2, SCREEN_LENGTH*0.73)
    
    #reset the game for the next user 
    def reset(self):
        global ship
        #reset everything 
        asteroids_field = []
        enemies_field = []
        self.lives = 5
        self.points = 0
        ship = Ship() 
        
        # asteroids generated 
        for n in range(4):
            while True:
                dx = random.randint(-20,20)/10
                dy = random.randint(-20,20)/10
                if dx != 0 and dy != 0:
                    break
            asteroids_field.append(Asteroid(random.randint(20, SCREEN_WIDTH-20),random.randint(20, SCREEN_LENGTH-20), 'large', dx, dy))
        
        
    #playing the game screen
    def game_screen(self):
        global slow
    
        #reset screen with background
        background(0) 
        
        #bool to break main loop if needed
        run_loop = False  
        
        #check game for lives
        self.check_game()
        
        #based on how many points there are spawn certain items 
        self.spawner()     
        
        # loop through list of asteroids and draws them to the screen and moves them 
        for i in range (len(asteroids_field)):
            #move asteroid
            asteroids_field[i].move()
            #check if asteroid is touching ship
            if asteroids_field[i].collide(ship):
                #reduce live, split said asteroid, remove asteroid from list and reset the ship to starting location
               self.lives-=1  
               asteroids_field[i].split_asteroid()
               asteroids_field.pop(i)
               ship.reset()
               break               
            #check if asteroids are touching any bullets from ship
            for r in range (len(enemies_field)):
                #if the ships bullets collides with asteroid 
                if asteroids_field[i].collide(enemies_field[r]):
                    #split the asteroid into smaller version.
                    asteroids_field[i].split_asteroid()
                    #asteroid is hit and removed from the game
                    asteroids_field.pop(i)
                    #bullet is removed instead of continuing
                    enemies_field.pop(r) 
                    #both loops are broken preventing index error, to process change in index 
                    run_loop = True
                    break
            #main loop is broken to prevent index error 
            if run_loop:
                break
            for r in range (len(ship.get_bullets())):
                #if the ships bullets collides with asteroid 
                if asteroids_field[i].collide(ship.get_bullets()[r]):
                    #split the asteroid into smaller version.
                    asteroids_field[i].split_asteroid()
                    #gain points for asteroids broken
                    self.gain_points(asteroids_field[i])
                    #asteroid is hit and removed from the game
                    asteroids_field.pop(i)
                    #bullet is removed instead of continuing
                    ship.get_bullets().pop(r) 
                    #both loops are broken preventing index error, to process change in index 
                    run_loop = True
                    break
            #main loop is broken to prevent index error 
            if run_loop:
                break
            #draw the asteroid            
            asteroids_field[i].draw()
            
        run_loop = True 
        #loop through the lsit of enemies 
        for i in range (len(enemies_field)):
            #move them
            enemies_field[i].move()
            #randomly generate bullets
            enemies_field[i].setup_bullets()
            #use their bullets 
            enemies_field[i].use_bullets()
            #check through ships bullets to see if there is a collision them and enemy ship
            for r in range(len(ship.get_bullets())):
                #checks for collision
                if enemies_field[i].collide(ship.get_bullets()[r]):
                    #gain points based off enemy
                     self.gain_points(enemies_field[i])
                     #remove the enemy
                     enemies_field.pop(i)  
                     #break loop to avoid index error
                     run_loop = False                  
                     break  
            #break loop to avoid index error 
            if not run_loop:
                 break  
            #check if enemies bullets are hitting the user 
            for r in range(len(enemies_field[i].get_bullets())):
                #if they are 
                if ship.collide(enemies_field[i].get_bullets()[r]):
                    #remove the enemy
                    enemies_field.pop(i)
                    #reduce lives and reset ship
                    self.lives -=1 
                    ship.reset()
                    #break loop to avoid index error
                    run_loop = False 
                    break
            #break loop to avoid index error 
            if not run_loop:
                break
            
            #if enemy collides with the ship
            if enemies_field[i].collide(ship):
                #remove the ship
                enemies_field.pop(i)  
                #take live away and reset the ship
                self.lives -=1 
                ship.reset()
                run_loop = False                  
                break                 
            if not run_loop:
                 break       
            #draw enemy ship
            enemies_field[i].draw()
        
        #use bullets from ships current supply
        ship.use_bullets()
        # draw the ship 
        ship.draw()
        #move ship based on current velocity and angle 
        ship.move()
        
        #if up key is released.. slow down the velocity once each loop
        if not ship.is_thrusting():
            ship.slow_down()
        
        #display points to top left corner of scren 
        self.display_points()     
        #display num of lives
        self.display_lives()

############################################################################
# FUNCTIONS     
                
#function to find distance between two objects 
def find_distance(object_1, object_2): #pass both objects in 
    #finds differnece between x and y for both objects
    delta_x = abs(object_1.x - object_2.x)
    delta_y = abs(object_1.y - object_2.y)
    
    # distance found using pythagorean 
    distance = math.sqrt(delta_x**2 + delta_y**2)
    #return distance between two objects
    return distance     

##################################################################################
# object creation & variables 
            
# screen dimension constants 
SCREEN_WIDTH = 800
SCREEN_LENGTH = 600

#all enemies
enemies_field = []
# generates all random  asteroids
asteroids_field = []
#generate random asteroids for menu screen
home_field =  []

#generate random asteroids for menu screen
for n in range(6):
    while True:
        dx = random.randint(-20,20)/10
        dy = random.randint(-20,20)/10
        if dx != 0 and dy != 0:
            break
    if n < 3:
        home_field.append(Asteroid(random.randint(20, SCREEN_WIDTH-20),random.randint(20, SCREEN_LENGTH-20), 'large', dx, dy))
    else:
        home_field.append(Asteroid(random.randint(20, SCREEN_WIDTH-20),random.randint(20, SCREEN_LENGTH-20), 'medium', dx, dy))
    
# asteroids generated 
for n in range(4):
    while True:
        dx = random.randint(-20,20)/10
        dy = random.randint(-20,20)/10
        if dx != 0 and dy != 0:
            break
    asteroids_field.append(Asteroid(random.randint(20, SCREEN_WIDTH-20),random.randint(20, SCREEN_LENGTH-20), 'large', dx, dy))

#ship created 
ship = Ship()
#controlls all aspects of the game, such as lives, game screen and paused screen
game = Game()

######################################################
# processing stuff 

def setup():
    global enemy, live, font, images, img1, img2, img3, img4, img5, img6, instruct, border
    #size of screen
    size(SCREEN_WIDTH, SCREEN_LENGTH)
    #all images imported 
    enemy = loadImage("enemy.png") 
    live = loadImage("lives.png")
    #font imported 
    font = createFont(PFont.list()[0],32)
    #all variations of asteroids
    img1 = loadImage("asteroid1.png")
    img2 = loadImage("asteroid2.png")
    img3 = loadImage("asteroid3.png")
    img4 = loadImage("asteroid4.png")
    img5 = loadImage("asteroid5.png")
    img6 = loadImage("asteroid6.png")
    
    #background screens 
    instruct = loadImage("instructions.jpeg")
    border = loadImage("border.jpeg")

# draw loop 
def draw():   
    #run the game.. class methods will handle all the work.. they call on themselves 
    game.run()
   
# function ran when any key is pressed
def keyPressed():
    #game screen
    if game.get_gamestate() == 'GAME':
        # rotates right if right key is pressed
        if keyCode == RIGHT:
            ship.rotate_right()
        #rotates left if left key is pressed
        if keyCode == LEFT:
            ship.rotate_left()
        #ships accelerates
        if keyCode == UP:
            #accelerate the ship
            ship.accelerate()
        #shoot bullets
        if key == ' ': 
            ship.generate_bullets()
    
    #if on instruction screen
    if game.get_gamestate() == "INSTRUCT":
        if keyCode == RIGHT:
            game.change_mode("GAME")
        if keyCode == LEFT:
            game.change_mode("HOME") 
         
def keyReleased():
    # once up key is released activate bool which slows ship down once every loop
    if keyCode == UP:  
        #deactivate thrust bool 
        ship.stop_acceleration()
        
def mousePressed():
    #home screen
    if game.get_gamestate() == "HOME":
        #game button
        if mouseX > 250 and mouseX < SCREEN_WIDTH-250 and mouseY > SCREEN_LENGTH*0.5 and mouseY < SCREEN_LENGTH*0.55:
            game.change_mode("GAME") 
        #instruction button
        elif mouseX > 250 and mouseX < SCREEN_WIDTH-250 and mouseY > SCREEN_LENGTH*0.5 and mouseY < SCREEN_LENGTH*0.65:
            game.change_mode("INSTRUCT")
    #end screen
    if game.get_gamestate() == "END":
        #return home button
        if mouseX > 250 and mouseX < SCREEN_WIDTH-250 and mouseY > SCREEN_LENGTH*0.68 and mouseY < SCREEN_LENGTH*0.77: 
            #reset the game 
            game.reset()
            game.change_mode("HOME")
