from tkinter import *
from tkinter import messagebox
from formationvisualeditor import FormationVisualEditor
from scoutcardmakerexceptions import *



class FormationLibraryEditor(Frame):
    def __init__(self, root, controller):
        Frame.__init__(self, root)

        self.controller = controller

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        formation_entry_frame = Frame(self)
        Label(formation_entry_frame, text='Formation Name:').pack()
        self.formation_name_entry = Entry(formation_entry_frame)
        self.formation_name_entry.pack()
        self.save_formation_btn = Button(formation_entry_frame, text='Save Formation', command=self.save_formation)
        self.save_formation_btn.pack()
        Label(formation_entry_frame, text='Composite Name:').pack()
        self.composite_name_entry = Entry(formation_entry_frame)
        self.composite_name_entry.pack()
        self.load_composite_btm = Button(formation_entry_frame, text='Load Composite', command=self.load_composite_formation)
        self.load_composite_btm.pack()
        formation_entry_frame.grid(row=0, column=0)

        override_checkboxes_frame = Frame(self)
        self.is_override_cb_value = BooleanVar()
        self.is_override_cb = Checkbutton(override_checkboxes_frame, text='Override Formation', variable=self.is_override_cb_value)
        self.is_override_cb.pack(anchor=W)
        self.t_cb_value = BooleanVar()
        self.t_cb = Checkbutton(override_checkboxes_frame, text='T', variable=self.t_cb_value)
        self.t_cb.pack(anchor=W)
        self.h_cb_value = BooleanVar()
        self.h_cb = Checkbutton(override_checkboxes_frame, text='H', variable=self.h_cb_value)
        self.h_cb.pack(anchor=W)
        self.x_cb_value = BooleanVar()
        self.x_cb = Checkbutton(override_checkboxes_frame, text='X', variable=self.x_cb_value)
        self.x_cb.pack(anchor=W)
        self.y_cb_value = BooleanVar()
        self.y_cb = Checkbutton(override_checkboxes_frame, text='Y', variable=self.y_cb_value)
        self.y_cb.pack(anchor=W)
        self.z_cb_value = BooleanVar()
        self.z_cb = Checkbutton(override_checkboxes_frame, text='Z', variable=self.z_cb_value)
        self.z_cb.pack(anchor=W)
        self.q_cb_value = BooleanVar()
        self.q_cb = Checkbutton(override_checkboxes_frame, text='Q', variable=self.q_cb_value)
        self.q_cb.pack(anchor=W)
        override_checkboxes_frame.grid(row=0, column=1, stick=W)

        formation_library_frame = Frame(self)
        Label(formation_library_frame, text='Formations').pack()
        self.delete_selected_btn = Button(formation_library_frame, text='Delete Selected Formation')
        self.delete_selected_btn.pack()
        library_scrollbar = Scrollbar(formation_library_frame, orient=VERTICAL)
        self.library_lb = Listbox(formation_library_frame, yscrollcommand=library_scrollbar.set)
        library_scrollbar.config(command=self.library_lb.yview)
        library_scrollbar.pack(side=RIGHT, fill=Y, expand=True)
        self.library_lb.pack(side=LEFT, fill=Y, expand=True)
        formation_library_frame.grid(row=1, column=0, stick=N+S)
        self.library_lb.bind('<<ListboxSelect>>', lambda e:self.library_on_select(e))

        self.formation_visual_editor = FormationVisualEditor(self, self.controller)
        self.formation_visual_editor.grid(row=1, column=1, stick=N+S+E+W)

        self.refresh_library_listbox()

        self.pack(fill=BOTH, expand=True)

    def library_on_select(self, event):
        listbox = event.widget
        if listbox.curselection():
            index = listbox.curselection()[0]
            self.controller.load_formation_from_library(listbox.get(index))
            self.formation_visual_editor.visualize_formation(self.controller.current_formation)

    def save_formation(self):
        try:
            is_override_formation = self.is_override_cb_value.get()

            override_player_tags = []
            if self.t_cb_value.get():
                override_player_tags.append('T')
            if self.h_cb_value.get():
                override_player_tags.append('H')
            if self.x_cb_value.get():
                override_player_tags.append('X')
            if self.y_cb_value.get():
                override_player_tags.append('Y')
            if self.z_cb_value.get():
                override_player_tags.append('Z')
            if self.q_cb_value.get():
                override_player_tags.append('Q')

            self.controller.save_formation_to_library(self.formation_name_entry.get(), is_override_formation, override_player_tags)
            self.refresh_library_listbox()

        except ScoutCardMakerException as e:
            messagebox.showerror('Save Formation Error', e)

    def load_composite_formation(self):
        try:
            self.controller.load_composite_formation_from_library(self.composite_name_entry.get())
            self.formation_visual_editor.visualize_formation(self.controller.current_formation)
        except ScoutCardMakerException as e:
            messagebox.showerror('Load Composite Error', e)




    def refresh_library_listbox(self):
        formations = self.controller.formation_library.get_sorted_formation_names_right()
        self.library_lb.delete(0, END)
        for formation in formations:
            self.library_lb.insert(END, formation)




from formationlibrary import FormationLibrary
from libraryeditorcontroller import LibraryEditorController
from formation import Formation

if __name__ == '__main__':

    root = Tk()
    library = FormationLibrary()
    library.load_library('formations.scmfl')

    formations = sorted([formation_name for formation_name in library.formations.keys() ])

    libraryeditor = FormationLibraryEditor(root, LibraryEditorController(library))

    print(formations)


    root.mainloop()
