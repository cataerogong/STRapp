from webui import webui

def main():

	# Create a window object
	MyWindow = webui.window()
	MyWindow.set_port(8008)

	# Note
	# Add this script to all your .html files:
	# <script src="webui.js"></script>

	# Show a window using the local file
	MyWindow.show("index.html")

	# Wait until all windows are closed
	webui.wait()

if __name__ == "__main__":
	main()