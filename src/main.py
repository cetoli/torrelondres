print('oi')
bolada = "https://i.imgur.com/rgTSap6.png"
amarelo = 'https://i.imgur.com/FwCTxwE.png'
azul = 'https://i.imgur.com/ERl5wQU.png'
rosa = 'https://i.imgur.com/goMGtsi.png'
vermelho = 'https://i.imgur.com/hNCB7v3.png'
palita = 'https://i.imgur.com/JErcF8k.png'


class Vaga:
    def __init__(self, h=None, palito=None):
        self.vaga = h.DIV(style={"position": "absolute", "bottom": "0px", "left": "-20px"})
        self.bola = None
        self.palito = palito

    def vai(self):
        return self.vaga

    def sai(self):
        bola, self.bola = self.bola.sai(), None
        return bola

    def entra(self, bola):
        self.bola = bola.entra(self.palito)
        self.palito.lota()
        _ = self.vaga <= bola.vai()


class Bola:
    def __init__(self, h=None, cor=None, move=None, palito=None):
        def mover(ev):
            ev.stopPropagation()
            move(self)
        self.bola = h.DIV(h.IMG(src=cor, width="100px"))
        self.bola.bind("click", mover)
        self.palito = palito

    def entra(self, palito=None):
        self.palito.sai()
        self.palito = palito
        return self

    def vai(self):
        return self.bola


class Palito:
    def __init__(self, h=None, ordem=0, top=300, move=None):
        def mover(ev):
            ev.stopPropagation()
            move(self)
        self.palito = h.DIV(h.IMG(src=palita, width="60px", height=f"{300-100*ordem}px"),
                            style={"position": "absolute", "top": f"{top+100*ordem}px",
                            "left": f"{30+ordem*150}px"})
        self.vaga = Vaga(h, self)
        self.lotado = self
        self.loc = (ordem, top)
        _ = self.palito <= self.vaga.vai()
        self.palito.bind("click", mover)

    def lota(self):
        class PalitoCheio:
            def __init__(self, palito):
                self.palito = palito

            def entra_(self, mao):
                print("self.palito.lotado.entra_()", self.palito.loc)
                self.palito.lotado = self

            def sai_(self):
                print("self.palito.lotado.sai_()", self.palito.loc)
                self.palito.lotado = self.palito

        self.lotado = PalitoCheio(self)

    def bola(self):
        return self.vaga.bola

    def entra(self, mao):
        self.lotado.entra_(mao)

    def entra_(self, mao):
        print("self.palito.entra(mao)", self.loc, mao)
        self.vaga.entra(mao)
        # self.lota()

    def vai(self):
        return self.palito

    def sai(self):
        print(self.lotado is self)
        return self.lotado.sai_()

    def sai_(self):
        _ = self
        pass
        print("self.palito.sai_()")


class Torre:
    def __init__(self, h=None, bolas=(amarelo, azul, vermelho)):
        self.palito = [Palito(h, o, o, self.remove) for o in range(3)]
        self.vaga = Vaga(h, self)
        self.mao = Palito(h, 2, -200)
        [_palito.entra(Bola(h, _bola, self.move, self)) for _palito, _bola in zip(self.palito, bolas)]

    def sai(self):
        return self

    def entra(self, bola):
        pass
        # self.vaga.entra(bola)

    def vai(self):
        return [_palito.vai() for _palito in self.palito] + [self.mao.vai()]

    def move(self, palito):
        self.mao.entra(palito)

    def remove(self, palito):
        palito.entra(self.mao.bola())


def main(h):
    return Torre(h).vai()
