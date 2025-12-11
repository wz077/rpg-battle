import tkinter as tk
from tkinter import messagebox
import random

import tkinter as tk
from tkinter import messagebox
import random

class Enemy:
    def __init__(self, health, maxhealth):
        self.health = health
        self.maxhealth = maxhealth
    
    def lightattack(self):
        damage = random.randint(3,6)
        player.health -= damage
        return f"Enemy used LIGHT attack and dealt {damage} damage!"
    
    def mediumattack(self):
        damage = random.randint(7,12)
        player.health -= damage
        return f"Enemy used MEDIUM attack and dealt {damage} damage!"
    
    def heavyattack(self):
        damage = random.randint(12,18)
        player.health -= damage
        return f"Enemy used HEAVY attack and dealt {damage} damage!"
    
    def heal(self):
        heal_amount = random.randint(8,15)
        self.health = min(self.maxhealth, self.health + heal_amount)
        return f"Enemy healed {heal_amount} HP!"
    
    def action(self):
        if self.health < 85:
            action = random.choice([self.lightattack, self.mediumattack, self.heavyattack, self.heal])
        else:
            action = random.choice([self.lightattack, self.mediumattack, self.heavyattack])
        return action()

class Player:
    def __init__(self, health, maxhealth):
        self.health = health
        self.maxhealth = maxhealth
         
    def punch(self):
        damage = random.randint(8,11)
        opponent.health -= damage
        return f"You punched the opponent and did {damage} damage!"
    
    def kick(self):
        damage = random.randint(1,18)
        opponent.health -= damage
        return f"You kicked the opponent and did {damage} damage!"
    
    def spell(self):
        if opponent.health < 82:
            spell = random.choice([self.fireball, self.explosion, self.earthquake, self.lightning, self.enemyheal])
        else:
            spell = random.choice([self.fireball, self.explosion, self.earthquake, self.lightning])
        return spell()
    
    def fireball(self):
        damage = random.randint(20,30)
        opponent.health -= damage
        return f"You cast FIREBALL and dealt {damage} damage!"
    
    def explosion(self):
        damage = random.randint(20,30)
        player.health -= damage
        return f"Your EXPLOSION spell backfired and dealt {damage} damage to yourself!"
    
    def earthquake(self):
        damage = random.randint(10,20)
        player.health -= damage
        opponent.health -= damage
        return f"You caused an EARTHQUAKE and dealt {damage} damage to both!"
        
    def lightning(self):
        hits = random.randint(1,5)
        damage = hits * 5
        opponent.health -= damage
        return f"You cast LIGHTNING {hits} times dealing {damage} damage!"
        
    def enemyheal(self):
        heal = random.randint(10,18)
        opponent.health += heal
        return f"You accidentally healed the enemy for {heal} HP!"
    
    def heal(self):
        heal_amount = random.randint(5,20)
        self.health = min(self.maxhealth, self.health + heal_amount)
        return f"You healed {heal_amount} HP!"


opponent = Enemy(100, 100)
player = Player(100, 100)


root = tk.Tk()
root.title("RPG Battle")

canvas_width = 500  
canvas_height = 180
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="#222222")
canvas.pack(pady=20)

canvas.create_text(50, 20, anchor="w", fill="white", font=("Arial", 12, "bold"), text="Enemy")
canvas.create_text(50, 80, anchor="w", fill="white", font=("Arial", 12, "bold"), text="Player")

canvas.create_rectangle(50, 30, 450, 60, fill="grey", outline="")
canvas.create_rectangle(50, 90, 450, 120, fill="grey", outline="")

player_bar = canvas.create_rectangle(50, 90, 450, 120, fill="green", outline="")
opponent_bar = canvas.create_rectangle(50, 30, 450, 60, fill="red", outline="")

log_text = tk.Text(root, height=12, width=65, state='disabled', bg="#f0f0f0", wrap='word')
log_text.pack(pady=10)

def update_health_bars():
    player_ratio = player.health / player.maxhealth
    canvas.coords(player_bar, 50, 90, 50 + 400 * player_ratio, 120)
    opponent_ratio = opponent.health / opponent.maxhealth
    canvas.coords(opponent_bar, 50, 30, 50 + 400 * opponent_ratio, 60)

def log(message):
    log_text.config(state='normal')
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)
    log_text.config(state='disabled')

def check_winner():
    if player.health <= 0:
        log("The opponent beat you!")
        messagebox.showinfo("Game Over", "You lost!")
        root.quit()
    elif opponent.health <= 0:
        log("You beat the opponent!")
        messagebox.showinfo("Victory!", "You won!")
        root.quit()

def enemy_turn():
    msg = opponent.action()
    log(msg)
    update_health_bars()
    check_winner()

def player_action(action):
    if action == "Punch":
        msg = player.punch()
    elif action == "Kick":
        msg = player.kick()
    elif action == "Spell":
        msg = player.spell()
    elif action == "Heal":
        if player.health < player.maxhealth:
            msg = player.heal()
        else:
            log("You're already at full health!")
            return
    log(msg)
    update_health_bars()
    check_winner()
    root.after(500, enemy_turn)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

for act in ["Punch", "Kick", "Spell", "Heal"]:
    b = tk.Button(button_frame, text=act, width=12, command=lambda a=act: player_action(a))
    b.pack(side='left', padx=5)

update_health_bars()

root.mainloop()

