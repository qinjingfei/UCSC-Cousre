import matplotlib.pyplot as plt
import sys

# data input
# times are in minute
Productive = ['Math117', 'Cmps104a', 'Cmps115', 'Cmps183']
Prod_times = [55.0, 135.0, 42.0, 102.0]
NonProductive = ['Music','Video Games', 'TV']
NP_times = [5, 90.0, 30.0]

# mircro color list
ColorList = ['whitesmoke', 'rosybrown', 'firebrick', 'r', 'darksalmon',
             'sienna', 'sandybrown', 'bisque', 'tan', 'moccasin',
             'floralwhite', 'gold', 'darkkhaki', 'lightgoldenrodyellow',
             'olivedrab', 'chartreuse', 'darksage', 'lightgreen',
             'green', 'mediumseagreen', 'mediumaquamarine',
             'mediumturquoise', 'darkslategrey', 'c', 'cadetblue',
             'skyblue', 'dodgerblue', 'slategray']

# sector labels
labels = Productive + NonProductive

# calculate the percentages of each task
time_list = Prod_times + NP_times
total_time = sum(time_list)
percentages = [t / total_time for t in time_list]

# colors that used in the graph, sublist of the mircro color list
if len(labels) > len(ColorList): sys.exit("too many tasks")
colors = ColorList[:len(labels)]

# the productive tasks should be exploded
explode = [0.1] * len(Productive) + [0.0] * len(NonProductive)

# make the graph
plt.title('All Tasks', y = 1.05)
plt.pie(percentages, explode=explode, labels=labels, colors=colors,
        autopct = '%1.1f%%', shadow=True, startangle=90)
# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')


# Productive task figure
pfig1 = plt.figure()
ax1 = pfig1.gca()
ax1.set_title('Productive Tasks')
Prod_len = len(Prod_times)
explode1 = [0.0] * Prod_len
explode1[Prod_times.index(max(Prod_times))] = 0.1
ax1.pie([t / sum(Prod_times) for t in Prod_times], explode = explode1,
        labels = Productive, colors = ColorList[:Prod_len],
        autopct = '%1.1f%%', shadow=True, startangle=90)
ax1.set_aspect('equal')


# Non-Productive task figure
pfig2 = plt.figure()
ax1 = pfig2.gca()
ax1.set_title('Non-Productive Tasks')
NP_len = len(NP_times)
explode2 = [0.0] * NP_len
explode2[NP_times.index(max(NP_times))] = 0.1
ax1.pie([t / sum(NP_times) for t in NP_times], explode = explode2,
        labels = NonProductive, colors = ColorList[:NP_len],
        autopct = '%1.1f%%', shadow=True, startangle=90)
ax1.set_aspect('equal')

plt.show()
