# Spring-Simulator
Set any spring-mass configuration on a 2D plane and see how it evolves. 

Pygame and Numpy required

Instructions / Instrucciones:

Press left click to set a mass, right click to connect two masses with a spring, 
right click + R to create a rod approximation and middle click to create an "unmovable" mass.
ENTER starts/pauses the simulation. BACKSPACE deletes current configuration.
Press Q to set the physical properties for the next mass and/or string. Once created the properties remain, 
so concatenation of different masses and springs is possible. Press G to turn gravity ON/OFF

Presionar click izquierdo para crear una masa, click derecho para conectar dos masas con un resorte,
click derecho + R para crear una aproximacion de vara y click medio (la ruedita) para crear una masa que no se mueve.
ENTER empieza/pausa la simulacion. Se puede borrar la configuracion con BACKSPACE. Presionar Q permite cambiar
las propiedades fisicas de los proximos objetos. Una vez creados estas propiedades permanecen, de forma que se pueden combinar
masas y resortes distintos. La G activa o desactiva la gravedad.

Rod approximation: k ~ 10000 and initial length = natural length.

Unmovable mass: m ~ 10000kg

TODO: 
Allow for mass/spring deleting during the "prepare" menu. Save configurations.
