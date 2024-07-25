from collections import namedtuple
DI = namedtuple("DI", "s w h l t c p d")
print('oi')
bolas = "https://i.imgur.com/rgTSap6.png"
amarelo = 'https://i.imgur.com/FwCTxwE.png'
azul = 'https://i.imgur.com/ERl5wQU.png'
rosa = 'https://i.imgur.com/goMGtsi.png'
vermelho = 'https://i.imgur.com/hNCB7v3.png'
palito = 'https://i.imgur.com/JErcF8k.png'
dedos = 'dedos.png'


def _torre(h):
    cima = 90 + 150
    topo = 70 + 150
    dedo = -250
    no_dedo_top, no_dedo_left = 80, 210
    return [
        h.DIV(h.IMG(src=dedos, width="500px"),
              style={"position": "absolute", "left": "80px", "top": f"{dedo}px"}),
        h.DIV(h.IMG(src=palito, width="50px", height="350px"),
              style={"position": "absolute", "left": "80px", "top": f"{topo}px"}),
        h.DIV(h.IMG(src=palito, width="50px", height="242px"),
              style={"position": "absolute", "left": "180px", "top": f"{topo+100}px"}),
        h.DIV(h.IMG(src=palito, width="50px", height="125px"),
              style={"position": "absolute", "left": "280px", "top": f"{topo+200}px"}),
        h.DIV(h.IMG(src=azul, width="100px"),
              style={"position": "absolute", "left": "50px", f"top": f"{cima}px"}),
        h.DIV(h.IMG(src=rosa, width="100px"),
              style={"position": "absolute", "left": "50px", f"top": f"{cima+100}px"}),
        h.DIV(h.IMG(src=vermelho, width="100px"),
              style={"position": "absolute", "left": "50px", f"top": f"{cima+200}px"}),
        h.DIV(h.IMG(src=amarelo, width="100px"),
              style={"position": "absolute", "left": f"{no_dedo_left}px", f"top": f"{no_dedo_top}px"}),
              # style={"position": "absolute", "left": "150px", f"top": f"{cima+200}px"}),
    ]


class Local:
    BOLA = None
    DEDOS = None
    D, G = None, None

    def __init__(self, x, y, di: namedtuple):
        Local.DEDOS = self
        self.x, self.y = x, y
        self.bola = None
        self.vai = self.agora_vai
        self.sai = self.nem_vai
        self.html = Local.D(
            Local.G(src=f"{di.s}", width=f"{di.w}px", height=f"{di.h}px"),
            style={"position": "absolute", "left": f"{di.l}px", f"top": f"{di.t}px"}
        )

    def agora_vai(self):
        Local.BOLA, self.bola = None, Local.BOLA
        self.vai = self.nem_vai
        return self

    def nem_vai(self, *_):
        return self

    def agora_sai(self, *_):
        Local.BOLA, self.bola = self.bola, None
        self.vai = self.agora_vai

    def foi(self):
        return self.html


class Palito(Local):
    def sai(self, *_):
        Local.BOLA, self.bola = self.bola, None
        Local.DEDOS.vai()


class Torre:
    def __init__(self, h):
        Local.D, Local.G = h.DIV, h.IMG
        self.h = h
        pl = [DI(palito, 50, 350-i*112, 80+i*100, 70+150+i*100, 0, 0, 0) for i in range(3)]
        self.pl = [Local(0, 0, di).foi() for di in pl]
        _bolas = [azul, rosa, vermelho]
        pl = [DI(bola, 100, 100, 50, 90+150+i*100, 0, 0, 0)
              for i, bola in enumerate(_bolas)]
        self.bl = [Local(0, 0, di).foi() for di in pl]


    def foi(self):
        return [
            Local(80, -250, DI(dedos, 500, 400, 80, -250, 0, 0, 0)).foi()]+self.pl+self.bl


def torre(h):
    return Torre(h).foi()
