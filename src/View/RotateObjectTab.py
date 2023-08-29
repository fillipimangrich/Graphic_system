import tkinter as tk

class RotateObjectTab(tk.Frame):
    def __init__(self, master, controller, object):
        super().__init__(master)
        self.controller = controller
        self.object = object
        self.point_container = None
        self.point_x = None
        self.point_y = None

        # Creates type elements
        type_container = tk.LabelFrame(self, text="Rotation Axis")
        self.selected = tk.StringVar()
        rb1 = tk.Radiobutton(
            type_container,
            text="X",
            value="x",
            variable=self.selected,
            command=self.select,
            anchor="w",
            takefocus=0,
        )
        rb2 = tk.Radiobutton(
            type_container,
            text="Y",
            value="y",
            variable=self.selected,
            command=self.select,
            anchor="w",
            takefocus=0,
        )
        rb3 = tk.Radiobutton(
            type_container,
            text="Z",
            value="z",
            variable=self.selected,
            command=self.select,
            anchor="w",
            takefocus=0,
        )
        rb4 = tk.Radiobutton(
            type_container,
            text="Custom Vector",
            value="custom",
            variable=self.selected,
            command=self.select,
            anchor="w",
            takefocus=0,
        )

        self.amount_container = tk.LabelFrame(self, text="Angle")
        self.amount = tk.Entry(self.amount_container, width=5)
        label = tk.Label(self.amount_container, text="°")

        self.point_container = tk.LabelFrame(self, text="Vector Coordinates")
        self.point_x = tk.Entry(self.point_container, state="disabled", width=5)
        self.point_y = tk.Entry(self.point_container, state="disabled", width=5)
        self.point_z = tk.Entry(self.point_container, state="disabled", width=5)
        label_x = tk.Label(self.point_container, text="x:")
        label_y = tk.Label(self.point_container, text="y:")
        label_z = tk.Label(self.point_container, text="z:")

        apply_button = tk.Button(
            self, text="Add", font=("Arial", 10), command=self.add_rotation
        )

        self.amount_container.grid(row=0, column=0, pady=15, padx=10, sticky="NW")
        type_container.grid(
            row=1, column=0, pady=15, padx=10, sticky="NW", columnspan=2
        )
        self.point_container.grid(
            row=0, column=1, pady=15, padx=10, columnspan=2, sticky="NW"
        )
        apply_button.grid(row=1, column=2, sticky="SE", pady=15, padx=10)
        label.grid(row=0, column=1, padx=5, pady=5)
        self.amount.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        rb1.grid(row=0, column=0, padx=5, sticky="W")
        rb2.grid(row=0, column=1, padx=5, sticky="W")
        rb3.grid(row=0, column=2, padx=5, sticky="W")
        rb4.grid(row=0, column=3, padx=5, sticky="W")

        label_x.grid(row=0, column=0, padx=5, pady=5)
        self.point_x.grid(row=0, column=1, padx=5, pady=5)

        label_y.grid(row=0, column=2, padx=5, pady=5)
        self.point_y.grid(row=0, column=3, padx=5, pady=5)

        label_z.grid(row=0, column=4, padx=5, pady=5)
        self.point_z.grid(row=0, column=5, padx=5, pady=5)

        rb1.select()

    def select(self):
        if self.selected.get() == "custom":
            self.point_x.config(state="normal")
            self.point_y.config(state="normal")
            self.point_z.config(state="normal")

        else:
            self.point_x.selection_clear()
            self.point_y.selection_clear()
            self.point_z.selection_clear()
            self.point_x.config(state="disabled")
            self.point_y.config(state="disabled")
            self.point_z.config(state="disabled")

    def add_rotation(self):
        if self.amount.get():
            angle = float(self.amount.get())
            if self.selected.get() == "custom":
                axis = (
                    float(self.point_x.get()),
                    float(self.point_y.get()),
                    float(self.point_z.get()),
                )
            else:
                axis = self.selected.get()

            type = "rotation"

            self.master.add_rotation(angle, axis, type)
        else:
            self.controller.show_warning("Angle field is required!")
