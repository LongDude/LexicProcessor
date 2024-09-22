package main

import (
	"os"

	"github.com/therecipe/qt/widgets"
)

func main() {
	app := widgets.NewQApplication(len(os.Args), os.Args)

	// Creating window
	window := widgets.NewQMainWindow(nil, 0)
	window.SetMinimumSize2(250, 200)
	window.SetWindowTitle("Hello Widget Example")

	// Creating regular widget and centering
	widget := widgets.NewQWidget(nil, 0)
	widget.SetLayout(widgets.NewQVBoxLayout())
	window.SetCentralWidget(widget)

	// LineEdit with placeholding text
	input := widgets.NewQLineEdit(nil)
	input.SetPlaceholderText("Placeholder text")
	widget.Layout().AddWidget(input)

	// Creating button
	button := widgets.NewQPushButton2("Click", nil)
	button.ConnectClicked(func(bool) {
		widgets.QMessageBox_Warning(nil, "Succass", input.Text(), widgets.QMessageBox__Ok, widgets.QMessageBox__Ok)
	})
	widget.Layout().AddWidget(button)

	window.Show()
	app.Exec()
}
