# -----------------------------------------------------------#
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.font_manager as font_manager
from scipy.interpolate import make_interp_spline, BSpline
import numpy as np
import os
# -----------------------------------------------------------#





# --------------------------------------------------------#
# Script construído para o plot de gráficos do tipo cmap  #
#                                                         #
# Para uso é necessário apenas colocar os dados a serem   #
# plotados em arquivos de extensão '.dat' em uma pasta    #
# de nome 'graficos' e executar o script que deve estar   #
# junto com o arquivo de estilos 'font.mplstyle'          #
# --------------------------------------------------------#


###########################################################
# Bloco de código pra correção de problemas relacionados  #
#              as fontes do MATPLOTLIB                    #
###########################################################


os.system('rm ~/.cache/matplotlib -rf')

path = os.path.join(mpl.get_data_path(), "fonts/ttf/new-century-schoolbook-roman.otf")
prop = font_manager.FontProperties(fname=path)
plt.rcParams['font.family'] = prop.get_name()

plt.style.use('./font.mplstyle')

###########################################################

def plot_files():
    '''Seleciona apenas arquivos de
     extensão .dat para serem plotados'''

    files_name = os.listdir('graficos')
    name = [ifiles for ifiles in files_name if ifiles.split('.')[-1].lower() == 'dat']
    
    return name



def graph_plot():
    '''Contém todas as configurações
     para o plot dos gráficos'''

    files_name = plot_files()

    for name in files_name:

        data = np.loadtxt("graficos/%s" % name,unpack = True)  # Carrega e lê os arquivos 

        x = data[0]
        N = (len(data)-1)

        cmap = plt.get_cmap("jet", N)  # Define estilo de cores do gráfico

        fig, ax = plt.subplots()


        #######################
        # Ajuste das curvas   #
        #######################

        for i in range(2,(N-1)):
            y = data[i]
            for n in enumerate(np.linspace(0,1,N)):
                model = make_interp_spline(x,y,k=3)
                xs = np.linspace(100,2500,500)
                ys = model(xs)
                ax.plot(xs, ys, color=cmap(i))


        ##########################
        # Configuração dos eixos #
        ##########################


        '''---x axis---''' 

        ax.set_xlabel(r"T(K)")
        ax_xticks = [100,300,500,750,1000,2000,2500]
        ax.set_xticks(ax_xticks)
        ax2 = ax.secondary_xaxis('top')
        ax2.xaxis.set_ticks_position('top')
        ax2.set_xticklabels([])




        '''---y axis----'''


        ax.set_ylabel(r"$\mathregular{F^{MS-QH}_{%s,i}}$" % name.strip('.dat').upper())

        ax_ticks = []

        lim_min = data[1][1]
        lim_max = data[-1][-1]

        if (lim_max - lim_min) <= 30:
            for i in range((int(data[1][1])),int(data[-1][-1]+2.0),2):
                ax_ticks.append(float(i))
        elif (lim_max - lim_min) <= 40:
            for i in range((int(data[1][1])),int(data[-1][-1]+2.0),4):
                ax_ticks.append(float(i))
        else:
            for i in range((int(data[1][1])),int(data[-1][-1]+2.0),4):
                ax_ticks.append(float(i))

        ax.set_yticks(ax_ticks)
        ax2 = ax.secondary_yaxis('right')
        ax2.yaxis.set_ticks_position('right')
        ax2.set_yticklabels([])
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

        #######################
        # Definição de escala #
        # e tamanho da barra  #
        #      lateral        #
        #######################

        sm = plt.cm.ScalarMappable(cmap=cmap, norm=mpl.colors.Normalize(vmin=0, vmax=N))
        sm.set_array([N])


        boundaries = np.linspace(0, N, N + 1)
        cbar = plt.colorbar(sm, boundaries=boundaries)
        cbar.set_label('No. Rotamers',labelpad = 20)

        

        #####################
        # Plot e salvamento #
        #    dos gráficos   #
        #####################



        plt.axis([100,2500,lim_min,(lim_max+ 1.0)])
        plt.savefig("graficos/plot-%s.pdf" % name.strip('.dat').upper())
        

    return

graph_plot()
