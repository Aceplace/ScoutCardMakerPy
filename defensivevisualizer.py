from tkinter import *
from offense.formation import Formation
from defense import Defense

#Constant Values
CENTER_X_POS = 600
CENTER_Y_POS = 400
HORIZONTAL_COORDINATE_SIZE = 10
VERTICAL_COORDINATE_SIZE = 25
PLAYER_WIDTH = 26
PLAYER_HEIGHT = 20
LABEL_FONT = "Times 12"
DEFENDER_FONT = "Times 18"
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


def player_coordinates_to_canvas(player_x, player_y):
    return (CENTER_X_POS + player_x * HORIZONTAL_COORDINATE_SIZE, CENTER_Y_POS + player_y * VERTICAL_COORDINATE_SIZE)

def defender_coordinates_to_canvas(defender_x, defender_y):
    return (CENTER_X_POS + defender_x * HORIZONTAL_COORDINATE_SIZE, CENTER_Y_POS + defender_y * VERTICAL_COORDINATE_SIZE * -1)


class DefensiveVisualizer(Frame):
    def __init__(self, root, controller):
        Frame.__init__(self, root)

        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        xscrollbar = Scrollbar(self, orient=HORIZONTAL)
        xscrollbar.grid(row=1, column=0, sticky=E+W)
        yscrollbar = Scrollbar(self)
        yscrollbar.grid(row=0, column=1, sticky=N+S)

        self.canvas = Canvas(self, bd=0, xscrollcommand=xscrollbar.set, background='white',
                        yscrollcommand=yscrollbar.set, scrollregion=(0,0,1200,800))
        self.canvas.grid(row=0, column=0, sticky=N+S+E+W)
        xscrollbar.config(command=self.canvas.xview)
        yscrollbar.config(command=self.canvas.yview)

        self.draw_field_lines()
        self.create_player_shapes_for_visualization()

        self.visualize_formation_and_defense(self.controller.current_formation, self.controller.current_defense)


    def draw_field_lines(self):
        #draw sideline
        self.canvas.create_line(LEFT_SIDELINE, CENTER_Y_POS - FIVE_YARDS * 3, LEFT_SIDELINE, CENTER_Y_POS + FIVE_YARDS * 2)
        self.canvas.create_line(RIGHT_SIDELINE, CENTER_Y_POS - FIVE_YARDS * 3, RIGHT_SIDELINE, CENTER_Y_POS + FIVE_YARDS * 2)

        for num in range(-3, 3):
            #draw lines that go accross field at 5 yard intervals
            self.canvas.create_line(LEFT_SIDELINE, CENTER_Y_POS + FIVE_YARDS * num, RIGHT_SIDELINE, CENTER_Y_POS + FIVE_YARDS * num)
            #draw hash marks
            self.canvas.create_line(LEFT_HASH, CENTER_Y_POS + num * FIVE_YARDS - HASH_SIZE, LEFT_HASH, CENTER_Y_POS + num * FIVE_YARDS + HASH_SIZE)
            self.canvas.create_line(RIGHT_HASH, CENTER_Y_POS + num * FIVE_YARDS - HASH_SIZE, RIGHT_HASH, CENTER_Y_POS + num * FIVE_YARDS + HASH_SIZE)
            #draw ticks for the top of numbers and bottom of numbers
            self.canvas.create_line(LEFT_BOTTOM_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS - HASH_SIZE, LEFT_BOTTOM_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS + HASH_SIZE)
            self.canvas.create_line(LEFT_TOP_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS - HASH_SIZE, LEFT_TOP_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS + HASH_SIZE)
            self.canvas.create_line(RIGHT_BOTTOM_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS - HASH_SIZE, RIGHT_BOTTOM_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS + HASH_SIZE)
            self.canvas.create_line(RIGHT_TUP_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS - HASH_SIZE, RIGHT_TUP_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS + HASH_SIZE)

    def create_player_shapes_for_visualization(self):
        self.player_shapes = {}
        formation = Formation() #create default formation to place players around in
        for label, player in formation.players.items():
            x, y = player_coordinates_to_canvas(player.x, player.y)
            self.player_shapes[label] = {"Oval" : self.canvas.create_oval(x - PLAYER_WIDTH / 2, y - PLAYER_HEIGHT / 2, x + PLAYER_WIDTH / 2, y + PLAYER_HEIGHT / 2, fill="white"),
                                        "Text" : self.canvas.create_text(x, y, text=player.label, font=LABEL_FONT),
                                        "Label" : player.label}
        defense = Defense() #create default formation to place defenders around in
        self.defender_shapes = {}
        for label, defender in defense.defenders.items():
            x, y = defender_coordinates_to_canvas(*defender.place_defender(formation))
            self.defender_shapes[label] = {'Text' : self.canvas.create_text(x, y, text=defender.label, font=DEFENDER_FONT),
                                        'Label' : player.label }

    def visualize_formation_and_defense(self, formation, defense):
        for label, player in formation.players.items():
            x, y = player_coordinates_to_canvas(player.x, player.y)
            self.canvas.coords(self.player_shapes[label]["Oval"], x - PLAYER_WIDTH / 2, y - PLAYER_HEIGHT / 2, x + PLAYER_WIDTH / 2, y + PLAYER_HEIGHT / 2)
            self.canvas.coords(self.player_shapes[label]["Text"], x, y)
        for label, defender in defense.defenders.items():
            x, y = defender_coordinates_to_canvas(*defender.place_defender(formation))
            self.canvas.coords(self.defender_shapes[label]["Text"], x, y)


class MockController:
    def __init__(self):
        self.current_formation = Formation()
        self.current_formation.flip_formation()
        self.current_formation.y.x = -25
        self.current_formation.x.x = 12
        self.current_defense = Defense()

if __name__ == '__main__':
    root = Tk()
    root.state('zoomed')
    visualizer = DefensiveVisualizer(root, MockController())
    visualizer.pack(fill=BOTH, expand=True)
    root.mainloop()