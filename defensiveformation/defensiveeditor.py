from tkinter import *
from tkinter import messagebox

from defensiveformation.defensivevisualizer import DefensiveVisualizer
from misc.scoutcardmakerexceptions import ScoutCardMakerException


class DefensiveEditor(Frame):
    def __init__(self, root, controller):
        Frame.__init__(self, root)
        self.controller = controller
        controller.view = self

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(3, weight=1)

        offensive_formation_frame = Frame(self)
        Label(offensive_formation_frame, text='Offensive Formation:').pack()
        self.offensive_formation_entry = Entry(offensive_formation_frame)
        self.offensive_formation_entry.pack()
        self.get_offensive_formation_btn = Button(offensive_formation_frame, text='Get Offensive Formation', command=self.get_offensive_formation)
        self.get_offensive_formation_btn.pack()
        offensive_formation_frame.grid(row=0, column=0, stick=W)

        affected_defenders_frame = Frame(self)
        Label(affected_defenders_frame, text='Affected Defenders').grid(row = 0, column = 0)
        self.t_cb_value = BooleanVar()
        self.t_cb = Checkbutton(affected_defenders_frame, text='T', variable=self.t_cb_value, command=self.checked_affected_defenders_box)
        self.t_cb.grid(row=1, column=0, sticky=W)
        self.n_cb_value = BooleanVar()
        self.n_cb = Checkbutton(affected_defenders_frame, text='N', variable=self.n_cb_value, command=self.checked_affected_defenders_box)
        self.n_cb.grid(row=2, column=0, sticky=W)
        self.a_cb_value = BooleanVar()
        self.a_cb = Checkbutton(affected_defenders_frame, text='A', variable=self.a_cb_value, command=self.checked_affected_defenders_box)
        self.a_cb.grid(row=3, column=0, sticky=W)
        self.p_cb_value = BooleanVar()
        self.p_cb = Checkbutton(affected_defenders_frame, text='P', variable=self.p_cb_value, command=self.checked_affected_defenders_box)
        self.p_cb.grid(row=4, column=0, sticky=W)
        self.w_cb_value = BooleanVar()
        self.w_cb = Checkbutton(affected_defenders_frame, text='W', variable=self.w_cb_value, command=self.checked_affected_defenders_box)
        self.w_cb.grid(row=5, column=0, sticky=W)
        self.m_cb_value = BooleanVar()
        self.m_cb = Checkbutton(affected_defenders_frame, text='M', variable=self.m_cb_value, command=self.checked_affected_defenders_box)
        self.m_cb.grid(row=6, column=0, sticky=W)
        self.b_cb_value = BooleanVar()
        self.b_cb = Checkbutton(affected_defenders_frame, text='B', variable=self.b_cb_value, command=self.checked_affected_defenders_box)
        self.b_cb.grid(row=1, column=1, sticky=W)
        self.s_cb_value = BooleanVar()
        self.s_cb = Checkbutton(affected_defenders_frame, text='S', variable=self.s_cb_value, command=self.checked_affected_defenders_box)
        self.s_cb.grid(row=2, column=1, sticky=W)
        self.c_cb_value = BooleanVar()
        self.c_cb = Checkbutton(affected_defenders_frame, text='C', variable=self.c_cb_value, command=self.checked_affected_defenders_box)
        self.c_cb.grid(row=3, column=1, sticky=W)
        self.f_cb_value = BooleanVar()
        self.f_cb = Checkbutton(affected_defenders_frame, text='F', variable=self.f_cb_value, command=self.checked_affected_defenders_box)
        self.f_cb.grid(row=4, column=1, sticky=W)
        self.q_cb_value = BooleanVar()
        self.q_cb = Checkbutton(affected_defenders_frame, text='Q', variable=self.q_cb_value, command=self.checked_affected_defenders_box)
        self.q_cb.grid(row=5, column=1, sticky=W)
        self.set_affected_defender_checkboxes()
        affected_defenders_frame.grid(row=0, column=1, stick=W)


        defender_frame = Frame(self)
        defender_frame.grid(row=0, column=2, stick=E)

        Label(defender_frame, text='Current Defender :').grid(row=0, column=0, sticky=E)
        defender_names = self.controller.get_defender_names()
        self.current_defender_value = StringVar()
        self.current_defender_value.set(self.controller.current_defender.label)
        self.current_defender_om = OptionMenu(defender_frame, self.current_defender_value, *defender_names, command=self.change_defender)
        self.current_defender_om.grid(row=0, column=1, sticky=W+E)

        Label(defender_frame, text='Placement Rule :').grid(row=1, column=0, sticky=E)
        placement_rule_names = self.controller.get_placement_names()
        self.placement_rule_name_value = StringVar()
        self.placement_rule_name_value.set(controller.get_placement_rule_name_from_placement_rule(self.controller.current_defender.placement_rule))
        self.placement_rule_om = OptionMenu(defender_frame, self.placement_rule_name_value, *placement_rule_names, command=self.change_placement_rule)
        self.placement_rule_om.grid(row=1, column=1, sticky=W + E)


        self.defensive_visualizer = DefensiveVisualizer(self, controller)
        self.defensive_visualizer.grid(row = 1, column = 0, columnspan = 4, sticky=W+E+S+N)


        self.placement_rule_frame = None
        self.change_placement_rule_gui()


    def change_defender(self, *args):
        self.controller.set_current_defender(self.current_defender_value.get())
        self.placement_rule_name_value.set(self.controller.get_current_defender_placement_rule_name())
        self.change_placement_rule_gui()

    def change_placement_rule(self, *args):
        self.controller.change_placement_rule(self.placement_rule_name_value.get())
        self.change_placement_rule_gui()

    def change_placement_rule_gui(self):
        if self.placement_rule_frame:
            self.placement_rule_frame.grid_forget()
            self.placement_rule_frame.destroy()

        self.placement_rule_frame = self.controller.get_placement_rule_gui(self)
        self.placement_rule_frame.grid(row = 0, column = 3, sticky = W)
        self.update_view()

    def update_view(self):
        self.defensive_visualizer.visualize_formation_and_defense(self.controller.current_formation,
                                                                  self.controller.current_defense)

    def get_affected_defenders(self):
        affected_defender_tags = []
        if self.t_cb_value.get():
            affected_defender_tags.append('T')
        if self.n_cb_value.get():
            affected_defender_tags.append('N')
        if self.a_cb_value.get():
            affected_defender_tags.append('A')
        if self.p_cb_value.get():
            affected_defender_tags.append('P')
        if self.w_cb_value.get():
            affected_defender_tags.append('W')
        if self.m_cb_value.get():
            affected_defender_tags.append('M')
        if self.b_cb_value.get():
            affected_defender_tags.append('B')
        if self.s_cb_value.get():
            affected_defender_tags.append('S')
        if self.c_cb_value.get():
            affected_defender_tags.append('C')
        if self.f_cb_value.get():
            affected_defender_tags.append('F')
        if self.q_cb_value.get():
            affected_defender_tags.append('Q')
        return affected_defender_tags

    def set_affected_defender_checkboxes(self):
        self.t_cb_value.set(True if 'T' in self.controller.current_defense.affected_defender_tags else False)
        self.n_cb_value.set(True if 'N' in self.controller.current_defense.affected_defender_tags else False)
        self.a_cb_value.set(True if 'A' in self.controller.current_defense.affected_defender_tags else False)
        self.p_cb_value.set(True if 'P' in self.controller.current_defense.affected_defender_tags else False)
        self.w_cb_value.set(True if 'W' in self.controller.current_defense.affected_defender_tags else False)
        self.m_cb_value.set(True if 'M' in self.controller.current_defense.affected_defender_tags else False)
        self.b_cb_value.set(True if 'B' in self.controller.current_defense.affected_defender_tags else False)
        self.s_cb_value.set(True if 'S' in self.controller.current_defense.affected_defender_tags else False)
        self.c_cb_value.set(True if 'C' in self.controller.current_defense.affected_defender_tags else False)
        self.f_cb_value.set(True if 'F' in self.controller.current_defense.affected_defender_tags else False)
        self.q_cb_value.set(True if 'Q' in self.controller.current_defense.affected_defender_tags else False)

    def get_offensive_formation(self):
        try:
            self.controller.load_offensive_formation(self.offensive_formation_entry.get())
            self.update_view()
        except ScoutCardMakerException as e:
            messagebox.showerror('Load Formation Error', e)

    def checked_affected_defenders_box(self):
        self.controller.checked_affected_defenders_box(self.get_affected_defenders())


if __name__ == '__main__':
    from defensiveformation.defensecontroller import DefenseController
    root = Tk()
    controller = DefenseController()
    controller.formation_library.load_library('library1.scmfl')
    DefensiveEditor(root, controller).pack(fill=BOTH, expand=TRUE)
    root.state('zoomed')
    root.mainloop()

