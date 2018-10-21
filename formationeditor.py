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
        t_entry = Entry(player_edit_frame).grid(row=0, column=1)
        Label(player_edit_frame, text="H").grid(row=1, column=0)
        h_entry = Entry(player_edit_frame).grid(row=1, column=1)
        Label(player_edit_frame, text="X").grid(row=2, column=0)
        x_entry = Entry(player_edit_frame).grid(row=2, column=1)
        Label(player_edit_frame, text="Y").grid(row=3, column=0)
        y_entry = Entry(player_edit_frame).grid(row=3, column=1)
        Label(player_edit_frame, text="Z").grid(row=4, column=0)
        z_entry = Entry(player_edit_frame).grid(row=4, column=1)
        Label(player_edit_frame, text="Q").grid(row=5, column=0)
        q_entry = Entry(player_edit_frame).grid(row=5, column=1)

        formation_visualizer_frame = Frame(self)
        formation_visualizer_frame.pack(fill=BOTH, expand=TRUE)
        formation_visualizer = FormationVisualizer(formation_visualizer_frame, Formation())



root = Tk()
FormationEditor(root)
root.mainloop()
