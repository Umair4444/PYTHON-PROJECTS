import tkinter as tk

class EraserCanvas:
    def __init__(self, root, width, height, cell_size):
        self.root = root
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Create the canvas
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()

        # Draw the grid of blue cells
        self.cells = []
        for y in range(0, self.height, self.cell_size):
            row = []
            for x in range(0, self.width, self.cell_size):
                rect = self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill="blue")
                row.append(rect)
            self.cells.append(row)

        # Create the eraser rectangle (initially at position (0,0))
        self.eraser_size = self.cell_size
        self.eraser = self.canvas.create_rectangle(0, 0, self.eraser_size, self.eraser_size, outline="red", width=2)

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_eraser)
        self.canvas.bind("<B1-Motion>", self.move_eraser)
        self.canvas.bind("<ButtonRelease-1>", self.release_eraser)

    def start_eraser(self, event):
        # Store the initial position for dragging
        self.eraser_start_x = event.x
        self.eraser_start_y = event.y
        self.erase_cells(event)

    def move_eraser(self, event):
        # Move the eraser rectangle
        dx = event.x - self.eraser_start_x
        dy = event.y - self.eraser_start_y
        self.canvas.move(self.eraser, dx, dy)
        self.eraser_start_x = event.x
        self.eraser_start_y = event.y
        self.erase_cells(event)

    def release_eraser(self, event):
        # Clear the eraser movement flag
        self.eraser_start_x = None
        self.eraser_start_y = None

    def erase_cells(self, event):
        # Get the position of the eraser
        eraser_coords = self.canvas.bbox(self.eraser)
        eraser_x1, eraser_y1, eraser_x2, eraser_y2 = eraser_coords

        # Check which grid cells are touched by the eraser
        for row in self.cells:
            for rect in row:
                rect_coords = self.canvas.bbox(rect)
                rect_x1, rect_y1, rect_x2, rect_y2 = rect_coords
                # Check if the eraser rectangle overlaps with the current grid cell
                if not (eraser_x2 < rect_x1 or eraser_x1 > rect_x2 or eraser_y2 < rect_y1 or eraser_y1 > rect_y2):
                    self.canvas.itemconfig(rect, fill="white")  # Set the cell to white


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Eraser on Canvas")

    canvas_width = 600
    canvas_height = 400
    cell_size = 30  # Size of each grid cell

    eraser_canvas = EraserCanvas(root, canvas_width, canvas_height, cell_size)

    root.mainloop()
