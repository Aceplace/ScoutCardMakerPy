from tkinter import *
from formationvisualizer import FormationVisualizer
from formation import Formation

class FormationEditor(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.pack(fill=BOTH, expand=TRUE)

        player_edit_frame = Frame(self, padx = 10, pady = 10)
        player_edit_frame.pack()
        Label(player_edit_frame, text="T").grid(row=0, column=0)
        self.t_entry = Entry(player_edit_frame)
        self.t_entry.grid(row=0, column=1)
        Label(player_edit_frame, text="H").grid(row=1, column=0)
        self.h_entry = Entry(player_edit_frame)
        self.h_entry.grid(row=1, column=1)
        Label(player_edit_frame, text="X").grid(row=2, column=0)
        self.x_entry = Entry(player_edit_frame)
        self.x_entry.grid(row=2, column=1)
        Label(player_edit_frame, text="Y").grid(row=3, column=0)
        self.y_entry = Entry(player_edit_frame)
        self.y_entry.grid(row=3, column=1)
        Label(player_edit_frame, text="Z").grid(row=4, column=0)
        self.z_entry = Entry(player_edit_frame)
        self.z_entry.grid(row=4, column=1)
        Label(player_edit_frame, text="Q").grid(row=5, column=0)
        self.q_entry = Entry(player_edit_frame)
        self.q_entry.grid(row=5, column=1)
        update_button = Button(player_edit_frame, text="Update Positions", command=lambda:self.update_positions())
        update_button.grid(row=6, column=0, columnspan=2)

        self.current_formation = Formation()

        formation_visualizer_frame = Frame(self)
        formation_visualizer_frame.pack(fill=BOTH, expand=TRUE)
        self.formation_visualizer = FormationVisualizer(formation_visualizer_frame)
        self.formation_visualizer.arrange_players_in_formation(self.current_formation)

        self.update_entry_boxes_with_coordinates()


        frame = Frame(root, bd=2, relief=SUNKEN)




    def update_positions(self):
        self.update_position(self.t_entry, 'T')
        self.update_position(self.h_entry, 'H')
        self.update_position(self.x_entry, 'X')
        self.update_position(self.y_entry, 'Y')
        self.update_position(self.z_entry, 'Z')
        self.update_position(self.q_entry, 'Q')

        self.formation_visualizer.arrange_players_in_formation(self.current_formation)
        self.update_entry_boxes_with_coordinates()

    def update_position(self, entry, label):
        coordinate_text = entry.get()
        #convert coordinates to numbers
        try:
            split_text = coordinate_text.split(',')
            x,y = None, None

            if len(split_text) != 2:
                raise ValueError('Coordinates not in proper format')
            x = int(split_text[0])
            y = int(split_text[1])

            self.current_formation.players[label].x = x
            self.current_formation.players[label].y = y
        except Exception: #Any exceptions will simply cause us to use the coordinates already in place
            pass



    def update_entry_boxes_with_coordinates(self):
        self.t_entry.delete(0, END)
        self.t_entry.insert(0, self.get_string_for_player_coordinates('T'))
        self.h_entry.delete(0, END)
        self.h_entry.insert(0, self.get_string_for_player_coordinates('H'))
        self.x_entry.delete(0, END)
        self.x_entry.insert(0, self.get_string_for_player_coordinates('X'))
        self.y_entry.delete(0, END)
        self.y_entry.insert(0, self.get_string_for_player_coordinates('Y'))
        self.z_entry.delete(0, END)
        self.z_entry.insert(0, self.get_string_for_player_coordinates('Z'))
        self.q_entry.delete(0, END)
        self.q_entry.insert(0, self.get_string_for_player_coordinates('Q'))


    def get_string_for_player_coordinates(self, label):
        return str(self.current_formation.players[label].x) + ',' + str(self.current_formation.players[label].y)













root = Tk()
FormationEditor(root)
root.mainloop()
