from ursina import *
import random

time_counter = 0
time_enemy = 0
enemy_index = 0

bullets = []
auras = []

speed = 1
dx = 0
shrink = 2

app = Ursina()

liste = []

sizex = 16
sizey = 9

direction_tire = Vec3(1, 0, 0)

score = 0

pause_handler = Entity(ignore_paused=True)
pause_text = Text('PAUSE', origin=(0,0), scale=2, enabled=False)
lose_text = Text('Vous avez perdu', origin=(0,0), scale=2, enabled=False)

class Enemy(Entity):
    def __init__(self, name, x, y, target):
        super().__init__()
        self.model = "quad"
        self.color = color.white
        self.texture = "Gob"
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
        if distance_to_player > 1.5:
            self.position += direction * self.speed * time.dt

class Health_bar(Entity):
    def __init__(self, target, offset_y, r, g, b):
        super().__init__()
        self.model = "quad"
        self.scale = (1, 0.1)
        self.color = color.rgb(r, g, b)
        self.target = target
        self.offset_y = offset_y 
        self.origin = (-0.5, 0)

    def update(self):
        self.x = self.target.x - 0.5
        self.y = self.target.y + self.offset_y

bg = Entity(model="quad", scale=(sizex, sizey), texture="Jungle", z=1)
player = Entity(model='quad', scale_y=1, collider="box",texture = "Perso")

text=Text(text=f"Exp: {score}", target=player, scale=2.5, color=color.yellow,background=True,position=(-.65,.4))

class Experience(Entity):
    def __init__(self, position):
        super().__init__(
            model='sphere',
            color=color.yellow,
            scale=0.5,
            position=position,
            collider='box',
            texture = "Exp"
        )

    def update(self):
        global score,text
        if distance(self.position, player.position) < 1:
            Audio(sound_file_name="XP_Sound", volume=0.15)
            score +=1
            text.text = f"Exp: {score}"
            destroy(self)

full_bar = Health_bar(player, -0.6, 255, 0, 0)
full_bar.z = 0.1
green_bar = Health_bar(player, -0.6, 0, 255, 0)
green_bar.z = 0

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

    def pause_handler_input(key):
        if held_keys['space']:  # Appuyez sur espace pour activer/désactiver la pause
            application.paused = not application.paused
            pause_text.enabled = application.paused
    pause_handler.input = pause_handler_input

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

    for aura in auras:
        destroy(aura)
    auras.clear()

    if score >= 5:
        aura2 = Entity(
            y=player.y + 2,
            x=player.x + 2,
            model='cube',
            color=color.yellow,
            scale=0.5,
            collider='box',
            target=player,
            texture = "Boule"
        )
        auras.append(aura2)

    if score >= 20:
        aura3 = Entity(
            y=player.y + 3,
            x=player.x + 3,
            model='cube',
            color=color.yellow,
            scale=0.5,
            collider='box',
            target=player,
            texture = "Boule"
        )
        auras.append(aura3)

    if score >= 40:
        aura4 = Entity(
            y=player.y + 4,
            x=player.x + 4,
            model='cube',
            color=color.yellow,
            scale=0.5,
            collider='box',
            target=player,
            texture = "Boule"
        )
        auras.append(aura4)

    for i, aura in enumerate(auras):
        angle = (time.time() * 100 + i * (360 / len(auras))) % 360
        aura.x = player.x + 2 * math.cos(math.radians(angle))
        aura.y = player.y + 2 * math.sin(math.radians(angle))

    if score <= 15:
        if time_counter >= 1: 
            e = Entity(
                y=player.y,
                x=player.x,
                model='cube',
                scale=0.8,
                collider='box',
                texture = "Dague"
            )
            e.animate_position(
                e.position + direction_tire * 30,  
                duration=3,
                curve=curve.linear
            )
            Audio(sound_file_name="knife_sound", volume=0.15)
            bullets.append(e)
            invoke(destroy, e, delay=3)
            time_counter = 0
    else :
        if score <=50:
            if time_counter >= 0.4: 
                e = Entity(
                    y=player.y,
                    x=player.x,
                    model='cube',
                    scale=0.8,
                    collider='box',
                    texture = "Dague"
                )
                e.animate_position(
                    e.position + direction_tire * 30,  
                    duration=3,
                    curve=curve.linear
                )
                Audio(sound_file_name="knife_sound", volume=0.15)
                bullets.append(e)
                invoke(destroy, e, delay=3)
                time_counter = 0
        else :
            if time_counter >= 0.2: 
                e = Entity(
                    y=player.y,
                    x=player.x,
                    model='cube',
                    scale=0.8,
                    collider='box',
                    texture = "Dague"
                )
                Audio(sound_file_name="knife_sound", volume=0.15)
                e.animate_position(
                    e.position + direction_tire * 30,  
                    duration=3,
                    curve=curve.linear
                )
                bullets.append(e)
                invoke(destroy, e, delay=3)
                time_counter = 0

    if score <= 15:
        if time_enemy >= 3:
            x_random = random.uniform(-sizex, sizex)
            y_random = random.uniform(-sizey, sizey)
            new_enemy = Enemy(f"ennemi{enemy_index}", x_random, y_random, player)
            liste.append(new_enemy)
            enemy_index += 1
            time_enemy = 0
    else:
        if score <= 40:
            if time_enemy >= 1.5:
                x_random = random.uniform(-sizex, sizex)
                y_random = random.uniform(-sizey, sizey)
                new_enemy = Enemy(f"ennemi{enemy_index}", x_random, y_random, player)
                liste.append(new_enemy)
                enemy_index += 1
                time_enemy = 0
        else:
            if score <= 150:
                if time_enemy >= .5:
                    x_random = random.uniform(-sizex, sizex)
                    y_random = random.uniform(-sizey, sizey)
                    new_enemy = Enemy(f"ennemi{enemy_index}", x_random, y_random, player)
                    liste.append(new_enemy)
                    enemy_index += 1
                    time_enemy = 0
            else :
                if time_enemy >= .2:
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

    for bullet in bullets[:]:
        for enemy in liste[:]:
            if bullet.intersects(enemy).hit:
                Experience(position=enemy.position)
                destroy(bullet)
                destroy(enemy)
                bullets.remove(bullet)
                liste.remove(enemy)
                break 
                
    for aura in auras[:]:
        for enemy in liste[:]:
            if aura.intersects(enemy).hit:
                Experience(position=enemy.position)
                destroy(enemy)
                liste.remove(enemy)
                break 

    for enemy in liste:
        if enemy.intersects(player).hit:
            green_bar.scale_x -= shrink * time.dt
            if green_bar.scale_x < 0:
                green_bar.scale_x = 0
                application.paused = True
                lose_text.enabled = True
                

camera.add_script(SmoothFollow(target=player, offset=[0, 1, -40], speed=10))
app.run()
