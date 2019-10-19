import gi

class Canvas(gtk.DrawingArea):
    def __init__(self):
        super(Canvas, self).__init__()
        self.connect("expose_event", self.expose)
        self.set_size_request(800,500)

    def expose(self, widget, event):
        cr = widget.window.cairo_create()
        rect = self.get_allocation()

        # you can use w and h to calculate relative positions which
        # also change dynamically if window gets resized
        w = rect.width
        h = rect.height

        # here is the part where you actually draw
        cr.move_to(0,0)
        cr.line_to(w/2, h/2)
        cr.stroke()

window = gtk.Window()
canvas = Canvas()
window.add(canvas)
window.set_position(gtk.WIN_POS_CENTER)
window.show_all()
gtk.main()