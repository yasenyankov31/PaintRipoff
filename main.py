import tkinter as tk

class PaintApp:
    def __init__(self, master):
        self.master = master
        master.title("Paint App")
        self.elpise_counter=0

        # Set up the canvas
        self.canvas = tk.Canvas(master, width=800, height=600, bg="white")
        self.canvas.pack()

        # Bind events to the canvas
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

        # Set up the ellipse
        self.ellipse = None
        self.ellipse_color = "black"

        # Set up the drawing flag
        self.drawing = False

    def start_draw(self, event):
        # Start drawing the ellipse
        self.drawing = True
        self.ellipse = (event.x, event.y, event.x, event.y)

    def draw(self, event):
        # Update the ellipse size while drawing
        if self.drawing:
            self.ellipse = (self.ellipse[0], self.ellipse[1], event.x, event.y)
            self.draw_ellipse()

    def end_draw(self, event):
        # Stop drawing the ellipse
        self.drawing = False
        x0, y0, x1, y1 = self.ellipse
        self.elpise_counter+=1
        self.canvas.create_oval(x0, y0, x1, y1, outline=self.ellipse_color, tags=f"ellipse{self.elpise_counter}")

    def draw_ellipse(self):
        # Draw the ellipse on the canvas
        if self.canvas.find_withtag("ellipse"):
            self.canvas.delete("ellipse")
        if self.ellipse:
            x0, y0, x1, y1 = self.ellipse
            self.canvas.create_oval(x0, y0, x1, y1, outline=self.ellipse_color, tags="ellipse")

root = tk.Tk()
app = PaintApp(root)
root.mainloop()
