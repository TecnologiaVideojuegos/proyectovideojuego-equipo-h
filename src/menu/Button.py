import arcade

class Button(arcade.gui.TextButton):
    def __init__(self, center_x, center_y, width, height, text):
        super().__init__(center_x, center_y, width, height, text)
        theme = arcade.gui.Theme()
        theme.set_font(24, arcade.color.WHITE)
        normal = ":resources:gui_themes/Fantasy/Buttons/Normal.png"
        hover = ":resources:gui_themes/Fantasy/Buttons/Hover.png"
        clicked = ":resources:gui_themes/Fantasy/Buttons/Clicked.png"
        locked = ":resources:gui_themes/Fantasy/Buttons/Locked.png"
        theme.add_button_textures(normal, hover, clicked, locked)
        self.normal_texture = theme.button_textures['normal']
        self.hover_texture = theme.button_textures['hover']
        self.clicked_texture = theme.button_textures['clicked']
        self.locked_texture = theme.button_textures['locked']
        self.font_size = theme.font_size
        self.font_name = theme.font_name
        self.font_color = theme.font_color
        self.theme = True

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False

    def draw(self):
        self.draw_texture_theme()
        arcade.draw_text(self.text, self.center_x, self.center_y,
                         self.font_color, font_size=self.font_size,
                         font_name=self.font_name,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")
