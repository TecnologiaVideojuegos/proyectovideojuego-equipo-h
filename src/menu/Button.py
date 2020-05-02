import arcade


class Button(arcade.gui.TextButton):
    def __init__(self, center_x, center_y, width, height, text, theme):
        super().__init__(center_x, center_y, width, height, text, theme)

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False

    def draw(self):
        super().draw_texture_theme()
