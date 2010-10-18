import engine

import event, gui
import random

from gui import theme

def print_val(val):
    if not val.disabled:
        print val.text

def main():
    test = engine.display.Display()
    test.setup(screen_size=(640,480))
    test.build()
    test.clear()

    test.set_2d()
    test.set_lighting(False)

    event_handler = event.Handler()
    main_app = gui.App(event_handler)
    main_app.load_theme('gui_theme.txt')

    some_cont = gui.Container(main_app, (300,200), (100,150))
    some_cont.bg_color = (1,0,0,1)

##    gui.Icon(some_cont, (0,0), engine.helpers.load_image2D('unit-test-archer.gif'))
    gui.Icon(main_app, (0,0), 'archer')
    gui.Icon(main_app, (75,0), 'base')
    gui.Label(some_cont, (5, 5), "Hello Hello?")
    gui.Label(main_app, (0, 75), "Hello Hello?")
##
##    butt = gui.Button(some_cont, (75,5), "test\nclick")
##    text_box = gui.MessageBox(main_app, (300,100), (50, 200))
##    text_box.bg_color = (1,0,0,0.5)
##    butt.dispatch.bind('click',
##                       lambda: text_box.add_line(
##                           'test'+str(random.randint(0,45))))
##
    inp = gui.Input(main_app, (55,155))
    inp.theme.set_val('width', 290)

    gui.List(some_cont, gui.RelativePos(x="right", y="top"), ['test1', 'test2', 'test3'])
##
##    popup = gui.PopUp(butt, text="adds text to the message box below", width=100)
##    popup.bg_color = engine.misc.Color((255,255,255,100), 'rgba255')
##
##    drop = gui.DropDown(main_app, (5, 5), "press me!")
##    drop.setChild(gui.Label(main_app, (0,0), 'woah!'))
##
    menu = gui.Menu(main_app, gui.RelativePos(), ['abc', '123', ('come on now!', True)])
    menu2 = gui.DropDownMenu(main_app, gui.RelativePos(x="right", y="top", to=menu),
                             'clickme!', ['abc', '123', 'come on now!'])
    menu.dispatch.bind('select', print_val)


    while 1:
        event_handler.update()

        if event_handler.quit:
            test.destroy()
            return None

        test.clear()
        main_app.render()
        test.refresh()

main()
