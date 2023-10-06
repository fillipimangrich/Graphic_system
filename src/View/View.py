import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter.colorchooser import askcolor
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askstring
from src.View.ChoiceDialog import ChoiceDialog
from src.View.RotateWindowTab import Rotation
from src.Controllers.Controller import Controller
from src.shapes.Point import Point
from src.shapes.Line import Line
from src.shapes.WireFrame import WireFrame
from src.Helpers.MatrixHelper import MatrixHelper
from src.Helpers.DescritorOBJ import DescritorOBJ
from src.View.TransformObjectsView import TransformObjectsView


class View(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.__controller = Controller()
        self.__line_width = 3
        self.__drawing_object = "Point"
        self.__points_counter = 0
        self.__object_name = "Wireframe 1"
        self.__last_mode_choice = "Arame"

    def run(self) -> None:
        self.geometry("1280x720")
        self.configure(bg = "#2D2D2D")
        self.setViewPort()
        self.setLogOfActionsView()
        self.setListOfObjectsView()
        self.setControlView()
        self.setAddObjectButton()
        self.setRotationWindowButton()
        self.setOBJButton()
        self.setClippingAlghoritmsButtons()

        self.mainloop()
    

    def on_algorithm_selected(self, evt):
        self.__controller.chosen_clipping_algorithm = self.__algorithm_combobox.get()


    def setClippingAlghoritmsButtons(self):
        algorithms = ["Cohen–Sutherland", "Liang-Barsky"]
        algorithm_label = tk.Label(self.__control, text="Line Clipping Method", bg="#565656", fg="#FFFFFF")  # Ajuste as cores de fundo (bg) e texto (fg) conforme necessário.
        algorithm_label.place(x=10, y=300)
        self.__algorithm_combobox = ttk.Combobox(self.__control, values=algorithms)
        self.__algorithm_combobox.place(x=10, y=320)
        self.__algorithm_combobox.set(self.__controller.chosen_clipping_algorithm)  # Valor padrão
        self.__algorithm_combobox.bind("<<ComboboxSelected>>", self.on_algorithm_selected)


    def setDrawingObject(self, drawing_object, popup):
        self.__drawing_object = drawing_object
        self.__points_counter = 0
        popup.destroy()

    def setViewPort(self) -> None:
        self.__view_port = tk.Canvas(
            self,bg = "#FFFFFF",height = 460,width = 920,bd = 0,highlightthickness = 0,relief = "ridge")
        self.__view_port.place(x=340, y=20)
        self.__view_port.bind("<Button-1>", self.draw)
        self.bind("<Left>", self.arrow_key_pressed)
        self.bind("<Right>", self.arrow_key_pressed)
        self.bind("<Up>", self.arrow_key_pressed)
        self.bind("<Down>", self.arrow_key_pressed)
        self.bind("<MouseWheel>", self.zoom)

        self.__view_port.create_rectangle(50,50,870,410, outline='red')


        #TO DO: DRAW THE LINE BASED IN THE POSITION OF THE CURSOR

        # self.__view_port.bind("<B1-Motion>", self.draw)


    def setLogOfActionsView(self) -> None:
        self.log_frame = tk.Frame(self)
        self.log_frame.place(x=340, y=500, width=920, height=200)

        self.scroll_y = tk.Scrollbar(self.log_frame, orient="vertical")
        self.scroll_y.pack(side="right", fill="y")

        self.__log_actions_view = tk.Canvas(
            self.log_frame, bg="#FFFFFF", bd=0, highlightthickness=0, relief="ridge", yscrollcommand=self.scroll_y.set)
        self.__log_actions_view.pack(side="left", fill="both", expand=True)

        self.scroll_y.config(command=self.__log_actions_view.yview)

        self.log_y_position = 10
    
    def setListOfObjectsView(self) -> None:

        frame = tk.Frame(self)
        frame.grid(padx=20, pady=20, row=0, column=0)

        self.__list_of_objects_view = tk.Canvas(
            frame, bg="#FFFFFF", height=240, width=280, bd=0, highlightthickness=0, relief="ridge")
        self.__list_of_objects_view.pack(side="left", fill="y")

        scroll_y = tk.Scrollbar(frame, orient="vertical", command=self.__list_of_objects_view.yview)
        scroll_y.pack(side="right", fill="y")

        self.__list_of_objects_view.configure(yscrollcommand=scroll_y.set)

        self.__object_list_items = {}
        self.__list_y_position = 10


    def setControlView(self) -> None:
        self.__control = tk.Canvas(
            self,bg = "#565656",height = 420,width = 300,bd = 0,highlightthickness = 0,relief = "ridge")
        self.__control.place(x=20, y=280)
        self.setAddObjectButton()
        self.setZoomButtons()
        self.setMoveButtons()

    def setAddObjectButton(self) -> None:
        self.__add_object_button = tk.PhotoImage(file = f"src/Images/add_button.png")
        button_add = self.__control.create_image(230, 50, image=self.__add_object_button)
        self.__control.tag_bind(button_add, "<Button-1>", lambda x: self.openViewForAddNewShape())


    def setOBJButton(self) -> None:
        self.__obj_button = tk.PhotoImage(file = f"src/Images/open_obj_button.png")
        button_obj_window = self.__control.create_image(150, 250, image=self.__obj_button)
        self.__control.tag_bind(button_obj_window, "<Button-1>", lambda x: self.openOBJPopup())


    def openOBJPopup(self):
        path = filedialog.askopenfilename(initialdir="/", title="Select file",
                    filetypes=(("obj files", "*.obj"),("all files", "*.*")))
        self.descriptor = DescritorOBJ()
        name, points = self.descriptor.parseOBJ(path)
        wire_frame = WireFrame(name, points, 'Arame')
        x,y,z,w = self.__controller.getViewport().getWindow().getCenter()-wire_frame.calcObjectCenter()
        wire_frame.transform(MatrixHelper.getTranslationMatrix(x,y,z))
        self.__controller.addObject(wire_frame)
        self.addObjectToList(wire_frame)

        self.draw()

    def setRotationWindowButton(self) -> None:
        self.__rotation_window_button = tk.PhotoImage(file = f"src/Images/rotate_button.png")
        button_rotation_window = self.__control.create_image(150, 150, image=self.__rotation_window_button)
        self.__control.tag_bind(button_rotation_window, "<Button-1>", lambda x: self.openRotationWindowPopup())
        self.__rotation_left = tk.PhotoImage(file = f"src/Images/rotate_left.png")
        button_rotation_window_left = self.__control.create_image(30, 160, image=self.__rotation_left)
        self.__control.tag_bind(button_rotation_window_left, "<Button-1>", lambda x: self.rotate(-30,"z"))
        self.__rotation_right = tk.PhotoImage(file = f"src/Images/rotate_right.png")
        button_rotation_window_right = self.__control.create_image(270, 160, image=self.__rotation_right)
        self.__control.tag_bind(button_rotation_window_right, "<Button-1>", lambda x: self.rotate(30,"z"))

    def rotate(self, angle, axis):
        self.__controller.rotateWindow(angle, axis)
        self.draw()

    def openRotationWindowPopup(self):
        popup = tk.Toplevel(self.__control)
        popup.title("Rotation")
        self.navigation = Rotation(popup, self.__controller, self)
        self.navigation.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.draw()

    def openViewForAddNewShape(self) -> None:
        popup = tk.Toplevel()
        popup.title("Opções")

        point_button = tk.Button(popup, text="Ponto", command=lambda: self.setDrawingObject("Point", popup))
        point_button.pack(pady=10)

        line_button = tk.Button(popup, text="Reta", command=lambda: self.setDrawingObject("Line", popup))
        line_button.pack(pady=10)

        wire_frame_button = tk.Button(popup, text="Wire Frame", command=lambda: self.setDrawingObject("Wire Frame", popup))
        wire_frame_button.pack(pady=10)

        
    def setZoomButtons(self) -> None:
        self.__zoom_in_button = tk.PhotoImage(file=f"src/Images/zoomIn.png")
        button_zoom_in = self.__control.create_image(20, 25, image = self.__zoom_in_button)
        self.__control.tag_bind(button_zoom_in, "<Button-1>", lambda x: self.zoom(type('event', (object,), {'delta': 1})()))
        
        self.__zoon_out_button = tk.PhotoImage(file =f"src/Images/zoomOut.png")
        button_zoom_out = self.__control.create_image(20, 70, image = self.__zoon_out_button)
        self.__control.tag_bind(button_zoom_out, "<Button-1>", lambda x: self.zoom(type('event', (object,), {'delta': 0})()) )

    def setMoveButtons(self) -> None:
        self.__move_up = tk.PhotoImage(file=f"src/Images/up.png")
        button_move_up = self.__control.create_image(100, 25, image = self.__move_up)
        self.__control.tag_bind(button_move_up, "<Button-1>", lambda x: self.moveUp() )

        self.__move_down = tk.PhotoImage(file=f"src/Images/down.png")
        button_move_down = self.__control.create_image(100, 70, image = self.__move_down)
        self.__control.tag_bind(button_move_down, "<Button-1>", lambda x: self.moveDown() )

        self.__move_right = tk.PhotoImage(file=f"src/Images/right.png")
        button_move_right = self.__control.create_image(140, 47, image = self.__move_right)
        self.__control.tag_bind(button_move_right, "<Button-1>", lambda x: self.moveRight() )

        self.__move_left = tk.PhotoImage(file=f"src/Images/left.png")
        button_move_left = self.__control.create_image(60, 47, image = self.__move_left)
        self.__control.tag_bind(button_move_left, "<Button-1>", lambda x: self.moveLeft() )

    def addLogs(self, message: str) -> None:
        self.__log_actions_view.create_text(10, self.log_y_position, text=message, anchor="w")
        self.log_y_position += 20

        self.__log_actions_view.config(scrollregion=self.__log_actions_view.bbox("all"))
        self.__log_actions_view.yview_moveto(1)
    
    def update_mesage(self):
        self._canvas.itemconfig(self.mesage_var, text =self._mensagem)
    
    def addObjectToList(self, obj):
        tag = obj.getId()
        name = obj.getName()
        x = 10
        y = self.__list_y_position 
        
        rectangle = self.__list_of_objects_view.create_rectangle(x,y,x+260,y+20, outline="#000000", fill="#D9D9D9")
        canvas_id = self.__list_of_objects_view.create_text(150, y+10, text=name, anchor=tk.CENTER, tags=(tag,))

        self.__object_list_items[tag] = (canvas_id, obj)

        self.__list_of_objects_view.tag_bind(canvas_id, "<Button-1>", lambda event, obj=obj: self.onObjectClicked(obj))
        self.__list_of_objects_view.tag_bind(rectangle, "<Button-1>", lambda event, obj=obj: self.onObjectClicked(obj))

        self.__list_y_position += 22

        self.__list_of_objects_view.config(scrollregion=self.__list_of_objects_view.bbox("all"))
        self.__list_of_objects_view.yview_moveto(1)

    def onObjectClicked(self, obj):
        popup = tk.Toplevel()
        popup.title("Opções")

        delete_button = tk.Button(popup, text="Apagar objeto", command=lambda: self.deleteObject(obj, popup))
        delete_button.pack(pady=10)

        color_button = tk.Button(popup, text="Trocar Cor", command=lambda: self.changeObjectColor(obj, popup))
        color_button.pack(pady=10)

        transformation_button = tk.Button(popup, text="Transformar", command=lambda: self.transformObject(obj, popup))
        transformation_button.pack(pady=10)

    def redrawObjectList(self):
        self.__list_of_objects_view.delete("all")

        self.__list_y_position = 10 

        for tag, (_, obj) in self.__object_list_items.items():
            self.addObjectToList(obj)

    def deleteObject(self, obj, popup):
        tag = obj.getId()     
        if tag in self.__object_list_items:
            del self.__object_list_items[tag]

        self.__controller.removeObject(obj)     
        self.addLogs('Apagou objeto ' + obj.getName())
        self.redrawObjectList()
        self.draw()
        popup.destroy()
        self.__list_of_objects_view.update()
        self.__points_counter = 0

    def changeObjectColor(self, obj, popup):
        color_code, color_hex = askcolor(title="Escolha uma cor")

        if color_hex:
            self.__controller.setColorById(obj.getId(), color_hex)
            self.addLogs('Alterou a cor do objeto ' + obj.getName())
            self.__controller.update()
            self.draw()

        popup.destroy()

    def transformObject(self, obj, popup):
        self.transform_object_window = TransformObjectsView(self, self.__controller, obj, self.draw)
        popup.destroy()

    def arrow_key_pressed(self, event):
        if event.keysym == "Up":
            self.moveUp()
        elif event.keysym == "Down":
            self.moveDown()
        elif event.keysym == "Left":
            self.moveLeft()
        elif event.keysym == "Right":
            self.moveRight()


    def moveUp(self):
        self.__controller.moveUp()
        self.addLogs('Moveu para cima')
        self.draw()

    def moveDown(self):
        self.__controller.moveDown()
        self.addLogs('Moveu para baixo')
        self.draw()
    
    def moveLeft(self):
        self.__controller.moveLeft()
        self.addLogs('Moveu para esquerda')
        self.draw()
    
    def moveRight(self):
        self.__controller.moveRight()
        self.addLogs('Moveu para direita')
        self.draw()

    def zoom(self, event):
        if(event.delta > 0):
            self.__controller.zoomIn()
            self.addLogs('ZoomIn')
        else:
            self.__controller.zoomOut()
            self.addLogs('ZoomOut')
        
        self.draw()


    def draw(self, event=None):
        self.setViewPort()
        if(event is not None):
            self.handleWithEvent(event)

        for obj in self.__controller.getListOfObjects():
            color = obj.getColor()
            coordinates = obj.getCoordinates()
            object_type = type(obj)
            if object_type == Point:
                self.drawPoint(color, coordinates)
            elif object_type == Line:
                self.drawLine(color, coordinates)
            else:
                if obj.fill_mode == "Arame":
                    self.drawWireFrame(color, coordinates)
                elif obj.fill_mode == "Grelha":
                    self.drawGridWireFrame(color, coordinates, 25)
                else:
                    self.drawFilledWireFrame(color, coordinates)
    

    def handleWithEvent(self, event):
        if(self.__drawing_object == 'Point'):
            self.__object_name = askstring("Nome","Digite o nome")
            point = Point(self.__object_name, [(event.x, event.y, 0)])
            self.addLogs('Adicionou ponto - '+ point.getName())
            self.addObjectToList(point)
            self.__controller.addObject(point)  

        elif(self.__drawing_object == 'Line'):
            if(self.__points_counter == 0):
                point = Point(self.__object_name, [(event.x, event.y, 0)])
                self.__controller.addObject(point)
                self.__points_counter += 1
            else:
                first_point = self.__controller.getListOfObjects()[-1]
                self.__object_name = askstring("Nome","Digite o nome")
                line = Line(self.__object_name, [first_point.getCoordinates()[0], (event.x, event.y, 0)])
                self.addLogs('Adicionou linha - '+ line.getName())
                self.__controller.popWorldObject()
                self.__controller.addObject(line)
                self.addObjectToList(line)
                self.__points_counter = 0

        elif(self.__drawing_object == 'Wire Frame'):
            if(self.__points_counter == 0):
                point = Point(self.__object_name, [(event.x, event.y, 0)])
                self.__controller.addObject(point)
                self.__points_counter += 1
            elif(self.__points_counter == 1):
                first_point = self.__controller.getListOfObjects()[-1]
                line = Line(self.__object_name, [first_point.getCoordinates()[0], (event.x, event.y, 0)])
                self.__controller.popWorldObject()
                self.__controller.addObject(line)
                self.__points_counter += 1
            else:
                last_object = self.__controller.getListOfObjects()[-1]
                points = [x for x in last_object.getCoordinates()]
                points.append((event.x,event.y,0))
                if(self.__points_counter == 2):
                    self.__object_name = askstring("Nome","Digite o nome")
                    choice = ChoiceDialog(self, title="Escolha um modo")
                    self.__last_mode_choice = choice.result
                    showinfo("Info", "Agora você pode continuar adicionando pontos para o seu Wireframe")
                wire_frame = WireFrame(self.__object_name, points, self.__last_mode_choice)
                wire_frame.setId(last_object.getId())
                self.__controller.popWorldObject()
                self.__controller.addObject(wire_frame)
                if(self.__points_counter == 2):
                    self.addObjectToList(wire_frame)
                    self.addLogs('Adicionou Wireframe - '+ wire_frame.getName())
                
                self.__points_counter += 1


    def drawPoint(self, color, coordinates):
        p1 = coordinates[0]
        x, y, z, w = p1
        self.__view_port.create_oval(x-2, y-2, x+2, y+2, fill=color)


    def drawLine(self, color, coordinates):
        p1, p2 = coordinates
        x1, y1, z1, w = p1
        x2, y2, z2, w = p2
        self.__view_port.create_line(x1, y1, x2, y2, fill=color, width=self.__line_width)


    def drawWireFrame(self, color, coordinates):
        for point in range(len(coordinates)):
            if (not point == (len(coordinates)-1)):
                p1 = coordinates[point]
                p2 = coordinates[point + 1]
                x1, y1, z1, w = p1
                x2, y2, z2, w = p2
                self.__view_port.create_line(x1, y1, x2, y2, fill=color, width=self.__line_width)
            else:
                p1 = coordinates[-1]
                p2 = coordinates[0]
                x1, y1, z1, w = p1
                x2, y2, z2, w = p2
                self.__view_port.create_line(x1, y1, x2, y2, fill=color, width=self.__line_width)

    
    def drawGridWireFrame(self, color, coordinates, grid_spacing=10):
        for point in range(len(coordinates)):
            p1 = coordinates[point]
            p2 = coordinates[(point + 1) % len(coordinates)]
            x1, y1, z1, w = p1
            x2, y2, z2, w = p2
            self.__view_port.create_line(x1, y1, x2, y2, fill=color, width=self.__line_width)
        
        y_coords = [coord[1] for coord in coordinates]
        y_min, y_max = min(y_coords), max(y_coords)
        for y in range(int(y_min), int(y_max) + 1, grid_spacing):
            intersections = self.getHorizontalIntersections(y, coordinates)
            for i in range(0, len(intersections)-1, 2):
                x_start = intersections[i]
                x_end = intersections[i+1]
                self.__view_port.create_line(x_start, y, x_end, y, fill=color, width=self.__line_width)

        x_coords = [coord[0] for coord in coordinates]
        x_min, x_max = min(x_coords), max(x_coords)
        for x in range(int(x_min), int(x_max) + 1, grid_spacing):
            intersections = self.getVerticalIntersections(x, coordinates)
            for i in range(0, len(intersections)-1, 2):
                y_start = intersections[i]
                y_end = intersections[i+1]
                self.__view_port.create_line(x, y_start, x, y_end, fill=color, width=self.__line_width)


    def getHorizontalIntersections(self, y, coordinates):
        intersections = []
        for i in range(len(coordinates)):
            p1 = coordinates[i]
            p2 = coordinates[(i + 1) % len(coordinates)]
            if self.crossesBorderHorizontal(p1, p2, y):
                x_cross = self.interpolateX(p1, p2, y)
                intersections.append(x_cross)
        return sorted(intersections)


    def getVerticalIntersections(self, x, coordinates):
        intersections = []
        for i in range(len(coordinates)):
            p1 = coordinates[i]
            p2 = coordinates[(i + 1) % len(coordinates)]
            if self.crossesBorderVertical(p1, p2, x):
                y_cross = self.interpolateY(p1, p2, x)
                intersections.append(y_cross)
        return sorted(intersections)


    def crossesBorderVertical(self, p1, p2, x):
        x1, x2 = p1[0], p2[0]
        return (x1 <= x <= x2) or (x2 <= x <= x1)


    def interpolateY(self, p1, p2, x):
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]

        if x1 == x2:
            return y1

        return y1 + (y2 - y1) * (x - x1) / (x2 - x1)


    def drawFilledWireFrame(self, color, coordinates):
        for point in range(len(coordinates)):
            p1 = coordinates[point]
            p2 = coordinates[(point + 1) % len(coordinates)]
            x1, y1, z1, w = p1
            x2, y2, z2, w = p2
            self.__view_port.create_line(x1, y1, x2, y2, fill=color, width=self.__line_width)
        
        y_coords = [coord[1] for coord in coordinates]
        y_min, y_max = min(y_coords), max(y_coords)

        for y in range(int(y_min), int(y_max) + 1):
            intersections = []
            for i in range(len(coordinates)):
                p1 = coordinates[i]
                p2 = coordinates[(i + 1) % len(coordinates)]
                
                if self.crossesBorderHorizontal(p1, p2, y):
                    x_cross = self.interpolateX(p1, p2, y)
                    intersections.append(x_cross)

            intersections.sort()
            for i in range(0, len(intersections)-1, 2):
                x_start = intersections[i]
                x_end = intersections[i+1]
                self.__view_port.create_line(x_start, y, x_end, y, fill=color, width=self.__line_width)


    def interpolateX(self, p1, p2, y):
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]

        if y1 == y2:
            return x1

        return x1 + (x2 - x1) * (y - y1) / (y2 - y1)
    

    def crossesBorderHorizontal(self, p1, p2, y):
        y1, y2 = p1[1], p2[1]
        return (y1 <= y <= y2) or (y2 <= y <= y1)
