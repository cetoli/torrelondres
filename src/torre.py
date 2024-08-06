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

        class Vaga:
            def __init__(self, fundo, bola=None, maxsize=1):
                self.bota, self.tira = self._bota, self._tira
                self.vaga_corrente = 0
                self.bola = h.IMG(src=bola, width=100).bind("click", self.move_para_mao) if bola else None
                self._vaga = None
                self.vaga = None

            def cria_cheio(self):
                _ = self
                class_vaga = cv = Vaga(0)
                class_vaga.vaga = None
                cv.bota = lambda *_: None
                return class_vaga

            def cria_vaga(self, fundo, bola=None):
                vaga = h.DIV(style={"position": "absolute", "bottom": f"{fundo}px", "left": f"{-25}px"})
                _ = vaga <= self.bola if bola else None
                print(bola)
                self.bota = self._bota if not bola else lambda *_: None
                class_vaga = Vaga(fundo, bola)
                class_vaga.vaga = vaga
                return class_vaga

            def cria(self, fundo, bola=None, maxsize=1):
                self._vaga = [self.cria_vaga(-fundo+f*100, bola) for f in range(maxsize)]  # +[self.cria_cheio()]
                # self.vaga = self._vaga[self.vaga_corrente].vai()
                self.vaga = [vg.vai() for vg in self._vaga]
                print(fundo, maxsize)
                return self
                # _ = self.vaga <= self.bola if bola else None

            def _bota(self, pino=None):
                pino(self.botando)

            def botando(self, bola=None):
                self.bola = bola
                # _ = self.vaga <= bola
                self.vaga_corrente += 1 if self.vaga_corrente < len(self._vaga)-1 else 0
                print(self.vaga_corrente, len(self._vaga))
                _vaga = self._vaga[self.vaga_corrente]
                _ = _vaga.vaga <= bola
                self.bota = lambda *_: None
                self.tira = self._tira

            def move_para_mao(self, ev):
                ev.stopPropagation()
                tor.mao.vaga.bota(self.tira)

            def vai(self):
                return self.vaga

            def _tira(self, pino):
                print(pino, self.bola)
                # self.vaga_corrente -= 1
                # _vaga = self._vaga[self.vaga_corrente]
                self.bota = self._bota  # _vaga.bota
                # self.tira = _vaga.tira
                self.tira = lambda *_: None
                pino(self.bola)

        class Pino:
            def __init__(self, p, top=altura, bola=None, tira=False):
                self.vaga = Vaga(p, bola).cria(p, bola, 3-p)
                # self.bota, self.tira = self.vaga.bota, self.vaga.tira
                tira = self.move_para_pino if tira else lambda *_: None
                self.pino = h.DIV(
                    [h.IMG(src=IMG.pa, width=50, height=300-100*p).bind("click", tira)],
                    style={"position": "absolute", "top": f"{top+100*p}px", "left": f"{p*100+50}px"}).bind(
                    "click", tira)
                _ = self.pino <= self.vaga.vai()

            def move_para_pino(self, ev):
                ev.stopPropagation()
                self.vaga.bota(tor.mao.vaga.tira)

            def vai(self):
                return self.pino
        self.mao = Pino(2, -200)
        self.pinos = [Pino(p, bola=img, tira=True).vai() for p, img in enumerate(IMG[:-2])]+[self.mao.vai()]


def torre(h):
    Torre.H = h
    return Torre().vai()
