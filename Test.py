from ursina import *

class Enemy(Entity):
    def __init__(self, x,y):
        super().__init__()
        self.model="cube"
        self.color=color.white
        self.texture="goblin"
        self.x=x
        self.y=y
speed =1
dx=0
# create a window
app = Ursina()

ennemi=Enemy(2,2)
sizex=16
sizey=9
bg=Entity(model="quad",scale=(sizex,sizey),texture="Forest",z=1)
player = Entity(model='sphere', color=color.orange, scale_y=1)

for m in range(2):
    for n in range(2):
        duplicate(bg,x=sizex*(m+1),y=sizey*(n+1))
        duplicate(bg,x=-sizex*(m+1),y=sizey*(n+1))
        duplicate(bg,x=sizex*(m+1),y=-sizey*(n+1))
        duplicate(bg,x=-sizex*(m+1),y=-sizey*(n+1))
        duplicate(bg,x=-sizex*(m+1))
        duplicate(bg,y=sizey*(m+1))
        duplicate(bg,x=sizex*(m+1))
        duplicate(bg,y=-sizey*(m+1))


# create a function called 'update'.
# this will automatically get called by the engine every frame.

def update():
    player.x += held_keys['d'] * (time.dt*3)
    player.x -= held_keys['a'] * (time.dt*3)
    player.y += held_keys['w'] * (time.dt*3)
    player.y -= held_keys['s'] * (time.dt*3)
    global speed, dx
    dx+=speed*time.dt
    if abs(dx)>2:
        speed*=-1
        dx=0
    ennemi.x+=speed*time.dt

# this part will make the player move left or right based on our input.
# to check which keys are held down, we can check the held_keys dictionary.
# 0 means not pressed and 1 means pressed.
# time.dt is simply the time since the last frame. by multiplying with this, the
# player will move at the same speed regardless of how fast the game runs.


#def input(key):
#    if key == 'space':
#       player.y += 1
#       invoke(setattr, player, 'y', player.y-1, delay=.25)

camera.add_script(SmoothFollow(target=player,offset=[0,1,-40],speed=10))

# start running the game
app.run()