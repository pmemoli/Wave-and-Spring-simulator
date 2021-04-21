from tkinter import *

instructions = """
En:
Press right click to set a mass, left click to connect two masses with a spring
and middle click to create an unmovable mass. ENTER starts/pauses the simulation.
BACKSPACE deletes current configuration. Press Q to set the physical properties 
of the next mass and/or string. Once created the properties remain, so concatenation
of different masses and springs is possible.

Esp:
Presionar click derecho para crear una masa, click izquierdo para conectar dos masas con un resorte
y click medio (la ruedita) para crear una masa que no se mueve. ENTER empieza/pausa la simulacion.
Se puede borrar la configuracion con BACKSPACE. Presionar Q permite cambiar las propiedades fisicas
de los proximos objetos. Una vez creados estas propiedades permanecen, de forma que se pueden combinar
masas y resortes distintos.

40 Pixels = 1 Meter
"""

class Instructions:
	def __init__(self):
		pass

	def run(self):
		self.root.mainloop()

	def create(self):
		self.root = Tk()
		self.instructions_frame = LabelFrame(self.root, text="Instructions")
		self.instructions_text = Label(self.instructions_frame, text=instructions)

		self.instructions_frame.pack()
		self.instructions_text.pack()


class Settings:
	def __init__(self):
		self.k = 6
		self.lo = 0
		self.mass = 5
		self.initial_velocity_x = 0
		self.initial_velocity_y = 0

	def run(self, mass=None, lo=None, k=None):
		self.root.mainloop()


	def create(self):
		self.root = Tk()
		settings_frame = LabelFrame(self.root, text="Properties for next objects")
		
		mass_label = Label(settings_frame, text='Mass (Kg): ')
		mass_input = Entry(settings_frame, borderwidth = 3)
		
		lo_label = Label(settings_frame, text='Natural Length (Pixels): ')
		lo_input = Entry(settings_frame, borderwidth = 3)

		k_label = Label(settings_frame, text='Spring Constant: ')
		k_input = Entry(settings_frame, borderwidth = 3)

		initial_velocity_x_label = Label(settings_frame, text='Initial Velocity X (Pixels/s): ')
		initial_velocity_x_input = Entry(settings_frame, borderwidth = 3)

		initial_velocity_y_label = Label(settings_frame, text='Initial Velocity Y (Pixels/s): ')
		initial_velocity_y_input = Entry(settings_frame, borderwidth = 3)

		apply_button = Button(settings_frame, text="Apply", command=lambda:self.apply_constants(mass_input, lo_input, k_input, initial_velocity_x_input, initial_velocity_y_input))

		settings_frame.pack()

		mass_input.insert(0, self.mass); lo_input.insert(0, self.lo); k_input.insert(0, self.k)
		initial_velocity_x_input.insert(0, self.initial_velocity_x); initial_velocity_y_input.insert(0, self.initial_velocity_y)

		mass_label.grid(row=0, column=0); mass_input.grid(row=0, column=1)
		lo_label.grid(row=1, column=0); lo_input.grid(row=1, column=1)
		k_label.grid(row=2, column=0); k_input.grid(row=2, column=1)
		initial_velocity_x_label.grid(row=3, column=0); initial_velocity_x_input.grid(row=3, column=1)
		initial_velocity_y_label.grid(row=4, column=0); initial_velocity_y_input.grid(row=4, column=1)

		apply_button.grid(row=5, column=0)


	def apply_constants(self, mass, lo, k, v_o_x, v_o_y):
		self.mass = mass.get()
		self.lo = lo.get()
		self.k = k.get()
		self.initial_velocity_x = int(v_o_x.get())
		self.initial_velocity_y = int(v_o_y.get())

		self.root.destroy()
