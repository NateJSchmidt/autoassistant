package main

import (
	"fmt"

	"github.com/go-vgo/robotgo"
)

func main() {
	fmt.Println("Hello world")

	// a := app.New()
	// w := a.NewWindow("Hello World")

	// hello := widget.NewLabel("Hello everybody!")
	// w.SetContent(container.NewVBox(
	// 	hello,
	// 	widget.NewButton("Hi!", func() {
	// 		hello.SetText("Welcome")
	// 	}),
	// ))

	// w.ShowAndRun()
	mleft := robotgo.AddEvent("mleft")
	if mleft == true {
		x, y := robotgo.GetMousePos()
		fmt.Printf("You clicked the left mouse button at %d, %d\n", x, y)
	} else {
		fmt.Println("Nothing was clicked?")
	}
}
