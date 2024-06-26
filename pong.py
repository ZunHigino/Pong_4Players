from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock

Window.size = (880, 680)

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset
            
class PongPaddleSide(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_x - self.center_x) / (self.width / 2)
            bounced = Vector(vx, -1 *  vy)
            vel = bounced * 1.1
            ball.velocity = vel.x + offset, vel.y


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) +  self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    player3 = ObjectProperty(None)
    player4 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            self.player1.center_y += 75
        elif keycode[1] == 's':
            self.player1.center_y -= 75
        elif keycode[1] == 'up':
            self.player2.center_y += 75
        elif keycode[1] == 'down':
            self.player2.center_y -= 75
        elif keycode[1] == 'u':
            self.player3.center_x += 75
        elif keycode[1] == 'h':
            self.player3.center_x -= 75
        elif keycode[1] == 'r':
            self.player4.center_x += 75
        elif keycode[1] == 'f':
            self.player4.center_x -= 75
        return True

    def serve_ball(self, vel=(0,4.5)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        self.player3.bounce_ball(self.ball)
        self.player4.bounce_ball(self.ball)

        '''if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -0.8'''

        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4.5, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4.5, 0))
        if self.ball.y > self.top:
            self.player3.score += 1
            self.serve_ball(vel=(0,-4.5))
        if self.ball.y < self.y:
            self.player4.score += 1
            self.serve_ball(vel=(0,4.5))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()