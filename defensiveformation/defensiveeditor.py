from tkinter import *
from defensiveformation.defensivevisualizer import DefensiveVisualizer

class DefensiveEditor(Frame):
    def __init__(self, root, controller):
        Frame.__init__(self, root)
        self.controller = controller
        controller.view = self

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        affected_defenders_frame = Frame(self)
        Label(affected_defenders_frame, text='Affected Defenders').grid(row = 0, column = 0)
        self.t_cb_value = BooleanVar()
        self.t_cb = Checkbutton(affected_defenders_frame, text='T', variable=self.t_cb_value)
        self.t_cb.grid(row=1, column=0, sticky=W)
        self.n_cb_value = BooleanVar()
        self.n_cb = Checkbutton(affected_defenders_frame, text='N', variable=self.n_cb_value)
        self.n_cb.grid(row=2, column=0, sticky=W)
        self.a_cb_value = BooleanVar()
        self.a_cb = Checkbutton(affected_defenders_frame, text='A', variable=self.a_cb_value)
        self.a_cb.grid(row=3, column=0, sticky=W)
        self.p_cb_value = BooleanVar()
        self.p_cb = Checkbutton(affected_defenders_frame, text='P', variable=self.p_cb_value)
        self.p_cb.grid(row=4, column=0, sticky=W)
        self.w_cb_value = BooleanVar()
        self.w_cb = Checkbutton(affected_defenders_frame, text='W', variable=self.w_cb_value)
        self.w_cb.grid(row=5, column=0, sticky=W)
        self.m_cb_value = BooleanVar()
        self.m_cb = Checkbutton(affected_defenders_frame, text='M', variable=self.m_cb_value)
        self.m_cb.grid(row=6, column=0, sticky=W)
        self.b_cb_value = BooleanVar()
        self.b_cb = Checkbutton(affected_defenders_frame, text='B', variable=self.b_cb_value)
        self.b_cb.grid(row=1, column=1, sticky=W)
        self.s_cb_value = BooleanVar()
        self.s_cb = Checkbutton(affected_defenders_frame, text='S', variable=self.s_cb_value)
        self.s_cb.grid(row=2, column=1, sticky=W)
        self.c_cb_value = BooleanVar()
        self.c_cb = Checkbutton(affected_defenders_frame, text='C', variable=self.c_cb_value)
        self.c_cb.grid(row=3, column=1, sticky=W)
        self.f_cb_value = BooleanVar()
        self.f_cb = Checkbutton(affected_defenders_frame, text='F', variable=self.f_cb_value)
        self.f_cb.grid(row=4, column=1, sticky=W)
        self.q_cb_value = BooleanVar()
        self.q_cb = Checkbutton(affected_defenders_frame, text='Q', variable=self.q_cb_value)
        self.q_cb.grid(row=5, column=1, sticky=W)

        affected_defenders_frame.grid(row=0, column=0, stick=W)


        defender_frame = Frame(self)
        defender_frame.grid(row=0, column=1, stick=E)

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
        self.defensive_visualizer.grid(row = 1, column = 0, columnspan = 3, sticky=W+E+S+N)


        self.placement_rule_frame = None
        self.change_placement_rule_gui()


    def change_defender(self, *args):
        self.controller.set_current_defender(self.current_defender_value.get())
        self.change_placement_rule_gui()

    def change_placement_rule(self, *args):
        self.controller.change_placement_rule(self.placement_rule_name_value.get())
        self.change_placement_rule_gui()

    def change_placement_rule_gui(self):
        if self.placement_rule_frame:
            self.placement_rule_frame.grid_forget()
            self.placement_rule_frame.destroy()

        self.placement_rule_frame = self.controller.get_placement_rule_gui(self)
        self.placement_rule_frame.grid(row = 0, column = 2, sticky = W)
        self.update_view()

    def update_view(self):
        self.defensive_visualizer.visualize_formation_and_defense(self.controller.current_formation,
                                                                  self.controller.current_defense)


if __name__ == '__main__':
    from defensiveformation.defensiveeditorcontroller import DefensiveEditorController
    root = Tk()
    controller = DefensiveEditorController()
    DefensiveEditor(root, controller).pack(fill=BOTH, expand=TRUE)
    root.mainloop()

