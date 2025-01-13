def create_sidebar(self):
        sidebar = tk.Canvas(self.root, bg=self.colors['white'], width=120, height=600, highlightthickness=0)  # Increased height to 600
        sidebar.pack_propagate(False)  # Prevent the sidebar from resizing to fit its contents
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, pady=(90, 70))  # Adjusted vertical padding

        # Draw rounded rectangle with only top left and bottom left corners rounded
        def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
            points = [
                x1 + radius, y1,
                x2, y1,
                x2, y1,
                x2, y1,
                x2, y1,
                x2, y2,
                x2, y2,
                x2, y2,
                x2, y2,
                x1 + radius, y2,
                x1, y2,
                x1, y2 - radius,
                x1, y1 + radius,
                x1, y1,
            ]
            return canvas.create_polygon(points, **kwargs, smooth=True)

        # Example usage of create_rounded_rectangle
        create_rounded_rectangle(sidebar, 10, 10, 110, 590, radius=45, fill=self.colors['pup_maroon'], outline=self.colors['pup_maroon'])  # Adjusted height to 590