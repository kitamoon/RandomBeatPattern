import numpy as np
import random


def generator():    # generating 64 random beat patterns
    drums = []
    for i in range(0, 64):
        beat_pattern = [np.random.choice([0, 1], size=32, p=[8. / 10, 2. / 10]),    # kick
                        np.random.choice([0, 1], size=32, p=[7. / 10, 3. / 10]),    # snare drum
                        np.random.choice([0, 1], size=32, p=[4. / 10, 6. / 10])]    # hi-hat
        drums.append(beat_pattern)
    return drums


def selector(x):
    points = 0
    total_points = []
    for key in range(len(x)):   # criteria based rating
        for i in range(0, 32):
            if x[key][0][i % 8] == 1:
                points += 5
            if x[key][0][i % 4] == 1:
                points += 5
            if x[key][0][0] == 1:
                points += 5
            if x[key][0][(i+1) % 2] == 1:
                points += 5
            if x[key][0][i] == 1 and x[key][1][i] == 1 and x[key][2][i] == 1:
                points -= 1
        total_points.append(points)
        points = 0

    idx = []
    while len(idx) < 32:    # selecting best patterns
        for s in range(len(total_points)):
            if total_points[s] == max(total_points):
                if len(x) == 32:
                    return x[s]
                idx.append(s)
                total_points[s] = min(total_points) - 1
                break

    selected = []
    for i in idx:
        selected.append(x[i])
    random.shuffle(selected)
    return selected


def crossing(population):
    parents_1 = population[:16]
    parents_2 = population[16:]
    crossed = []
    cut1 = np.random.randint(0, 31)
    cut2 = np.random.randint(0, 31)
    for p in range(len(parents_2)):
        crossed.append([[*parents_1[p][0][:cut1], *parents_2[p][0][cut1:]],
                        [*parents_1[p][1][:cut1], *parents_2[p][1][cut1:]],
                        [*parents_1[p][2][:cut1], *parents_2[p][2][cut1:]]])
        crossed.append([[*parents_1[p][0][:cut2], *parents_2[p][0][cut2:]],
                        [*parents_1[p][1][:cut2], *parents_2[p][1][cut2:]],
                        [*parents_1[p][2][:cut2], *parents_2[p][2][cut2:]]])
        crossed.append([[*parents_2[p][0][:cut1], *parents_1[p][0][cut1:]],
                        [*parents_2[p][1][:cut1], *parents_1[p][1][cut1:]],
                        [*parents_2[p][2][:cut1], *parents_1[p][2][cut1:]]])
        crossed.append([[*parents_2[p][0][:cut2], *parents_1[p][0][cut2:]],
                        [*parents_2[p][1][:cut2], *parents_1[p][1][cut2:]],
                        [*parents_2[p][2][:cut2], *parents_1[p][2][cut2:]]])
    return crossed


def save_to_ly(patterns):
    with open('score.ly', 'w') as f:
        f.write(r'''\version "2.22.0"''')
        f.write('\n' + r'''\drums {''')
        f.write(' '.join(beat for beat in patterns[0]))
        f.write(" }" + '\n' + r'''\drums { ''')
        f.write(' '.join(beat for beat in patterns[1]))
        f.write(" }" + '\n' + r'''\drums { ''')
        f.write(' '.join(beat for beat in patterns[2]))
        f.write(" }")
        f.close()


def main():
    result = selector(crossing(selector(generator())))
    final_result = selector(result)

    for i in range(len(final_result[0])):   # naming beats
        if final_result[0][i] == 1:
            final_result[0][i] = 'bd8'
        elif final_result[0][i] == 0:
            final_result[0][i] = 'r8'
        if final_result[1][i] == 1:
            final_result[1][i] = 'sn8'
        elif final_result[1][i] == 0:
            final_result[1][i] = 'r8'
        if final_result[2][i] == 1:
            final_result[2][i] = 'hh8'
        elif final_result[2][i] == 0:
            final_result[2][i] = 'r8'
    save_to_ly(final_result)


if __name__ == "__main__":

    main()
