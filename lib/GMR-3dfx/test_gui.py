import engine

import event, gui
import random

def print_val(val):
    print val

def main():
    test = engine.Display()
    test.setup(screen_size=(640,480))
    test.build()
    test.clear()

    test.set_2d()
    test.set_lighting(False)

    event_handler = event.Handler()
    main_app = gui.App(test.screen, event_handler)
    main_app.bg_color = (1,1,1,0.5)

    some_cont = gui.Container(main_app, (300,100), (50,50))
    some_cont.bg_color = (1,0,0,1)

    gui.Icon(some_cont, (0,0), engine.load_image2D('unit-test-archer.gif'))
    gui.Label(some_cont, (0, 75), "Hello Hello?")


    while 1:
        event_handler.update()

        if event_handler.quit:
            test.destroy()
            return None

        test.clear()
        main_app.render()
        test.refresh()

main()