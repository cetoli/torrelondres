from collections import namedtuple

# noinspection SpellCheckingInspection
URL = "FwCTxwE  ERl5wQU goMGtsi hNCB7v3 JErcF8k".split()
IMG = namedtuple(
    "IMG", "am az ro ve pa")(*[f"https://i.imgur.com/{img}.png" for img in URL])


class Torre:
    H = None

    def __init__(self):
        self.pinos = []
        self.mao = None
        self.cria()

    def vai(self):
        return [pino for pino in self.pinos]

    def cria(self):
        h, altura, tor = Torre.H, 200, self

        class Pino:
            def __init__(self, p, top=altura, bola=None, tira=None):
                self.cheio = bola is not None
                tira = self.move_para_pino if tira else lambda *_: None
                self.bola = h.IMG(src=bola, width=100).bind("click", self.move_para_mao) if bola else None
                self.vaga = h.DIV(style={"position": "absolute", "bottom": f"{0}px", "left": f"{-25}px"})
                self.pino = h.DIV(
                    [h.IMG(src=IMG.pa, width=50, height=300-100*p).bind("click", tira), self.vaga],
                    style={"position": "absolute", "top": f"{top+100*p}px", "left": f"{p*100+50}px"}).bind(
                    "click", tira)
                _ = self.pino <= self.vaga
                _ = self.vaga <= self.bola if bola else None

            def bota_(self, bola=None):
                self.bola = bola = bola() if ((not self.cheio) and bola) else None
                _ = self.vaga <= bola if bola else None
                self.cheio = True

            def bota(self, pino=None):
                pino(self.botando) if not self.cheio else None

            def botando(self, bola=None):
                self.bola = bola
                _ = self.vaga <= bola if bola else None
                self.cheio = True

            def move_para_mao(self, ev):
                ev.stopPropagation()
                tor.mao.bota(self.tira)

            def move_para_pino(self, ev):
                ev.stopPropagation()
                self.bota(tor.mao.tira)

            def vai(self):
                return self.pino

            def tira_(self, bola=None):
                print(bola, self.cheio, self.bola)
                if self.cheio:
                    self.cheio = False
                    bola = self.bola
                return bola

            def tira(self, pino):
                print(pino, self.cheio, self.bola)
                if self.cheio:
                    self.cheio = False
                    pino(self.bola)
                # return bola

        self.mao = Pino(2, -200)
        _ = [h.DIV(
            [h.IMG(src=IMG.pa, width=50, height=300-100*p),
             h.DIV(h.IMG(src=img, width=100), style={"position": "absolute", "bottom": f"{0}px", "left": f"{-25}px"})],
            style={"position": "absolute", "top": f"{altura+100*p}px", "left": f"{p*100+50}px"})
            for p, img in enumerate(IMG[:-2])]+[self.mao.vai()]
        self.pinos = [Pino(p, bola=img, tira=True).vai() for p, img in enumerate(IMG[:-2])]+[self.mao.vai()]
        pass


def torre(h):
    Torre.H = h
    return Torre().vai()
