# Created by Weikai Wu

# Libraries needed
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import cStringIO


def plot_pie(title, percentiles, explode, labels, colors=None):
    color_list = ['whitesmoke', 'rosybrown', 'firebrick', 'r', 'darksalmon',
                 'sienna', 'sandybrown', 'bisque', 'tan', 'moccasin',
                 'floralwhite', 'gold', 'darkkhaki', 'lightgoldenrodyellow',
                 'olivedrab', 'chartreuse', 'darksage', 'lightgreen',
                 'green', 'mediumseagreen', 'mediumaquamarine',
                 'mediumturquoise', 'darkslategrey', 'c', 'cadetblue',
                 'skyblue', 'dodgerblue', 'slategray']
    # deal with empty lists
    if len(percentiles) == 0:
        percentiles = [100.0]
        explode = [0.0]
        labels = ['None']
    fig = plt.figure(figsize=(5, 4), dpi=75, facecolor='w')
    ax = fig.gca()
    ax.set_title(title)
    if colors is None or len(colors) == 0:
        colors = color_list[:len(percentiles)]
    ax.pie(percentiles, explode=explode, labels=labels, colors=colors,
           autopct='%1.1f%%', shadow=True)
    ax.set_aspect('equal')
    canvas = FigureCanvas(fig)
    stream = cStringIO.StringIO()
    canvas.print_png(stream)
    return stream.getvalue()


# Created by Weikai Wu
