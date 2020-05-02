import arcade


class Button(arcade.gui.TextButton):
    def __init__(self, center_x, center_y, width, height, text, theme: arcade.gui.Theme):
        super().__init__(center_x, center_y, width, height, text, theme)

        self.f_size = theme.font_size

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False

    def draw(self):
        if self.theme:
            self.draw_texture_theme()
        else:
            self.draw_color_theme()

        arcade.draw_text(self.text, self.center_x, self.center_y,
                         self.font_color, font_size=self.f_size,
                         font_name=self.font_name,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")
