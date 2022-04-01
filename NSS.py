import numpy as np
import matplotlib.pyplot as plt 
import random

plt.rcParams['image.cmap'] = 'binary'

def well_init(m_cols):
	initial_state = [0 for i in range(cols)]
	spacing = 2 / cols
	prev = 1

	for i in range(int(.5 * cols)):
		initial_state[i] = prev
		prev = prev - spacing

	for i in range(int(.5 * cols), cols):
		initial_state[i] = prev
		prev = prev + spacing

	return initial_state


def center_init(m_cols):
	initial_state = [1 for i in range(cols)]
	initial_state[m_cols // 2] = 0
	return initial_state

# makes 2d list of NSS showing only n_frames frames equally spaced
# of the evolution
def nss_summary_plot(nss_grid, n_frames):
	summary_grid = [[0] * len(nss_grid[0]) for i in range(n_frames)]
	spacing = len(nss_grid) // n_frames

	for i in range(n_frames):
		summary_grid[i] = nss_grid[i * spacing]

	return summary_grid


def evolve_cont(a):
	l,c,r = a
	birth_rate = (l + c) / 2
	death_rate = (c + (1 - r)) / 2
	c = .5 * (birth_rate + death_rate)
	return c

def evolve_simple(a):
	l,c,r = a
	delta = l - r
	c += delta
	if c < 0:
		c = 0
	elif c > 1:
		c = 1
	return c

def evolve_cont_ns(a):
	l,c,r = a
	l_pull = .5 * (l + c) # avg of l and c
	r_push = .5 * (3*c - r) # avg of c and c + (c-r)
	c = .5 * (l_pull + r_push) # = avg of push and pull
	if c < 0:
		return 0
	elif c > 1:
		return 1
	return c

def evolve_na(a):
	return a[1]

# Evolves the system for n_steps
def NSSEvolve(initial_state, n_steps, evolve_rule):
	m_cols = len(initial_state)

	grid = [[0] * m_cols for i in range(n_steps + 1)]

	grid[0] = initial_state

	for step in range(n_steps):
		minimum = grid[step][0]
		mindex = 0
		i = 0
		for e in grid[step]:
			if (e < minimum):
				minimum = e
				mindex = i

			l = grid[step][i - 1]
			c = grid[step][i]
			r = grid[step][(i + 1) % m_cols]
			grid[step + 1][i] = evolve_rule([l,c,r]) # e
			i = i + 1

		grid[step + 1][mindex - 1] = random.random()
		grid[step + 1][mindex] = random.random()
		grid[step + 1][(mindex + 1) % m_cols] = random.random()

	return grid




# Make list of y values for mean fitness at each time step
def avg_plot(nss_grid):
	m_cols = len(nss_grid[0])
	n_steps = len(nss_grid)

	avg_time_plot = [0 for i in range(n_steps)]

	for i in range(n_steps):
		total = 0
		for j in nss_grid[i]:
			total += j
		avg_time_plot[i] = total / m_cols

	return avg_time_plot


# Compare current values of cells against previous values and creates
# list of frequencies that each cell changes
def stability_plot(nss_grid):
	n_steps = len(nss_grid)
	m_cols = len(nss_grid[0])
	stability_plot = [0 for i in range(m_cols)]

	prev = nss_grid[0]

	# compare current step against last step, update frequency table
	for step in range(1, n_steps):
		curr = nss_grid[step]
		for i in range(m_cols):
			if (curr[i] != prev[i]): # if value differs from prev step
				stability_plot[i] += 1
		prev = nss_grid[step]

	return stability_plot

def sorted_plot(stability_plot_list):
	return sorted(stability_plot_list)

def freq_plot(stability_plot_list, n_bins):
	maximum = max(stability_plot_list)
	spacing = maximum // n_bins
	freq_list = [0 for i in range(n_bins)]

	sorted_list = sorted_plot(stability_plot_list)
	
	for i in sorted_list:
		bin_range_max = spacing

		for i_bin in range(n_bins):
			if (i < bin_range_max):
				freq_list[i_bin] += 1
				break
			else:
				bin_range_max += spacing

	return freq_list




cols = 100
steps = 1000
initial_state = [random.random() for i in range(cols)]
#initial_state = well_init(cols)
#initial_state = center_init(cols)

nss = NSSEvolve(initial_state, steps, evolve_na)
nss_summary = nss_summary_plot(nss, 200)
nss_stability_plot = stability_plot(nss)
nss_sorted_plot = sorted_plot(nss_stability_plot)
nss_freq_list = freq_plot(nss_stability_plot, 25)

plt.matshow(nss)
plt.matshow(nss_summary)
plt.show()

plt.plot(avg_plot(nss))
plt.show()

plt.plot(nss_stability_plot)
plt.plot(nss_sorted_plot)
plt.show()

plt.plot(nss_freq_list)
plt.show()

#plt.plot(nss_freq_list)
#plt.yscale("log")
#plt.show()









