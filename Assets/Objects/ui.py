from tkinter import *

instructions = """
En:
Press right click to set a mass, left click to connect two masses with a spring
and middle click to create an unmovable mass. ENTER key starts/pauses the simulation.
Press Q to set the physical properties of the next mass and/or string. Once created
the properties remain, so concatenation of different masses and springs is possible.

Esp:
Presionar click derecho para crear una masa, click izquierdo para conectar dos masas con un resorte
y click medio (la ruedita) para crear una masa que no se mueve. ENTER empieza/pausa la simulacion.
Presionar Q permite cambiar las propiedades fisicas de los proximos objetos. Una vez creados estas
propiedades permanecen, de forma que se pueden combinar masas y resortes distintos.

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

		apply_button = Button(settings_frame, text="Apply", command=lambda:self.apply_constants(mass_input, lo_input, k_input))

		settings_frame.pack()

		mass_input.insert(0, self.mass); lo_input.insert(0, self.lo); k_input.insert(0, self.k)

		mass_label.grid(row=0, column=0); mass_input.grid(row=0, column=1)
		lo_label.grid(row=1, column=0); lo_input.grid(row=1, column=1)
		k_label.grid(row=2, column=0); k_input.grid(row=2, column=1)

		apply_button.grid(row=3, column=0)


	def apply_constants(self, mass, lo, k):
		self.mass = mass.get()
		self.lo = lo.get()
		self.k = k.get()

		self.root.destroy()
