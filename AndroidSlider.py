'''
Created by Willie Lawrence - cptx032 arroba gmail dot com
https://github.com/cptx032/kivy-widgets
'''
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Rectangle, Color, Ellipse

def lerp(a, b, x):
	'''linear interpolation'''
	return a + ((b-a)*x)

class FilledCircle(Ellipse):
	def __init__(self, *args, **kws):
		x = kws.pop('x', 0)
		y = kws.pop('y', 0)
		radius = kws.pop('radius', 0)
		Ellipse.__init__(self, *args, **kws)
		self.x = x
		self.y = y
		self.radius = radius

	def update(self):
		pass

	@property
	def radius(self):
		# supposing the size is a square
		# the first (0) element is equals
		# to second element
		return self.size[0] / 2.0

	@radius.setter
	def radius(self, value):
		# preserving old position
		x, y = self.x, self.y
		# the anchor of square is the 'sw'
		# point, so we we need reposition
		# the square
		self.size = [value*2, value*2]
		# reposition:
		self.x, self.y = x, y
		self.update()

	@property
	def x(self):
		return self.pos[0] + self.radius

	@x.setter
	def x(self, value):
		pos = list(self.pos)
		pos[0] = value - self.radius
		self.pos = pos
		self.update()

	@property
	def y(self):
		return self.pos[1] + self.radius

	@y.setter
	def y(self, value):
		pos = list(self.pos)
		pos[1] = value - self.radius
		self.pos = pos
		self.update()

class AndroidSliderCenter(FilledCircle):
	def __init__(self, *args, **kws):
		self.outer_circle = FilledCircle(
			x=kws.get('x',0),
			y=kws.get('y',0),
			radius=15
		)
		FilledCircle.__init__(self, *args, **kws)

	def update(self):
		self.outer_circle.x = self.x
		self.outer_circle.y = self.y

class AndroidSlider(Widget, ButtonBehavior):
	def __init__(self, _min=0, _max=100, value=50):
		self.__min = _min
		self.__max = _max
		self.__value = value
		# used here only to save current pos and size
		self.widget_area = Rectangle()
		self.circle = AndroidSliderCenter(radius=5)
		self.bg_line = Rectangle()
		self.bg_line_color = Color(0.109,0.109,0.109,1.0)
		self.progress_line = Rectangle()
		self.bg_height = 3
		Widget.__init__(self)

		self.canvas.add(self.bg_line_color)
		self.canvas.add(self.bg_line)

		self.canvas.add(Color(0.18,0.7,0.89,1.0))
		self.canvas.add(self.progress_line)

		self.canvas.add(Color(0.18,0.7,0.89,1.0))
		self.canvas.add(self.circle)
		self.canvas.add(Color(0.18,0.7,0.89,0.5))
		self.canvas.add(self.circle.outer_circle)

		self.min = self.__min
		self.max = self.__max
		self.value = self.__value
		ButtonBehavior.__init__(self)

	def mouse_is_over(self, event):
		x, y = event.pos
		in_x = (x >= self.widget_area.pos[0]) and (x <= self.widget_area.pos[0]+self.widget_area.size[0])
		in_y = (y >= self.widget_area.pos[1]) and (y <= self.widget_area.pos[1]+self.widget_area.size[1])
		return in_x and in_y

	def set_value_by_event(self, event):
		x, y = event.pos
		self.value = lerp(self.min, self.max, (x - self.widget_area.pos[0]) / self.widget_area.size[0])

	def on_touch_move(self, event):
		if self.mouse_is_over(event):
			self.set_value_by_event(event)

	def on_touch_down(self, event):
		if self.mouse_is_over(event):
			self.set_value_by_event(event)

	def on_pos(self, parent, pos):
		self.widget_area.pos = pos
		self.update_slider()

	def on_size(self, parent, size):
		self.widget_area.size = size
		self.update_slider()

	def update_slider(self):
		self.bg_line.size = [self.widget_area.size[0], self.bg_height]
		self.bg_line.pos = [
			self.widget_area.pos[0],
			self.widget_area.pos[1]+(self.widget_area.size[1]/2.0)-(self.bg_height/2.0)
		]
		self.circle.x = lerp(
			self.widget_area.pos[0],
			self.widget_area.pos[0] + self.widget_area.size[0],
			(self.value-self.min) / (self.max-self.min)
		)
		size = [self.circle.x - self.widget_area.pos[0], self.bg_height]
		self.progress_line.size = size

		self.circle.y = self.bg_line.pos[1] + self.bg_height/2.0
		self.circle.update()

		self.progress_line.pos = self.bg_line.pos

	@property
	def min(self):
		return self.__min

	@min.setter
	def min(self, value):
		self.__min = float(value)
		self.update_slider()

	@property
	def max(self):
		return self.__max

	@max.setter
	def max(self, value):
		self.__max = float(value)
		self.update_slider()

	@property
	def value(self):
		return self.__value

	@value.setter
	def value(self, value):
		# fixme> verify bounds
		self.__value = float(value)
		self.update_slider()

	@property
	def bg_height(self):
		return self.bg_line.size[1]

	@bg_height.setter
	def bg_height(self, value):
		size = list(self.bg_line.size)
		size[1] = value
		self.bg_line.size = size
		self.update_slider()

if __name__ == '__main__':
	from kivy.app import App
	from kivy.uix.button import Button
	from kivy.uix.gridlayout import GridLayout

	class SliderApp(App):
		def build(self):
			grid = GridLayout(rows=1, cols=1, padding=55)
			grid.add_widget(AndroidSlider(_min=0, _max=100, value=50))
			return grid
	SliderApp().run()
