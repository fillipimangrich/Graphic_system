import tkinter as tk
from src.Controllers.Controller import Controller
from src.shapes.Point import Point
from src.shapes.Line import Line
from src.shapes.WireFrame import WireFrame
class View():
    def __init__(self) -> None:
        self.__window = tk.Tk()
        self.__controller = Controller()
        self.__line_width = 3
        self.__drawing_object = "Point"
        self.__points_counter = 0
        self.__logs = []

    def run(self) -> None:
        self.__window.geometry("1280x720")
        self.__window.configure(bg = "#2D2D2D")
        self.setViewPort()
        self.setLogOfActionsView()
        self.setListOfObjectsView()
        self.setControlView()
        self.setAddObjectButton()
        self.__window.mainloop()
        

    def setViewPort(self) -> None:
        self.__view_port = tk.Canvas(
            self.__window,bg = "#FFFFFF",height = 460,width = 920,bd = 0,highlightthickness = 0,relief = "ridge")
        self.__view_port.place(x=340, y=20)
        self.__view_port.bind("<Button-1>", self.draw)
        self.__window.bind("<Left>", self.arrow_key_pressed)
        self.__window.bind("<Right>", self.arrow_key_pressed)
        self.__window.bind("<Up>", self.arrow_key_pressed)
        self.__window.bind("<Down>", self.arrow_key_pressed)
        self.__window.bind("<MouseWheel>", self.zoom)


        #TO DO: DRAW THE LINE BASED IN THE POSITION OF THE CURSOR

        # self.__view_port.bind("<B1-Motion>", self.draw)


    def setLogOfActionsView(self) -> None:
        self.log_frame = tk.Frame(self.__window)
        self.log_frame.place(x=340, y=500, width=920, height=200)

        # Scrollbar
        self.scroll_y = tk.Scrollbar(self.log_frame, orient="vertical")
        self.scroll_y.pack(side="right", fill="y")

        # Canvas
        self.__log_actions_view = tk.Canvas(
            self.log_frame, bg="#FFFFFF", bd=0, highlightthickness=0, relief="ridge", yscrollcommand=self.scroll_y.set)
        self.__log_actions_view.pack(side="left", fill="both", expand=True)

        self.scroll_y.config(command=self.__log_actions_view.yview)

        self.log_y_position = 10
    
    def setListOfObjectsView(self) -> None:
        self.__list_of_objects_view = tk.Canvas(
            self.__window,bg = "#FFFFFF",height = 240,width = 300,bd = 0,highlightthickness = 0,relief = "ridge")
        self.__list_of_objects_view.place(x=20, y=20)

    def setControlView(self) -> None:
        self.__control = tk.Canvas(
            self.__window,bg = "#565656",height = 420,width = 300,bd = 0,highlightthickness = 0,relief = "ridge")
        self.__control.place(x=20, y=280)
        self.setAddObjectButton()
        self.setZoomButtons()
        self.setMoveButtons()

    def setAddObjectButton(self) -> None:
        self.__add_object_button = tk.PhotoImage(file = f"src/Images/add_button.png")
        button_add = self.__control.create_image(220, 50, image=self.__add_object_button)
        self.__control.tag_bind(button_add, "<Button-1>", lambda x: print("Adicionou objeto"))


    def setZoomButtons(self) -> None:
        self.__zoom_in_button = tk.PhotoImage(file=f"src\Images\zoomIn.png")
        button_zoom_in = self.__control.create_image(20, 25, image = self.__zoom_in_button)
        self.__control.tag_bind(button_zoom_in, "<Button-1>", lambda x: self.zoom(type('event', (object,), {'delta': 1})()))
        
        self.__zoon_out_button = tk.PhotoImage(file =f"src\Images\zoomOut.png")
        button_zoom_out = self.__control.create_image(20, 70, image = self.__zoon_out_button)
        self.__control.tag_bind(button_zoom_out, "<Button-1>", lambda x: self.zoom(type('event', (object,), {'delta': 0})()) )
    
    def addLogs(self, message: str) -> None:
        self.__log_actions_view.create_text(10, self.log_y_position, text=message, anchor="w")
        self.log_y_position += 20

        self.__log_actions_view.config(scrollregion=self.__log_actions_view.bbox("all"))
        self.__log_actions_view.yview_moveto(1)
    
    def update_mesage(self):
        self._canvas.itemconfig(self.mesage_var, text =self._mensagem)
    
    def arrow_key_pressed(self, event):
        if event.keysym == "Up":
            self.__controller.moveUp()
            self.addLogs('Moveu para cima')
        elif event.keysym == "Down":
            self.__controller.moveDown()
            self.addLogs('Moveu para baixo')
        elif event.keysym == "Left":
            self.__controller.moveLeft()
            self.addLogs('Moveu para esquerda')
        elif event.keysym == "Right":
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

    def setMoveButtons(self) -> None:
        pass


    def openViewForAddNewShape(self) -> None:
        pass
    

    def draw(self, event=None):
        self.setViewPort()
        if(event is not None):
            self.handleWithEvent(event)

        for obj in self.__controller.getListOfObjects():
            color = obj.getColor()
            coordinates = obj.getCoordinates()
            transformed_coordinates = self.__controller.getViewport().viewportTransform(coordinates)
            object_type = type(obj)

            if object_type == Point:
                self.drawPoint(color, transformed_coordinates)
            elif object_type == Line:
                self.drawLine(color, transformed_coordinates)
            else:
                self.drawWireFrame(color, transformed_coordinates)
    

    def handleWithEvent(self, event):
        if(self.__drawing_object == 'Point'):
            point = Point("ponto", [(event.x, event.y, 0)])
            self.addLogs('Adicionou ponto - '+ point.getName())
            self.__controller.addObject(point)
        elif(self.__drawing_object == 'Line'):
            if(self.__points_counter == 0):
                point = Point("ponto", [(event.x, event.y, 0)])
                self.__controller.addObject(point)
                self.__points_counter += 1
            else:
                first_point = self.__controller.getListOfObjects()[-1]
                line = Line("linha", [first_point.getCoordinates()[0], (event.x,event.y,0)])
                self.addLogs('Adicionou linha - '+ line.getName())
                self.__controller.getListOfObjects().pop()
                self.__controller.addObject(line)
                self.__points_counter = 0
        elif(self.__drawing_object == 'Wire Frame'):
            if(self.__points_counter == 0):
                point = Point("ponto", [(event.x, event.y, 0)])
                self.__controller.addObject(point)
                self.__points_counter += 1
            elif(self.__points_counter == 1):
                first_point = self.__controller.getListOfObjects()[-1]
                line = Line("linha", [first_point.getCoordinates()[0], (event.x,event.y,0)])
                self.__controller.getListOfObjects().pop()
                self.__controller.addObject(line)
                self.__points_counter += 1
            else:
                last_object = self.__controller.getListOfObjects()[-1]
                points = [x for x in last_object.getCoordinates()]
                points.append((event.x,event.y,0))
                wire_frame = WireFrame("wire frame", points)
                self.__controller.getListOfObjects().pop()
                self.__controller.addObject(wire_frame)
                self.addLogs('Adicionou Wireframe - '+ wire_frame.getName())
                self.__points_counter += 1

    def drawPoint(self, color, coordinates):
        p1 = coordinates[0]
        x, y = p1
        self.__view_port.create_oval(x-1, y-1, x+1, y+1, fill=color)

    def drawLine(self, color, coordinates):
        p1, p2 = coordinates
        x1, y1 = p1
        x2, y2 = p2
        self.__view_port.create_line(x1, y1, x2, y2, fill=color, width=self.__line_width)

    def drawWireFrame(self, color, coordinates):
        for point in range(len(coordinates)):
            if (not point == (len(coordinates)-1)):
                p1 = coordinates[point]
                p2 = coordinates[point + 1]
                x1, y1 = p1
                x2, y2 = p2
                self.__view_port.create_line(x1, y1, x2, y2, fill=color, width=self.__line_width)
            else:
                p1 = coordinates[-1]
                p2 = coordinates[0]
                x1, y1 = p1
                x2, y2 = p2
                self.__view_port.create_line(x1, y1, x2, y2, fill=color, width=self.__line_width)


    def update(self):
        pass

    def test(self):
        button1 = tk.Button(text='Get the Square Root', bg='brown', fg='white', font=('helvetica', 9, 'bold'))
        self.__view_port.create_window(200, 180, window=button1)