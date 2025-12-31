import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QMessageBox
from PyQt5.QtGui import QFont, QPainter, QColor
from PyQt5.QtCore import Qt, QTimer

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

opponent = Enemy(100,100)
player = Player(100,100)

class BattleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RPG Battle")
        self.setFixedSize(520, 500)

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.layout = QVBoxLayout()
        self.central.setLayout(self.layout)

        self.health_canvas = HealthCanvas()
        self.layout.addWidget(self.health_canvas)

        self.button_frame = QHBoxLayout()
        self.layout.addLayout(self.button_frame)

        for act in ["Punch", "Kick", "Spell", "Heal"]:
            btn = QPushButton(act)
            btn.setFixedWidth(100)
            btn.clicked.connect(lambda checked, a=act: self.player_action(a))
            self.button_frame.addWidget(btn)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFixedHeight(200)
        self.layout.addWidget(self.log_text)

        self.update_health_bars()

    def update_health_bars(self):
        self.health_canvas.update_bars(player.health/player.maxhealth, opponent.health/opponent.maxhealth)

    def log(self, message):
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())

    def check_winner(self):
        if player.health <= 0:
            self.log("The opponent beat you!")
            QMessageBox.information(self, "Game Over", "You lost!")
            QApplication.quit()
        elif opponent.health <= 0:
            self.log("You beat the opponent!")
            QMessageBox.information(self, "Victory!", "You won!")
            QApplication.quit()

    def enemy_turn(self):
        msg = opponent.action()
        self.log(msg)
        self.update_health_bars()
        self.check_winner()

    def player_action(self, action):
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
                self.log("You're already at full health!")
                return
        self.log(msg)
        self.update_health_bars()
        self.check_winner()
        QTimer.singleShot(500, self.enemy_turn)

class HealthCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(140)
        self.enemy_ratio = 1.0
        self.player_ratio = 1.0

    def update_bars(self, player_ratio, enemy_ratio):
        self.player_ratio = max(0, min(1, player_ratio))
        self.enemy_ratio = max(0, min(1, enemy_ratio))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(20, 20, 480, 100, QColor("#222222"))

        painter.setBrush(QColor("red"))
        painter.drawRect(50, 30, int(400 * self.enemy_ratio), 30)
        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.drawText(50, 52, "Enemy")

        painter.setBrush(QColor("green"))
        painter.drawRect(50, 80, int(400 * self.player_ratio), 30)
        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.drawText(50, 102, "Player")

app = QApplication(sys.argv)
window = BattleWindow()
window.show()
sys.exit(app.exec_())

