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

	// Creating root widget
	root := widgets.NewQWidget(nil, 0)
	root.SetLayout(widgets.NewQHBoxLayout())
	window.SetCentralWidget(root)

	// Left (editing) window
	edit := widgets.NewQTextEdit(nil)
	root.Layout().AddWidget(edit)

	// Right(results) window
	analysis := widgets.NewQWidget(nil, 0)
	analysis.SetLayout(widgets.NewQVBoxLayout())
	root.Layout().AddWidget(analysis)

	// AnalysisResult window
	// TODO

	// AnalysisStats(bottom) window
	// TODO

	window.Show()
	app.Exec()
}
