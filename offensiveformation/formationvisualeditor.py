from tkinter import *
from offensiveformation.formation import Formation

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


def player_coordinates_to_canvas(player_x, player_y):
    return (CENTER_X_POS + player_x * HORIZONTAL_COORDINATE_SIZE, CENTER_Y_POS + player_y * VERTICAL_COORDINATE_SIZE)

def canvas_coordinates_to_player(player_x, player_y):
    return (int((player_x - CENTER_X_POS) / HORIZONTAL_COORDINATE_SIZE), int((player_y - CENTER_Y_POS) / VERTICAL_COORDINATE_SIZE))


class FormationVisualEditor(Frame):
    def __init__(self, root, controller):
        Frame.__init__(self, root)
        #self.pack(fill=BOTH, expand=TRUE)

        self.controller = controller

        #self.formation_visualizer_frame.pack(fill=BOTH, expand=TRUE)

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

        #self.pack(fill=BOTH, expand=True)

        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<B1-Motion>", self.on_move)

        self.visualize_formation(self.controller.current_formation)


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

    def visualize_formation(self, formation):
        for label, player in formation.players.items():
            x, y = player_coordinates_to_canvas(player.x, player.y)
            self.canvas.coords(self.player_shapes[label]["Oval"], x - PLAYER_WIDTH / 2, y - PLAYER_HEIGHT / 2, x + PLAYER_WIDTH / 2, y + PLAYER_HEIGHT / 2)
            self.canvas.coords(self.player_shapes[label]["Text"], x, y)

    def on_press(self, event): #get initial location of object to be moved
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        drag_items = self.canvas.find_overlapping(x-1, y-1, x+1, y+1)
        if drag_items:
            player_drag_item = self.select_player_to_drag(drag_items)
            self.drag_data["item"] = player_drag_item
            self.drag_data["x"] = x
            self.drag_data["y"] = y
        else:
            self.drag_data["item"] = None
            self.drag_data["x"] = 0
            self.drag_data["y"] = 0

    def on_release(self, event): #reset data on release
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

    def on_move(self, event):
        if self.drag_data["item"]:
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            delta_x = x - self.drag_data["x"]
            delta_y = y - self.drag_data["y"]
            # move the object the appropriate amount
            if abs(delta_x) > HORIZONTAL_COORDINATE_SIZE:
                move_x = int(delta_x / HORIZONTAL_COORDINATE_SIZE) * HORIZONTAL_COORDINATE_SIZE
                self.canvas.move(self.drag_data["item"]["Oval"], move_x, 0)
                self.canvas.move(self.drag_data["item"]["Text"], move_x, 0)
                self.drag_data["x"] = self.drag_data["x"] + move_x
                self.controller.update_player_in_formation(self.drag_data["item"]["Label"], *self.visualizer_coordinates_to_formation_coordinates(self.drag_data["item"]["Text"]))
            if abs(delta_y) > VERTICAL_COORDINATE_SIZE:
                move_y = int(delta_y / VERTICAL_COORDINATE_SIZE) * VERTICAL_COORDINATE_SIZE
                self.canvas.move(self.drag_data["item"]["Oval"], 0, move_y)
                self.canvas.move(self.drag_data["item"]["Text"], 0, move_y)
                self.drag_data["y"] = self.drag_data["y"] + move_y
                self.controller.update_player_in_formation(self.drag_data["item"]["Label"], *self.visualizer_coordinates_to_formation_coordinates(self.drag_data["item"]["Text"]))

    def select_player_to_drag(self, drag_items):
        for drag_item in drag_items:
            for player in self.player_shapes.values():
                if drag_item is player["Oval"] or drag_item is player["Text"]:
                    return player
        return None

    def visualizer_coordinates_to_formation_coordinates(self, player_text):
        coordinates = self.canvas.coords(player_text)
        return canvas_coordinates_to_player(coordinates[0], coordinates[1])
