import  matplotlib.pyplot as plt
import numpy as np


class Graf():
    def __init__(self, wid, inter):
        super().__init__()
        self.outWID = wid
        self.inter = inter
        self.figur = self.make_graf()

    def string_to_func(self, s, x, lower_bound=-10, upper_bound=10):
        s = s.replace(',', ".")
        for i in s:
            if i not in "1234567890-+*/^ ()x.X":
                raise InputFuncException
        s = s.replace('^', "**").replace('X', 'x')
        return eval(s)

    def make_graf(self):
        y = []
        colors = []
        self.flag_iter = False
        self.errors = []

        for i in range(self.outWID.count()-1):
            s = self.outWID.itemAt(i).widget().children()[2].text()
            y.append(s)

            q = self.outWID.itemAt(i).widget().children()[3].currentIndex()
            if q == 0:
                colors.append('#b40e16')
            elif q ==1 :
                colors.append('#3f48cc')
            elif q ==2 :
                colors.append('#22b14c')
            elif q ==3 :
                colors.append('#f4e900')
            elif q ==4 :
                colors.append('#a349a4')

        if self.inter.children()[3].text() == '' and self.inter.children()[5].text() == '':
            x_from = -10
            x_to = 10
        else:
            try:
                x_from = float(self.inter.children()[3].text())
                x_to = float(self.inter.children()[5].text())
            except:
                self.flag_iter=True
                x_from = -10
                x_to = 10

        fig = plt.figure(frameon=True)
        ax = fig.add_axes((0.05, 0.1, 0.9, 0.8))

        step =  (x_to - x_from) / 750
        x = np.around(np.arange(x_from, x_to, step), decimals=4)

        for i in range(len(y)):
            try:
                f = lambda x_: self.string_to_func(y[i], x_)
                ax.plot(x, f(x), color=colors[i], label=y[i])
            except:
                self.errors.append(i)

        ax.legend()
        ax.grid(True)

        ax.text(0.5, 1.01,'y', transform=ax.transAxes)
        ax.text(0.98, 0.51,'x', transform=ax.transAxes)

        ax.spines['top'].set_color('none')
        ax.spines['right'].set_color('none')
        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('center')
        
        return fig

