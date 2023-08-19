import tkinter as tk
from src.Controllers.Controller import Controller
from src.shapes.Point import Point
from src.shapes.Line import Line
class View():
    def __init__(self) -> None:
        self.__window = tk.Tk()
        self.__controller = Controller()
        self.__line_width = 3
        self.__controller.addObject(Line("linha 1", [(50,50,0), (75,75,0)]))

    def run(self) -> None:
        self.__window.geometry("1280x720")
        self.__window.configure(bg = "#2D2D2D")
        self.setViewPort()
        self.setLogOfActionsView()
        self.setListOfObjectsView()
        self.setControlView()
        self.setAddObjectButton()
        self.draw()
        self.__window.mainloop()

    def setViewPort(self) -> None:
        self.__view_port = tk.Canvas(
            self.__window,bg = "#FFFFFF",height = 460,width = 920,bd = 0,highlightthickness = 0,relief = "ridge")
        self.__view_port.place(x=340, y=20)
        self.__view_port.bind("<Button-1>", self.draw)


    def setLogOfActionsView(self) -> None:
        self.__log_actions_view = tk.Canvas(
            self.__window,bg = "#FFFFFF",height = 200,width = 920,bd = 0,highlightthickness = 0,relief = "ridge")
        self.__log_actions_view.place(x=340, y=500)
    
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
        self.__control.tag_bind(button_zoom_in, "<Button-1>", lambda x: print("Zoom In") )
        self.__zoon_out_button = tk.PhotoImage(file =f"src\Images\zoomOut.png")
        button_zoom_out = self.__control.create_image(20, 70, image = self.__zoon_out_button)
        self.__control.tag_bind(button_zoom_out, "<Button-1>", lambda x: print("Zoom Out") )

    def setMoveButtons(self) -> None:
        pass


    def openViewForAddNewShape(self) -> None:
        pass
    

    def draw(self):
        for obj in self.__controller.getListOfObjects():
            color = obj.getColor()
            coordinates = obj.getCoordinates()
            trasnformed_coordinates = self.__controller.getViewport().viewportTransform(coordinates)

            object_type = type(obj)
            if object_type == Point:
                self.drawPoint(color, trasnformed_coordinates)
            elif object_type == Line:
                self.drawLine(color, trasnformed_coordinates)
            else:
                self.drawWireFrame(color, trasnformed_coordinates)
        
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
        pass

    def update(self):
        pass

    def test(self):
        button1 = tk.Button(text='Get the Square Root', bg='brown', fg='white', font=('helvetica', 9, 'bold'))
        self.__view_port.create_window(200, 180, window=button1)