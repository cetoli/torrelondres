print('oi')
bolada = "https://i.imgur.com/rgTSap6.png"
amarelo = 'https://i.imgur.com/FwCTxwE.png'
azul = 'https://i.imgur.com/ERl5wQU.png'
rosa = 'https://i.imgur.com/goMGtsi.png'
vermelho = 'https://i.imgur.com/hNCB7v3.png'
palita = 'https://i.imgur.com/JErcF8k.png'


class Vaga:
    def __init__(self, palito=None, altura=0):
        self.vaga = Torre.H.DIV(Id=f"vg_{str(palito)}_{altura}",
                                style={"position": "absolute", "bottom": f"{altura}px", "left": "-20px"})
        self._bola = None
        self.palito = palito

    @property
    def bola(self):
        return self._bola

    def vai(self):
        return self.vaga

    def tira(self):
        bola, self._bola = self._bola, None
        return bola

    def bota(self, bola):
        self._bola = bola.entra(self.palito)
        _ = self.vaga <= bola.vai()


class Bola:
    def __init__(self, h=None, cor=None, move=None, palito=None):
        def mover(ev):
            ev.stopPropagation()
            self.palito.bola(move)
            # move(self)
            # move(self.palito.vaga.bola)
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
    def __init__(self, palito, maxsize=1):
        self.pilha = []
        self.palito = palito
        self.pop_pilha = []
        self.maxsize = maxsize
        self.bota = self.vai_e_bota
        self.cria()
        self.vaga = None

    @property
    def bola(self):
        return self.vaga.bola

    def cria(self):
        pilha = self

        class UmaVaga(Vaga):
            def __init__(self, altura=0):
                super().__init__(pilha.palito, altura=altura)

        class UltimaVaga(UmaVaga):
            def bota(self, bola):
                # pilha.lotou()
                super().bota(bola)

            def tira(self):
                # pilha.vagou()
                return super().tira()

        self.vaga = UltimaVaga(altura=(self.maxsize-1)*100)
        self.pilha = [UmaVaga(altura=alt * 100) for alt in range(self.maxsize - 1)] + [self.vaga]

    def vai(self):
        return [vaga.vai() for vaga in self.pilha]
    #
    # def lotou(self):
    #     # self.bota = self.nao_bota
    #     pass
    #
    # def vagou(self):
    #     self.bota = self.vai_e_bota

    def vai_e_bota(self, bola):
        if not self.pilha:
            print("vai_e_bota", not self.pilha)
            return
        self.vaga = vaga = self.pilha.pop(0)
        self.pop_pilha = [vaga]+self.pop_pilha
        print("bota", self.palito.loc, len(self.pop_pilha), len(self.pilha))
        # self.pop_pilha.append(vaga)
        vaga.bota(bola)

    def tira(self):
        if not self.pop_pilha:
            return
        self.vaga = vaga = self.pop_pilha.pop(0)
        print("tira", self.palito.loc, len(self.pop_pilha))
        self.pilha = [vaga]+self.pilha
        return vaga.tira()

    def nao_bota(self, bola):
        pass


class Palito:
    def __init__(self, ordem=0, top=500, move=lambda _: None):
        def mover(ev):
            ev.stopPropagation()
            move(self)
        h = Torre.H
        self.palito = h.DIV(h.IMG(src=palita, width="60px", height=f"{300-100*ordem}px"),
                            style={"position": "absolute", "top": f"{top+100*ordem}px",
                            "left": f"{30+ordem*150}px"})
        self.vaga = Pilha(self, maxsize=3-ordem)
        self.lotado = self
        self.loc = (ordem, top)
        _ = self.palito <= self.vaga.vai()
        self.palito.bind("click", mover)

    # def move(self):
    #     self.vaga

    def lota(self):
        pass

    def bola(self, bota):
        return bota(self.vaga.bola) if self.vaga.bola else None

    def bota(self, mao):
        self.lotado.entra_(mao)

    def entra_(self, mao):
        # print("self.palito.entra(mao)", self.loc, mao)
        self.vaga.bota(mao)
        # self.lota()

    def vai(self):
        return self.palito

    def tira(self):
        print(self.lotado is self)
        return self.lotado.sai_()

    def sai_(self):
        _ = self
        self.vaga.tira()
        # print("self.palito.sai_()")


class Torre:
    H = None

    def __init__(self, h=None, bolas=(amarelo, azul, vermelho)):
        self.palito = [Palito(o, o+200, self.remove) for o in range(3)]
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
        self.mao.bola(palito.bota)
        # palito.bota(self.mao.bola())


def main(h):
    Torre.H = h
    return Torre(h).vai()
