import numpy as np
import matplotlib.pyplot as plt
import time

plt.ion()
plt.style.use('ggplot')

class SingleQHistogram(object):
    """Bar chart for single q values"""
    def __init__(self, action_size, action_names, width = 0.25, y_lim = 10):
        super(SingleQHistogram, self).__init__()
        self.action_size = action_size
        self.action_names = action_names
        self.width = width
        self.y_lim = y_lim
        self.fig, self.ax = plt.subplots()
        self.bar = None


    def render(self, q_values, title = 'Why did I make the move?'):
        if self.bar is None:
            x_pos = np.arange(self.action_size)
            self.bar = self.ax.bar(x_pos, q_values, self.width, align='center')
            self.ax.set_xticks(x_pos)
            self.ax.set_xticklabels(self.action_names)
            self.ax.set_xlabel('Q Value')
            self.ax.set_title(title)
            self.ax.set_ylim([-self.y_lim, self.y_lim])
            plt.show()
            plt.pause(0.001)
        else:
            for i, b in enumerate(self.bar):
                b.set_height(q_values[i])

            self.ax.autoscale_view()
            self.fig.canvas.flush_events()
            plt.pause(0.001)
        pass


class MultiQHistogram(object):
    """Bar chart for single q values"""
    def __init__(self, reward_size, action_size, action_names, width = 0.25, ylim = 10):
        super(MultiQHistogram, self).__init__()
        self.reward_size = reward_size
        self.action_size = action_size
        self.action_names = action_names
        self.fig, self.ax = plt.subplots()
        self.width = width
        self.ylim = ylim
        self.bars = []
        self.labels = []

    def render(self, q_values, q_labels,  title =  "Why did I make the move?"):
        if len(self.bars) == 0:
            x_pos = np.arange(self.action_size)
            for reward_type in range(self.reward_size):
                bar = self.ax.bar(x_pos + (reward_type * self.width),
                                  q_values[reward_type],
                                  self.width,
                                  align='center')
                self.bars.append(bar)
            self.ax.set_xticks(x_pos + (self.width * self.reward_size / 2) )
            self.ax.set_xticklabels(self.action_names)
            self.ax.set_xlabel('Q Value')
            self.ax.set_title(title)
            self.ax.spines['right'].set_visible(False)
            self.ax.spines['top'].set_visible(False)
            self.ax.legend(self.bars, q_labels, bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure)
            # self.ax.set_ylim[-self.ylim, self.ylim])
            plt.show()
            plt.pause(0.001)
        else:
            for reward_type in range(self.reward_size):
                for i, bar in enumerate(self.bars[reward_type]):
                    height = q_values[reward_type][i]
                    bar.set_height(height)

            plt.autoscale(enable=True, axis='y')
            max_q_value = np.max(q_values)
            min_q_value = np.min(q_values)
            self.ax.set_ylim([min_q_value - 2, max_q_value + 2])
            # self.ax.autoscale_view()
            self.fig.canvas.flush_events()
            plt.pause(0.001)
        pass