from bpsk_dsss import settings

from matplotlib import pyplot


def show_plot(*data):
    for plot in data:
        pyplot.plot(plot)
    pyplot.show()

last_plot_id = 0

def save_plot(file_name):
    global last_plot_id
    pyplot.savefig(f'{settings.results_path}{last_plot_id}_{file_name}', bbox_inches='tight')
    last_plot_id += 1
