from ursina import *
import random

time_counter = 0
time_enemy = 0
enemy_index = 0

bullets = []

speed = 1
dx = 0
shrink = 2

app = Ursina()

liste = []

sizex = 16
sizey = 9

direction_tire = Vec3(1, 0, 0)

score = 0

class Enemy(Entity):
    def __init__(self, name, x, y, target):
        super().__init__()
        self.model = "cube"
        self.color = color.white
        self.texture = "goblin"
        self.name = name
        self.x = x
        self.y = y
        self.target = target
        self.speed = 1
        self.collider = "box"

    def update(self):
        direction = self.target.position - self.position
        distance_to_player = direction.length()
        direction = direction.normalized()
        self.position += direction * self.speed * time.dt
        if distance_to_player > 1.5:  # Arrête l'ennemi à 1.5 unités du joueur
            self.position += direction * self.speed * time.dt


class Health_bar(Entity):
    def __init__(self, target, offset_y, r, g, b):
        super().__init__()
        self.model = "quad"
        self.scale = (1, 0.1)  # Taille de la barre de santé
        self.color = color.rgb(r, g, b)  # Couleur
        self.target = target  # L'entité à suivre (par exemple, le joueur)
        self.offset_y = offset_y  # Décalage vertical (c'est ici qu'il est défini)
        self.origin = (-0.5, 0)

    def update(self):
        # Synchroniser la position avec l'entité cible
        self.x = self.target.x - 0.5
        self.y = self.target.y + self.offset_y

bg = Entity(model="quad", scale=(sizex, sizey), texture="Forest", z=1)
player = Entity(model='sphere', color=color.orange, scale_y=1, collider="box")

text=Text(text=f"Score: {score}", target=player, scale=2, color=color.yellow,background=True,position=(-.65,.4))

class Experience(Entity):
    def __init__(self, position):
        super().__init__(
            model='sphere',
            color=color.yellow,
            scale=0.5,
            position=position,
            collider='box',
        )

    def update(self):
        global score,text
        if distance(self.position, player.position) < 1:
            score +=1
            text.text = f"Score: {score}"
            destroy(self)

full_bar = Health_bar(player, -0.6, 255, 0, 0)
green_bar = Health_bar(player, -0.6, 0, 255, 0)

for m in range(2):
    for n in range(2):
        duplicate(bg, x=sizex * (m + 1), y=sizey * (n + 1))
        duplicate(bg, x=-sizex * (m + 1), y=sizey * (n + 1))
        duplicate(bg, x=sizex * (m + 1), y=-sizey * (n + 1))
        duplicate(bg, x=-sizex * (m + 1), y=-sizey * (n + 1))
        duplicate(bg, x=-sizex * (m + 1))
        duplicate(bg, y=sizey * (m + 1))
        duplicate(bg, x=sizex * (m + 1))
        duplicate(bg, y=-sizey * (m + 1))


def update():
    global bullets, time_counter, enemy_index, time_enemy, direction_tire, score,  text
    time_counter += time.dt
    time_enemy += time.dt

    player_direction = Vec3(0, 0, 0)

    if held_keys['d']:
        player_direction.x = 1  
    if held_keys['a']:
        player_direction.x = -1 
    if held_keys['w']:
        player_direction.y = 1 
    if held_keys['s']:
        player_direction.y = -1

    player_direction = player_direction.normalized()
    player.x += player_direction.x * time.dt * 3
    player.y += player_direction.y * time.dt * 3

    if player_direction.length() > 0:
        direction_tire = player_direction.normalized()

    if time_counter >= 0.5: 
        e = Entity(
            y=player.y,
            x=player.x,
            model='cube',
            color=color.red,
            scale=0.2,
            collider='box'
        )
        e.animate_position(
            e.position + direction_tire * 30,  
            duration=3,
            curve=curve.linear
        )
        bullets.append(e)
        invoke(destroy, e, delay=3)
        time_counter = 0
    
    # Apparition des ennemis
    if time_enemy >= 3:
        x_random = random.uniform(-sizex, sizex)
        y_random = random.uniform(-sizey, sizey)
        new_enemy = Enemy(f"ennemi{enemy_index}", x_random, y_random, player)
        liste.append(new_enemy)
        enemy_index += 1
        time_enemy = 0

    for enemy in liste:
        for other in liste:
            if enemy != other:  # Vérifie que ce n'est pas le même ennemi
                distance = (enemy.position - other.position).length()
                if distance < 1:  # Si trop proche, les repousser
                    direction = (enemy.position - other.position).normalized()
                    enemy.position += direction * time.dt
        distance_to_player = (enemy.position - player.position).length()
        if distance_to_player < 1:  # Si trop proche du joueur, repousser l'ennemi
            direction = (enemy.position - player.position).normalized()
            enemy.position += direction * time.dt * 2  # Repousse l'ennemi plus vite

    for bullet in bullets[:]:  # Itérer sur une copie de la liste des balles
        for enemy in liste[:]:  # Itérer sur une copie de la liste des ennemis
            if bullet.intersects(enemy).hit:
                Experience(position=enemy.position)
                destroy(bullet)
                destroy(enemy)
                bullets.remove(bullet)
                liste.remove(enemy)
                break 
 
    for enemy in liste:
        if enemy.intersects(player).hit:
            green_bar.scale_x -= shrink * time.dt
            if green_bar.scale_x < 0:
                green_bar.scale_x = 0
    
            

camera.add_script(SmoothFollow(target=player, offset=[0, 1, -40], speed=10))
app.run()
