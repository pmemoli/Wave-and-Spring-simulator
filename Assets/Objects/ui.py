from tkinter import *

class Instructions:
	def __init__(self):
		pass

	def run(self):
		self.root.mainloop()

	def create(self):
		self.root = Tk()
		self.instructions_frame = LabelFrame(self.root, text="instructions")
		self.instructions_text = Label(self.instructions_frame, text="""
			TODO: INSTRUCTIONS
			""")

		self.instructions_frame.pack()
		self.instructions_text.pack()


class Settings:
	def __init__(self):
		self.k = 6
		self.lo = 0
		self.mass = 5

	def run(self):
		self.root.mainloop()

	def create(self):
		self.root = Tk()
		settings_frame = LabelFrame(self.root, text="instructions")
		
		mass_label = Label(settings_frame, 'Mass: ')
		mass_input = Entry(settings_frame, borderwidth = 3)
		
		lo_label = Label(settings_frame, 'Natural Length: ')
		lo_input = Entry(settings_frame, borderwidth = 3)

		k_label = Label(settings_frame, 'Spring Constant: ')
		k_input = Entry(settings_frame, borderwidth = 3)

		self.instructions_frame.pack()
	
	 


#Instructions = Instructions()
#Instructions.run()