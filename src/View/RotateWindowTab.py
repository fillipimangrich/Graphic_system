import tkinter as tk


class Rotation(tk.LabelFrame):
    def __init__(self, master, controller, view):
        super().__init__(
            master,
            width=50,
            height=50,
            bg="lightgray",
            padx=20,
            pady=5,
            text="Rotation",
        )

        self.selected = tk.StringVar()
        self.controller = controller
        self.view = view

        rotate_left_button = tk.Button(
            self, text="Rotate", font=("Arial", 10), command=self.rotate
        )

        label_angle = tk.Label(self, text="Angle:")
        label_angle.grid(row=0, column=0, padx=2, pady=5)

        self.entry_angle = tk.Entry(self, width=5)
        self.entry_angle.grid(row=0, column=1, columnspan=3, padx=2, pady=5)

        label_axis = tk.Label(self, text="Axis:")
        label_axis.grid(row=2, column=0, padx=2, pady=5)

        radio_x = tk.Radiobutton(
            self, text="x", value="x", variable=self.selected, anchor="w"
        )
        radio_y = tk.Radiobutton(
            self, text="y", value="y", variable=self.selected, anchor="w"
        )
        radio_z = tk.Radiobutton(
            self, text="z", value="z", variable=self.selected, anchor="w"
        )

        radio_x.grid(padx=1, row=2, column=1, sticky="w")
        radio_y.grid(padx=1, row=2, column=2, sticky="w")
        radio_z.grid(padx=1, row=2, column=3, sticky="w")

        radio_x.select()

        rotate_left_button.grid(row=4, column=0, columnspan=3, padx=2)

    def rotate(self):
        if self.entry_angle.get():
            angle = self.entry_angle.get()
            axis_direction = self.selected.get()
            self.controller.rotateWindow(int(angle), axis_direction)
            self.view.draw()
            self.master.destroy()
        else:
            self.controller.show_warning("No angle to rotate defined!")