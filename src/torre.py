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
                # self.cheio = bola is not None
                self.bota, self.tira = self._bota, self._tira
                tira = self.move_para_pino if tira else lambda *_: None
                self.bola = h.IMG(src=bola, width=100).bind("click", self.move_para_mao) if bola else None
                self.vaga = h.DIV(style={"position": "absolute", "bottom": f"{0}px", "left": f"{-25}px"})
                self.pino = h.DIV(
                    [h.IMG(src=IMG.pa, width=50, height=300-100*p).bind("click", tira), self.vaga],
                    style={"position": "absolute", "top": f"{top+100*p}px", "left": f"{p*100+50}px"}).bind(
                    "click", tira)
                _ = self.pino <= self.vaga
                _ = self.vaga <= self.bola if bola else None

            def _bota(self, pino=None):
                pino(self.botando)

            def botando(self, bola=None):
                self.bola = bola
                _ = self.vaga <= bola
                self.bota = lambda *_: None
                self.tira = self._tira

            def move_para_mao(self, ev):
                ev.stopPropagation()
                tor.mao.bota(self.tira)

            def move_para_pino(self, ev):
                ev.stopPropagation()
                self.bota(tor.mao.tira)

            def vai(self):
                return self.pino

            def _tira(self, pino):
                print(pino, self.bola)
                self.bota = self._bota
                self.tira = lambda *_: None
                pino(self.bola)

        self.mao = Pino(2, -200)
        self.pinos = [Pino(p, bola=img, tira=True).vai() for p, img in enumerate(IMG[:-2])]+[self.mao.vai()]


def torre(h):
    Torre.H = h
    return Torre().vai()
