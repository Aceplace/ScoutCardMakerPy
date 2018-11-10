from tkinter import *
from defensiveformation.defensiveeditor import DefensiveEditor

class DefensiveLibraryEditor(Frame):
    def __init__(self, root, controller):
        Frame.__init__(self, root)

        self.controller = controller

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        defense_name_frame = Frame(self)
        Label(defense_name_frame, text='Defense Name').pack()
        self.defense_name_entry = Entry(defense_name_frame)
        self.defense_name_entry.pack()
        self.save_defense_btn = Button(defense_name_frame, text='Save Defense', command=self.save_defense)
        self.save_defense_btn.pack()
        Label(defense_name_frame, text='Composite Defense').pack()
        self.composite_defense_entry = Entry(defense_name_frame)
        self.composite_defense_entry.pack()
        self.load_composite_btn = Button(defense_name_frame, text='Load Defense', command=self.load_composite_defense)
        self.load_composite_btn.pack()
        defense_name_frame.grid(row=0, column=0, sticky=W)

        defense_library_list_frame = Frame(self)
        Label(defense_library_list_frame, text='Defenses').pack()
        self.delete_selected_btn = Button(defense_library_list_frame, text='Delete Selected Defense', command=self.delete_selected_defense)
        self.delete_selected_btn.pack()
        defense_library_scrollbar = Scrollbar(defense_library_list_frame, orient=VERTICAL)
        self.defense_library_lb = Listbox(defense_library_list_frame, yscrollcommand=defense_library_scrollbar.set)
        defense_library_scrollbar.config(command=self.defense_library_lb.yview)
        defense_library_scrollbar.pack(side=RIGHT, fill=Y, expand=True)
        self.defense_library_lb.pack(side=LEFT, fill=Y, expand=True)
        self.defense_library_lb.bind('<<ListboxSelect>>', lambda e: self.defense_library_on_select(e))
        defense_library_list_frame.grid(row=1, column=0, sticky=N+S)

        defense_editor_frame = Frame(self)
        self.defense_editor = DefensiveEditor(defense_editor_frame, self.controller)
        self.defense_editor.pack(fill=BOTH, expand=True)
        defense_editor_frame.grid(row=0, column=1, rowspan=2, sticky=N+S+E+W)


    def save_defense(self):
        pass

    def load_composite_defense(self):
        pass

    def delete_selected_defense(self):
        pass

    def defense_library_on_select(self, event):
        listbox = event.widget
        #if listbox.curselection():
        #    index = listbox.curselection()[0]
        #    self.controller.load_formation_from_library(listbox.get(index))
        #    self.t_cb_value.set(True if 'T' in self.controller.current_formation.affected_player_tags else False)
        #    self.h_cb_value.set(True if 'H' in self.controller.current_formation.affected_player_tags else False)
        #    self.x_cb_value.set(True if 'X' in self.controller.current_formation.affected_player_tags else False)
        #    self.y_cb_value.set(True if 'Y' in self.controller.current_formation.affected_player_tags else False)
        #    self.z_cb_value.set(True if 'Z' in self.controller.current_formation.affected_player_tags else False)
        #    self.q_cb_value.set(True if 'Q' in self.controller.current_formation.affected_player_tags else False)
        #    self.formation_visual_editor.visualize_formation(self.controller.current_formation)


if __name__ == '__main__':
    from defensiveformation.defensiveeditorcontroller import DefensiveEditorController
    root = Tk()
    controller = DefensiveEditorController()
    controller.current_formation_library.load_library('library1.scmfl')
    DefensiveLibraryEditor(root, controller).pack(fill=BOTH, expand=TRUE)
    root.state('zoomed')
    root.mainloop()