import tkinter as tk

class DragDropButton(tk.Button):
    def __init__(self,canvas, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Button-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_move)
        self.bind("<ButtonRelease-1>", self.on_button_release)
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.canvas=canvas

    def on_button_press(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_move(self, event):
        self.master.delete("resize_rect")
        self.canvas.delete("resize_rect")
        x, y = self.winfo_x() - self.drag_start_x + event.x, self.winfo_y() - self.drag_start_y + event.y
        self.place(x=x, y=y)
        self.canvas.create_rectangle(0, 0, x, y,outline='black', fill="",tags="resize_rect")
        self.master.create_rectangle(0, 0, x, y,outline='black', fill="",tags="resize_rect")

    def on_button_release(self, event):
        x, y = self.winfo_x() - self.drag_start_x + event.x, self.winfo_y() - self.drag_start_y + event.y
        self.canvas.delete("resize_rect")
        self.master.delete("resize_rect")
        self.canvas.config(width=x,height=y)

class ZoomCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<MouseWheel>", self.zoom)

    def zoom(self, event):
        scale = 1.0
        if event.delta > 0:
            scale *= 1.1
        else:
            scale /= 1.1
        self.scale("all", 0,0, scale, scale)

root = tk.Tk()
root.geometry('1000x800')

v_s = tk.Scrollbar(root, orient=tk.VERTICAL)
v_s.pack(side=tk.RIGHT, fill=tk.Y)

h_s = tk.Scrollbar(root, orient=tk.HORIZONTAL)
h_s.pack(side=tk.BOTTOM, fill=tk.X)

frame = tk.Canvas(root,background="gray")
frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

canvas = ZoomCanvas(frame, background="white",width=600,height=400, scrollregion=(0, 0, 2000, 2000))
canvas.pack(side=tk.LEFT, anchor="nw")

button = DragDropButton(canvas,frame, text="Click Me!")
button.pack(side=tk.LEFT,pady=400, anchor="nw")

canvas.create_rectangle(50, 50, 150, 150, fill="red")
canvas.create_rectangle(200, 50, 300, 100, fill="green")
canvas.create_rectangle(250, 100, 350, 150, fill="blue")

v_s.config(command=canvas.yview)
h_s.config(command=canvas.xview)

canvas.config(xscrollcommand=h_s.set, yscrollcommand=v_s.set)

root.mainloop()
