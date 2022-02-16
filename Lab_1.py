t = 3295

intensity = 2556

gamma = 0.53

work_hours = [3544, 20, 207, 1796, 327, 285, 732, 551,
956, 642, 169, 5, 137, 616, 1352, 302, 271,
9, 13, 408, 45, 738, 854, 640, 131, 1921,
472, 1092, 166, 703, 155, 406, 223, 1070,
286, 431, 375, 208, 449, 151, 39, 129, 487,
17, 185, 302, 494, 695, 7, 204, 195, 121,
1438, 311, 121, 455, 4, 361, 647, 540, 125,
704, 7, 99, 628, 387, 193, 106, 1022, 1434,
684, 76, 144, 761, 45, 672, 852, 872, 1215,
1970, 42, 18, 529, 244, 1104, 1130, 2751,
2134, 657, 867, 692, 61, 222, 122, 296, 789,
408, 1138, 150, 1049]

work_hours.sort()

sumed_work_hours = 0
for i in work_hours:
    sumed_work_hours += i
avarage = sumed_work_hours/len(work_hours)

print("Sorted hours: ", work_hours)
print("Avarage: ", avarage)

max_hours = work_hours[-1]
h = work_hours[-1]/10

print("Max hours: ", max_hours)
print("Length: ", h)

intervals = []
i = 0
for _ in range(11):
    intervals.append(i)
    i += h

print("Intervals: ", intervals)    
frequensy_possibilities = []
for i in range(len(intervals) - 1):
    times = []
    for time in work_hours:
        if intervals[i] < time <= intervals[i + 1]:
            times.append(time)
    frequensy_possibilities.append(len(times) / (len(work_hours) * h))
print("Failure probability: ", frequensy_possibilities)  


probabilities = []

for time in intervals:
    frequensies = 0
    for i in range(0, int(time // h)):
        frequensies += frequensy_possibilities[i]
    
    current_frequensy_possibilities = frequensy_possibilities[int(time // h)] if not int(time // h) >= len(frequensy_possibilities) else 0
    integral = frequensies * h + current_frequensy_possibilities * (time % h)
    probabilities.append(1 - integral)

print("Probabilities: ", probabilities)

t_y_index = 0
for i in range(len(probabilities)):
    if probabilities[i] <= gamma:
        t_y_index = i
        break

print("T_y index: ", t_y_index)

t_i = t_y_index * h
t_i_decreased = (t_y_index - 1) * h


frequensies_t_i = 0
for i in range(0, int(t_i // h)):
    frequensies_t_i += frequensy_possibilities[i]

integral_t_i = frequensies_t_i * h + frequensy_possibilities[int(t_i // h)] * (t_i % h)

frequensies_t_i_decreased = 0
for i in range(0, int(t_i_decreased // h)):
    frequensies_t_i_decreased += frequensy_possibilities[i]

integral_t_i_decreased = frequensies_t_i_decreased * h + frequensy_possibilities[int(frequensies_t_i_decreased // h)] * (t_i_decreased % h)

t_y = t_i - h * (1 - integral_t_i - gamma) / ((1 - integral_t_i) - (1 - integral_t_i_decreased))


print("T_y : ", t_y)

frequensies_t = 0
for i in range(0, int(t // h)):
    frequensies_t += frequensy_possibilities[i]

probability_of_failure_free_operation = 1 - (frequensies_t * h + frequensy_possibilities[int(t // h)] * (t % h))

print("Probability of failure free operation : ", probability_of_failure_free_operation)

intensities = 0
for i in range(0, int(intensity // h)):
    intensities += frequensy_possibilities[i]

failure_intensity = frequensy_possibilities[int(intensity // h)] / (1 - (intensities * h + frequensy_possibilities[int(intensity // h)] * (intensity % h)))

print("Failure intensity : ", failure_intensity)
