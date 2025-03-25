import pyautogui
import tkinter as tk
from ui.regions.region import TitledRegionGroupSequence, getRegionsTitles
from common.jsonRW import readJSON, writeJSON
import os

class ScreenRegionChoser(tk.Tk):
    save_path = "./regions_save.json"
    def __init__(self, sequence : TitledRegionGroupSequence):
        tk.Tk.__init__(self)
        self.sequence = sequence

        # Create a transparent overlay window
        self.attributes("-alpha", 0.7)  # Set transparency (0.0 to 1.0)
        self.overrideredirect(True)  # Remove window decorations (title bar, etc.)

        # Canvas for drawing
        screen_width, screen_height = pyautogui.size()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.geometry(f"{100}x{100}+0+0")

        # Your Python interface elements
        self.canvas = tk.Canvas(self, bg="white", width=screen_width, height=screen_height)
        self.canvas.pack(anchor="n")

        self.display = self.canvas.create_text(self.screen_width//2, 0, text="", font=("Helvetica", 16), anchor="n")

        #Post-Load init
        self.loadSave()
        self.set_overlay_title(self.sequence.getTitle(), self.sequence.getColor())

        # Prevent the overlay window from losing focus
        #self.geometry(f"{100}x{100}+0+0")
        self.attributes("-topmost", True)
        self.grab_set()

        # Bind the "Esc" key to close the overlay
        self.bind("<Escape>", lambda x : self.destroy())
        self.bind("<BackSpace>", self.backspace_pressed)
        self.bind("<Return>", self.return_pressed)
        self.bind("<KeyPress>", self.on_key_press)

        # Bind mouse events for drawing a square
        self.canvas.bind("<B1-Motion>", self.draw_square)
        self.canvas.bind("<ButtonRelease-1>", self.get_square_coordinates)

        # Initialize variables for square drawing
        self.start_x = None
        self.start_y = None
        self.visible = False

    def on_key_press(self, event):
        if event.keysym == 't':  # 4 corresponds to the Ctrl key
            self.visible = not self.visible
            if self.visible :
                self.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
            else :
                self.geometry(f"{100}x{100}+0+0")

    def writeSave(self) :
        writeJSON(self.save_path, self.sequence.region_groups)

    def loadSave(self) :
        if not os.path.exists(self.save_path):
            return
        
        data = readJSON(self.save_path)
        for group in data :
            for region in group :
                self.canvas.create_rectangle(
                    region[0], region[1], region[0]+region[2], region[1]+region[3],
                    outline=self.sequence.getColor(),
                    tags=f"group:{self.sequence.getGroupIndex()}-index:{self.sequence.getIndex()}"
                )
                self.sequence.addRegion(region)
            self.sequence.nextRegionGroup()

    def return_pressed(self, event) :
        ended = self.sequence.nextRegionGroup()
        self.set_overlay_title(self.sequence.getTitle(), self.sequence.getColor())
        if ended :
            self.writeSave()
            self.destroy()


    def backspace_pressed(self, event) :
        erase_needed = self.sequence.removeLast()
        self.set_overlay_title(self.sequence.getTitle(), self.sequence.getColor())
        if erase_needed :
            self.clearCurrentShape()

    def beginSquare(self, x,y):
        self.start_x, self.start_y = x,y

    def clearCurrentShape(self):
        self.canvas.delete(f"group:{self.sequence.getGroupIndex()}-index:{self.sequence.getIndex()}")

    def draw_square(self, event):
        # Draw a square on the canvas while the left mouse button is pressed
        if self.start_x is not None and self.start_y is not None:
            # Clear current square
            self.clearCurrentShape()
            width, height = event.x-self.start_x, event.y-self.start_y
            #width = max(abs(event.x - self.start_x),abs(event.y - self.start_y))
            #height = width
            self.canvas.create_rectangle(
                self.start_x, self.start_y, self.start_x+width, self.start_y+height, outline=self.sequence.getColor(), tags=f"group:{self.sequence.getGroupIndex()}-index:{self.sequence.getIndex()}"
            )
        else :
            self.beginSquare(event.x,event.y)

    def get_square_coordinates(self, event):
        # Get the coordinates and dimensions of the drawn square
        if self.start_x is not None and self.start_y is not None:
            width, height = event.x-self.start_x, event.y-self.start_y
            #width = max(abs(event.x - self.start_x),abs(event.y - self.start_y))
            #height=width
            self.sequence.addRegion((self.start_x, self.start_y, width, height))
            self.start_x = self.start_y = None
            self.set_overlay_title(self.sequence.getTitle(), self.sequence.getColor())
    
    def set_overlay_title(self, new_title, color):
        self.canvas.itemconfig(self.display, text=new_title+"\nEntrée pour passer à la suite", fill=color)

if __name__ == "__main__":
    sequence = TitledRegionGroupSequence(*getRegionsTitles())
    overlay = ScreenRegionChoser(sequence)
    overlay.mainloop()