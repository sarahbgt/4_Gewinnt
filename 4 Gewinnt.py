import os
import pygame
import random 

class Settings:
    WINDOW_WIDTH = 800 #Breite 
    WINDOW_HEIGHT = 700 #Höhe
    FPS = 60 #Bildauflösung

    REIHEN = 6 
    SPALTEN = 8 
    ZELLEN = 100 #Größe der Zellen
    RADIUS = ZELLEN // 2 #Radius der Spielsteine 

    BLUE = (0, 0, 255)
    GREEN =(0,255,0)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    MAGENTA = (240,0,255)

    Player_1 = 000
    Player_2 = 000

    max_zug = 48 / 2

class Board:
    def __init__(self):
        #Spielfeld erstellen: für die Spalten und Reihen am Anfang 0 (leer)
        self.board = [[0 for _ in range(Settings.SPALTEN)] for _ in range(Settings.REIHEN)] 

    def drop_stein(self, spalte, stein): 
        for reihe in range(Settings.REIHEN): #Von unten nach oben 1
            if self.board[reihe][spalte] == 0: #Wenn das Feld leer ist
                self.board[reihe][spalte] = stein #Stein setzen
                return True #Wenn alles geklappt hat
        return False #Wenn es nicht geht (die spalte ist voll)

    def check_win(self, stein): # Prüft, ob 4 gleiche Steine nebeneinander, untereinander oder diagonal sind
        for s in range(Settings.SPALTEN - 3): #Spalten durchgehen (nur so weit, dass noch 4 Steine passen)
            for r in range(Settings.REIHEN):  #Alle Reihen durchgehen
                if all(self.board[r][s+i] == stein for i in range(4)): #prüft ob 4 gleiche Steine waagerecht sind
                    return True #Spieler hat gewonnen
        for s in range(Settings.SPALTEN):  #Spalten durchgehen
                for r in range(Settings.REIHEN - 3):  #Reihen durchgehen (nur so weit, dass 4 untereinander passen)
                    if all(self.board[r+i][s] == stein for i in range(4)):  #prüft ob 4 gleiche Steine senkrecht sind
                        return True  #Spieler hat gewonnen

        for s in range(Settings.SPALTEN - 3):  #Spalten durchgehen für Diagonale nach rechts unten
            for r in range(Settings.REIHEN - 3):  #Reihen durchgehen für Diagonale nach rechts unten
                if all(self.board[r+i][s+i] == stein for i in range(4)):  #prüft ob 4 gleiche Steine schräg nach rechts unten gehen 
                    return True  #Spieler hat gewonnen

        for s in range(Settings.SPALTEN - 3):  #Spalten durchgehen für Diagonale nach rechts oben
            for r in range(3, Settings.REIHEN):  #Reihen von oben nach unten
                if all(self.board[r-i][s+i] == stein for i in range(4)):  #prüft ob 4 gleiche Steine schräg nach rechts oben gehen
                    return True  #Spieler hat gewonnen

        return False  #Kein Gewinn gefunden

    def draw(self, screen):  #Zeichnet das Spielfeld und die Steine 

        for s in range(Settings.SPALTEN):  #Geht jede Spalte durch
            for r in range(Settings.REIHEN):  #Geht jede Zeile durch
                pygame.draw.rect(screen, Settings.BLUE, (s * Settings.ZELLEN, (r+1) * Settings.ZELLEN, Settings.ZELLEN, Settings.ZELLEN))  #Blauer Hintergrund für jede Zelle
                pygame.draw.circle(screen, Settings.BLACK, (s * Settings.ZELLEN + Settings.ZELLEN//2, (r+1) * Settings.ZELLEN + Settings.ZELLEN//2), Settings.RADIUS)  #Schwarzer Kreis für leere Felder

        for s in range(Settings.SPALTEN):  #Nochmal jede Spalte durchgehen
            for r in range(Settings.REIHEN):  #Jede Zeile durchgehen
                if self.board[r][s] == 1:  #Wenn Spieler 1 ein Stein gesetzt hat
                    pygame.draw.circle(screen, Settings.RED, (s * Settings.ZELLEN + Settings.ZELLEN//2, Settings.WINDOW_HEIGHT - (r * Settings.ZELLEN + Settings.ZELLEN//2)), Settings.RADIUS)  #Roten Kreis zeichnen
                elif self.board[r][s] == 2:  #Wenn Spieler 2 ein Stein gesetzt hat
                    pygame.draw.circle(screen, Settings.YELLOW, (s * Settings.ZELLEN + Settings.ZELLEN//2, Settings.WINDOW_HEIGHT - (r * Settings.ZELLEN + Settings.ZELLEN//2)), Settings.RADIUS)  #Gelben Kreis zeichnen

        font = pygame.font.SysFont(None, 75) #Schriftart festlegen für Text
        score1 = "Player 1: " + str(Settings.Player_1)
        text = font.render(score1, True, Settings.RED) #Text erstellen
        screen.blit(text, (Settings.WINDOW_WIDTH*0.18 - text.get_width()//2, Settings.WINDOW_HEIGHT*0.08 - text.get_height()//2))

        score1 = "Player 2: " + str(Settings.Player_2)
        text = font.render(score1, True, Settings.YELLOW) #Text erstellen
        screen.blit(text, (Settings.WINDOW_WIDTH*0.80 - text.get_width()//2, Settings.WINDOW_HEIGHT*0.08 - text.get_height()//2))

        pygame.display.update()  #Bildschirm aktualisieren

class AI:  #KI Klasse für den Computer
    def get_move(board): #Wählt zufällig eine passende Spalte
        gültige_spalten = [s for s in range(Settings.SPALTEN) if board.board[Settings.REIHEN-1][s] == 0] #Sucht alle Spalten, wo oben noch was frei ist
        if gültige_spalten: #Wenn es freie Spalten gibt, dann
            return random.choice(gültige_spalten) #zufällig eine auswählen
        return None #Wenn keine Spalte mehr frei ist

def wartenAufBtn():
    waiting = True  #Auf Tastendruck warten
    while waiting:
        for event in pygame.event.get():  #Alle Events durchgehen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:  #Taste gedrückt
                    Btn = True #Rückgabewert, dass de richtige taste gedrückt wurde, also 'j'
                    waiting = False  #Warten stoppen
                    return Btn #Rückgabewqert
                else :
                    Btn = False #Rückgabewert, dass belibige andere taste gedrückt wurde, Spiel beenden
                    waiting = False  #Warten stoppen
                    return Btn

def main(): #Hauptfunktion startet das Spiel
    pygame.init()  #Pygame starten
    screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)) #Fenstergröße festlegen
    pygame.display.set_caption("Vier Gewinnt") #Fenstertitel geben
    clock = pygame.time.Clock() #Uhr für FPS erstellen

    font = pygame.font.SysFont(None, 75) #Schriftart festlegen für Begrüßungstext
    screen.fill(Settings.BLACK) #Hintergrung schwarz
    text = font.render("Willkommen, drücke eine taste!", True, Settings.BLUE) #Text erstellen
    screen.blit(text, (Settings.WINDOW_WIDTH//2 - text.get_width()//2, Settings.WINDOW_HEIGHT//2 - text.get_height()//2)) #Text Mittig setzen
    pygame.display.update() #Bildschirm aktualisieren

    waiting = True  #Auf Tastendruck warten
    while waiting:
        for event in pygame.event.get():  #Alle Events durchgehen
            if event.type == pygame.QUIT:  #Fenster schließen
                pygame.quit()  #Pygame beenden
                return
            if event.type == pygame.KEYDOWN:  #Taste gedrückt
                waiting = False  #Warten stoppen

    board = Board()  #Neues Spielfeld erstellen
    turn = 0  #Startspieler: 0 = Mensch, 1 = Computer
    zähler = 0


    running = True  #Spiel läuft
    while running:
        screen.fill(Settings.BLACK)  #Den Hintergrund schwarz machen
        board.draw(screen)  #Das Spielfeld zeichnen

        for event in pygame.event.get():  #Alle Events prüfen
            if event.type == pygame.QUIT:  #Wenn Fenster geschlossen wird
                running = False  #Das Spiel beenden

        if turn == 0:  #Spieler (Mensch) ist dran
            keys = pygame.key.get_pressed()  #DieTastatur abfragen
            for i in range(Settings.SPALTEN):  #Über alle Spalten laufen
                if keys[getattr(pygame, f'K_{i+1}')]:  #Wenn Taste 1-7 gedrückt wird
                    if board.drop_stein(i, 1):  #Der Spieler setzt ein Stein in Spalte i
                        if board.check_win(1):  #Prüft ob der Spieler gewonnen hat
                            board.draw(screen)  #Den Gewinnerstein zeichnen
                            text = font.render("Du hast gewonnen!", True, Settings.GREEN) #Text erstellen
                            screen.blit(text, (Settings.WINDOW_WIDTH//2 - text.get_width()//2, Settings.WINDOW_HEIGHT//2 - text.get_height()//2))
                            Settings.Player_1 = Settings.Player_1 + 1
                            pygame.display.update() #Bildschirm refresh
                            pygame.time.wait(3000)  #3 Sekunden warten
                            screen.fill(Settings.BLACK) #Bildschirm löschen
                            pygame.display.update() #Bildschirm refresh
                            text = font.render("Weiterspielen? J / N", True, Settings.GREEN) #Text erstellen
                            screen.blit(text, (Settings.WINDOW_WIDTH//2 - text.get_width()//2, Settings.WINDOW_HEIGHT//2 - text.get_height()//2))
                            pygame.display.update() #Bildschirm refresh 
                            if wartenAufBtn(): #wartenAufBtn()
                                main()
                            else:
                                running = False  #Spiel beenden
                        else:
                            zähler += 1
                            turn = 1  #Computer ist als nächstes dran
        else:  #Computer ist dran
            pygame.time.wait(500)  #Kurze Pause, damit es "überlegt" wirkt
            spalte = AI.get_move(board)  #Computer wählt eine Spalte
            if spalte is not None and board.drop_stein(spalte, 2):  #Wenn freie Spalte vorhanden ist -> Stein setzen
                if board.check_win(2):  #Prüft ob der Computer gewonnen hat
                    Settings.Player_2 = Settings.Player_2 + 1
                    board.draw(screen)  #Den Gewinnerstein zeichnen
                    text = font.render("Komputer gewinnt!", True, Settings.GREEN) #Text erstellen
                    screen.blit(text, (Settings.WINDOW_WIDTH//2 - text.get_width()//2, Settings.WINDOW_HEIGHT//2 - text.get_height()//2))
                    pygame.display.update() #Bildschirm refresh
                    pygame.time.wait(3000)  #3 Sekunden warten
                    screen.fill(Settings.BLACK) #Bildschirm löschen
                    pygame.display.update() #Bildschirm refresh
                    text = font.render("Weiterspielen? J / N", True, Settings.GREEN) #Text erstellen
                    screen.blit(text, (Settings.WINDOW_WIDTH//2 - text.get_width()//2, Settings.WINDOW_HEIGHT//2 - text.get_height()//2))
                    pygame.display.update() #Bildschirm refresh 
                    if wartenAufBtn(): #wartenAufBtn()
                        main()
                    else:
                        running = False  #Spiel beenden
                else:
                    zähler == 1
                    if zähler >= Settings.max_zug: #für den Fall 'Unentschieden'
                        board.draw(screen)  #Den Gewinnerstein zeichnen
                        text = font.render("Unentschieden", True, Settings.MAGENTA) #Text erstellen
                        screen.blit(text, (Settings.WINDOW_WIDTH//2 - text.get_width()//2, Settings.WINDOW_HEIGHT//2 - text.get_height()//2))
                        text = font.render("Weiterspielen? J / N", True, Settings.MAGENTA) #Text erstellen
                        screen.blit(text, (Settings.WINDOW_WIDTH//2 - text.get_width()//2, Settings.WINDOW_HEIGHT*0.80 - text.get_height()//2))
                        pygame.display.update() #Bildschirm refresh 
                        if wartenAufBtn(): #wartenAufBtn()
                            main()
                        else:
                            running = False  #Spiel beenden
                turn = 0  #Spieler ist als nächstes dran
    
            else:
                turn = 0  #Spieler ist als nächstes dran

    pygame.display.flip()  #Bildschirm aktualisieren
    clock.tick(Settings.FPS)  #FPS einhalten 
    pygame.quit()  #Wenn das Spiel zu Ende ist: Pygame beenden


if __name__ == "__main__": #Nur ausführen, wenn diese Datei gestartet wird
    main() #Hauptfunktion starten

#hilfsmitel: die Unterlagen aus dem ersten Schul-/ Halbjahr, hilfe von einem Familien mitgied
