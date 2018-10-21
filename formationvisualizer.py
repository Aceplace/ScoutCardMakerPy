from tkinter import *
from formation import Formation

#Constant Values
CENTER_X_POS = 600
CENTER_Y_POS = 400
HORIZONTAL_COORDINATE_SIZE = 10
VERTICAL_COORDINATE_SIZE = 25
PLAYER_WIDTH = 26
PLAYER_HEIGHT = 20
LABEL_FONT = "Times 12"
HASH_SIZE = 5
#Derived Constant Values
LEFT_SIDELINE = CENTER_X_POS - HORIZONTAL_COORDINATE_SIZE * 53
RIGHT_SIDELINE = CENTER_X_POS + HORIZONTAL_COORDINATE_SIZE * 53
LEFT_HASH = CENTER_X_POS - HORIZONTAL_COORDINATE_SIZE * 18
RIGHT_HASH = CENTER_X_POS + HORIZONTAL_COORDINATE_SIZE * 18
LEFT_TOP_OF_NUMBERS = CENTER_X_POS - HORIZONTAL_COORDINATE_SIZE * 35
LEFT_BOTTOM_OF_NUMBERS = CENTER_X_POS - HORIZONTAL_COORDINATE_SIZE * 39
RIGHT_TUP_OF_NUMBERS = CENTER_X_POS + HORIZONTAL_COORDINATE_SIZE * 35
RIGHT_BOTTOM_OF_NUMBERS = CENTER_X_POS + HORIZONTAL_COORDINATE_SIZE * 39
FIVE_YARDS = VERTICAL_COORDINATE_SIZE * 5

class FormationVisualizer(Canvas):
    def __init__(self, root, formation):
        Canvas.__init__(self, root)
        self.configure(background="white")
        self.pack(fill=BOTH, expand=True)
        self.draw_field_lines()
        self.draw_players_in_formation(formation)

    def draw_field_lines(self):
        #draw sideline
        self.create_line(LEFT_SIDELINE, CENTER_Y_POS - FIVE_YARDS * 3, LEFT_SIDELINE, CENTER_Y_POS + FIVE_YARDS * 2)
        self.create_line(RIGHT_SIDELINE, CENTER_Y_POS - FIVE_YARDS * 3, RIGHT_SIDELINE, CENTER_Y_POS + FIVE_YARDS * 2)

        for num in range(-3, 3):
            #draw lines that go accross field at 5 yard intervals
            self.create_line(LEFT_SIDELINE, CENTER_Y_POS + FIVE_YARDS * num, RIGHT_SIDELINE, CENTER_Y_POS + FIVE_YARDS * num)
            #draw hash marks
            self.create_line(LEFT_HASH, CENTER_Y_POS + num * FIVE_YARDS - HASH_SIZE, LEFT_HASH, CENTER_Y_POS + num * FIVE_YARDS + HASH_SIZE)
            self.create_line(RIGHT_HASH, CENTER_Y_POS + num * FIVE_YARDS - HASH_SIZE, RIGHT_HASH, CENTER_Y_POS + num * FIVE_YARDS + HASH_SIZE)
            #draw ticks for the top of numbers and bottom of numbers
            self.create_line(LEFT_BOTTOM_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS - HASH_SIZE, LEFT_BOTTOM_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS + HASH_SIZE)
            self.create_line(LEFT_TOP_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS - HASH_SIZE, LEFT_TOP_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS + HASH_SIZE)
            self.create_line(RIGHT_BOTTOM_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS - HASH_SIZE, RIGHT_BOTTOM_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS + HASH_SIZE)
            self.create_line(RIGHT_TUP_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS - HASH_SIZE, RIGHT_TUP_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS + HASH_SIZE)

    def draw_players_in_formation(self, formation):
        for label, player in formation.players.items():
            x, y = FormationVisualizer.player_coordinates_to_canvas(player)
            self.create_oval(x - PLAYER_WIDTH / 2, y - PLAYER_HEIGHT / 2, x + PLAYER_WIDTH / 2, y + PLAYER_HEIGHT / 2,
                            fill="white")
            self.create_text(x, y, text=player.label, font=LABEL_FONT)


    @staticmethod
    def player_coordinates_to_canvas(player):
        return (CENTER_X_POS + player.x * HORIZONTAL_COORDINATE_SIZE, CENTER_Y_POS + player.y * VERTICAL_COORDINATE_SIZE)

if __name__ == "__main__":
    root = Tk()
    formation = Formation()
    fvc = FormationVisualizer(root, formation)
    root.mainloop()
