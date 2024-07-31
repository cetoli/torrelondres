print('oi')
bolada = "https://i.imgur.com/rgTSap6.png"
amarelo = 'https://i.imgur.com/FwCTxwE.png'
azul = 'https://i.imgur.com/ERl5wQU.png'
rosa = 'https://i.imgur.com/goMGtsi.png'
vermelho = 'https://i.imgur.com/hNCB7v3.png'
palita = 'https://i.imgur.com/JErcF8k.png'


class Vaga:
    def __init__(self, palito=None):
        self.vaga = Torre.H.DIV(style={"position": "absolute", "bottom": "0px", "left": "-20px"})
        self.bola = None
        self.palito = palito

    def vai(self):
        return self.vaga

    def tira(self):
        bola, self.bola = self.bola.tira(), None
        return bola

    def bota(self, bola):
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
        self.palito.tira()
        self.palito = palito
        return self

    def vai(self):
        return self.bola


class Pilha:
    def __init__(self, maxsize=1):
        self.pilha = []
        self.pop_pilha = []
        self.maxsize = maxsize
        self.estado_pilha = self
        self.bota = self.vai_e_bota
        self.cria()

    def cria(self):
        class UmaVaga:
            def __init__(self):
                self.bola = None

            def bota(self, bola):
                self.bola = bola

            def tira(self):
                bola, self.bola = self.bola, None
                return bola

        class UltimaVaga(UmaVaga):
            def bota(vaga, bola):
                self.lotou()
                super().bota(bola)

            def tira(vaga):
                self.vagou()
                return super().tira()

        self.pilha = [UltimaVaga()]+[UmaVaga() for _ in range(self.maxsize-1)]

    def lotou(self):
        self.bota = self.nao_bota

    def vagou(self):
        self.bota = self.vai_e_bota

    def vai_e_bota(self, bola):
        vaga = self.pilha.pop()
        self.pop_pilha.append(vaga)
        vaga.bota(bola)

    def tira(self):
        vaga = self.pop_pilha.pop()
        self.pilha.append(vaga)
        return vaga.tira()

    def nao_bota(self, bola):
        pass


class Palito:
    def __init__(self, ordem=0, top=300, move=None):
        def mover(ev):
            ev.stopPropagation()
            move(self)
        h = Torre.H
        self.palito = h.DIV(h.IMG(src=palita, width="60px", height=f"{300-100*ordem}px"),
                            style={"position": "absolute", "top": f"{top+100*ordem}px",
                            "left": f"{30+ordem*150}px"})
        self.vaga = Vaga(self)
        self.lotado = self
        self.loc = (ordem, top)
        _ = self.palito <= self.vaga.vai()
        self.palito.bind("click", mover)

    def lota(self):
        class PalitoCheio:
            def __init__(self, palito):
                self.palito = palito

            def entra_(self, _):
                print("self.palito.lotado.entra_()", self.palito.loc)
                self.palito.lotado = self

            def sai_(self):
                print("self.palito.lotado.sai_()", self.palito.loc)
                self.palito.lotado = self.palito

        self.lotado = PalitoCheio(self)

    def bola(self):
        return self.vaga.bola

    def bota(self, mao):
        self.lotado.entra_(mao)

    def entra_(self, mao):
        print("self.palito.entra(mao)", self.loc, mao)
        self.vaga.bota(mao)
        # self.lota()

    def vai(self):
        return self.palito

    def tira(self):
        print(self.lotado is self)
        return self.lotado.sai_()

    def sai_(self):
        _ = self
        pass
        print("self.palito.sai_()")


class Torre:
    H = None

    def __init__(self, h=None, bolas=(amarelo, azul, vermelho)):
        self.palito = [Palito(o, o, self.remove) for o in range(3)]
        self.vaga = Vaga(self)
        self.mao = Palito(2, -200)
        [_palito.bota(Bola(h, _bola, self.move, self)) for _palito, _bola in zip(self.palito, bolas)]

    def tira(self):
        return self

    def bota(self, bola):
        pass
        # self.vaga.entra(bola)

    def vai(self):
        return [_palito.vai() for _palito in self.palito] + [self.mao.vai()]

    def move(self, palito):
        self.mao.bota(palito)

    def remove(self, palito):
        palito.bota(self.mao.bola())


def main(h):
    Torre.H = h
    return Torre(h).vai()
