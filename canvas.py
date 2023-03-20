import tkinter as tk

# Create the main window
root = tk.Tk()
root.geometry('400x400')

# Create a canvas widget with a large size
canvas = tk.Canvas(root, width=800, height=800,background="white")
canvas.pack(side='left', fill='both', expand=True)

# Add some content to the canvas
flip=False
for i in range(50):
    flip=not flip
    if i%5==0:
        for j in range(50):
            if flip:
                canvas.create_rectangle(i*20, j*20, (i+1)*20, (j+1)*20, fill='white')
            else:
                canvas.create_rectangle(i*20, j*20, (i+1)*20, (j+1)*20, fill='black')

# Create horizontal scrollbar
x_scrollbar = tk.Scrollbar(root, orient='horizontal', command=canvas.xview)
x_scrollbar.pack(side='bottom', fill='x')

# Create vertical scrollbar
y_scrollbar = tk.Scrollbar(root, orient='vertical', command=canvas.yview)
y_scrollbar.pack(side='right', fill='y')

# Configure the canvas to use the scrollbars
canvas.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

# Make the canvas scrollable with the mouse
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=(0,0,2000,2000)))

root.mainloop()
