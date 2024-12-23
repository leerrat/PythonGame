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


full_bar = Health_bar(player, -0.6, 255, 0, 0)
green_bar = Health_bar(player, -0.6, 0, 255, 0)

""" green_bar.scale_x = 1 """

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
    global bullets, time_counter, enemy_index, time_enemy
    time_counter += time.dt
    time_enemy += time.dt

    # Déplacement du joueur
    player.x += held_keys['d'] * (time.dt * 2)
    player.x -= held_keys['a'] * (time.dt * 2)
    player.y += held_keys['w'] * (time.dt * 2)
    player.y -= held_keys['s'] * (time.dt * 2)

    # Création d'une balle
    if time_enemy >= 1:
        e = Entity(
            y=player.y,
            x=player.x,
            model ='cube',
            color = color.red,
            scale = 0.2,
            collider='box'
        )

        e.animate_y(
            30,
            duration=3,
            curve=curve.linear
        )
        bullets.append(e)
        invoke(destroy, e,delay=3)
        time_enemy = 0
    
    # Apparition des ennemis
    if time_counter >= 3:
        x_random = random.uniform(-sizex, sizex)
        y_random = random.uniform(-sizey, sizey)
        new_enemy = Enemy(f"ennemi{enemy_index}", x_random, y_random, player)
        liste.append(new_enemy)
        enemy_index += 1
        time_counter = 0

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
