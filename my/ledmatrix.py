from .font import LCD_FONT, proportional
import apa102, machine

class LedMatrix():
    def __init__(self, width=8, height=1, cascaded=1):
        self.strip = apa102.APA102(machine.Pin(5), machine.Pin(4), width*height*cascaded)
        self.width = width
        self.height = height
        self.cascaded = cascaded
        self.intesity = 1
        self.backcolor = (0,0,0)

    def clear(self, backcolor=None ):
        if not backcolor:
            backcolor = self.backcolor
        color = list(backcolor)
        color.append(self.intesity)
        color = tuple(color)
        for x in range(self.width*self.height*self.cascaded):
            self.strip[x] = color
        self.draw()

    def point(self, xy, color):
        x, y = xy
        if x >= self.width*self.cascaded or y >= self.height:
            return
        color = list(color)
        color.append(self.intesity)
        color = tuple(color)
        
        pos = 0
        if x>=self.width:
            cascade = x//self.width
            pos = self.width*self.height*cascade
            x = x-self.width*cascade
            
        pos += y * self.width + x
        # if pos >= self.width * self.height:
        #     return
        # print(pos)
        self.strip[pos] = color

    def draw(self):
        self.strip.write()

    def text(self, txt, color=(0xC0, 0xC0, 0xC0), font=proportional(LCD_FONT), start=(0,0)):

        # self.clear()

        x, y = start
        for ch in txt:
            # print('drawing ', ch)
            for byte in font[ord(ch)]:
                for j in range(8):
                    if byte & 0x01 > 0:
                        self.point((x, y + j), color=color)
                    else:
                        self.point((x, y + j), self.backcolor)
                    byte >>= 1
                x += 1
        
        for pos_x in range(x, self.width * self.cascaded):
            for pos_y in range(self.height):
                # print(x, y)
                self.point((pos_x, pos_y), self.backcolor)

        self.draw()