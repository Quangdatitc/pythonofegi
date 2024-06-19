# Using the mouseReleased event handler

# Create a listner that reapplies the selected property of all JySubMenu items
# ...after the BasicMenuUI listener has done all of its required work
from java.awt.event import MouseAdapter
class NonDeselectingListener(MouseAdapter):
	def __init__(self, originalListener):
		self.originalListener = originalListener
	
	def mouseEntered(self, event):
		self.originalListener.mouseEntered(event)
		self.restoreSelections(event)
	    
	def mouseExited(self, event):
		self.originalListener.mouseExited(event)
	
	def mouseReleased(self, event):
		self.originalListener.mouseReleased(event)
		
	def restoreSelections(self, event):
		for component in event.source.parent.components:
			if 'JySubMenu' in component.__class__.__name__:
				component.selected = True

# Recursively sets the background and foreground colors of all the sub components of a popup menu
def setMenuColor(menu, background, foreground):
	menu.background = background
	menu.foreground = foreground
	for component in menu.components:
		setMenuColor(component, background, foreground)

		# If a submenu is found, color its popup and set it selected property to true
		if 'JySubMenu' in component.__class__.__name__:
			setMenuColor(component.popupMenu, background, foreground)
			component.selected = True
		
		# Locate the Basic UI listener of the menu item
		# ...and wrap in a listener that listener that will restore the selected coloring
		# ...before the component is repainted
		for listener in component.mouseListeners:
			if 'BasicMenuUI' in listener.__class__.__name__ or 'BasicMenuItemUI' in listener.__class__.__name__:
				component.removeMouseListener(listener)
				component.addMouseListener(NonDeselectingListener(listener))
	
# Simple nested popup example based on documented example # 4:
def sayHello(event):
	print ('Hello')
subMenu01 = [["Click Me 1", "Click Me 2"], [sayHello, sayHello]]
subMenu02 = [["Click Me 3", "Click Me 4"], [sayHello, sayHello]]
subMenu03 = [["Click Me 5", "Click Me 6"], [sayHello, sayHello]]
subMenu04 = [["Click Me 7", "Click Me 8"], [sayHello, sayHello]]
subMenu05 = [["Click Me 9", "Click Me 10"], [sayHello, sayHello]]
menu = system.gui.createPopupMenu(['Click Me', 'subMenu01', 'subMenu02', 'subMenu03', 'subMenu04', 'subMenu05'], [sayHello, subMenu01, subMenu02, subMenu03, subMenu04, subMenu05])
setMenuColor(menu, system.gui.color('black'), system.gui.color('white'))
menu.show(event)