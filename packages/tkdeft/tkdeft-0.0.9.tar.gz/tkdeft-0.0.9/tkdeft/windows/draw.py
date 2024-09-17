class DDraw(object):
    def create_tksvg_image(self, path):
        from tksvg import SvgImage
        tkimage = SvgImage(file=path)
        return tkimage

    def create_tk_image(self, path):
        from PIL.Image import open
        from PIL.ImageTk import PhotoImage
        image = open(path)
        self.tkimage = PhotoImage(image=image)
        return tkimage


class DSvgDraw(DDraw):
    def create_drawing(self, width, height, temppath=None, **kwargs):
        if temppath:
            path = temppath
        else:
            from tempfile import mkstemp
            _, path = mkstemp(suffix=".svg", prefix="tkdeft.temp.")
        import svgwrite
        dwg = svgwrite.Drawing(path, width=width, height=height, **kwargs)

        return path, dwg
