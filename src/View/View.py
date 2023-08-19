import tkinter as tk
from src.Controllers.Controller import Controller
from src.shapes.Line import Line
class View():
    def __init__(self) -> None:
        self.__window = tk.Tk()
        self.__controller = Controller()
        self.__controller.addObject(Line("linha 1", "linha", [(50,50,0), (75,75,0)]))

    def run(self) -> None:
        self.__window.geometry("1280x720")
        self.__window.configure(bg = "#2D2D2D")
        self.setViewPort()
        self.setLogOfActionsView()
        self.setListOfObjectsView()
        self.setControlView()
        self.setAddObjectButton()
        self.drawLine(self.__controller.getLisOfObjects()[0])
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

    def draw(self, event):
        print(event.x, event.y)
        self.drawPoint(event)
        
    def drawPoint(self,event):
        BLACK = "#000000"
        x1, y1 = (event.x - 2), (event.y - 2)
        x2, y2 = (event.x + 2), (event.y + 2)
        self.__view_port.create_oval(x1, y1, x2, y2, fill=BLACK)

    def drawLine(self,line):
        x1, y1, z1 = line.getCoordinates()[0]
        x2, y2, z2 = line.getCoordinates()[1]
        self.__view_port.create_line(x1, y1, x2, y2, fill="#ff0000")

    def update(self):
        pass

    def test(self):
        button1 = tk.Button(text='Get the Square Root', bg='brown', fg='white', font=('helvetica', 9, 'bold'))
        self.__view_port.create_window(200, 180, window=button1)