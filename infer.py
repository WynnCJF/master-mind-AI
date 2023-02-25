import random

color_set = ['red', 'green', 'blue', 'white',
             'brown', 'pink', 'orange', 'yellow']


def find_color_diff(guess1, guess2):
    """Find the color difference between two consecutive guesses."""
    change = []
    incre = []
    decre = []
    for c in guess2:
        if c not in guess1:
            incre.append(c)
    for c in guess1:
        if c not in guess2:
            decre.append(c)

    for (g1, g2) in zip(decre, incre):
        change.append((g1, g2))

    return change

def correct(c, assume_correct, assume_incorrect):
    if c not in assume_correct: assume_correct.append(c)
    if c in assume_incorrect: assume_incorrect.remove(c)

def incorrect(c, assume_correct, assume_incorrect):
    if c not in assume_incorrect: assume_incorrect.append(c)
    if c in assume_correct: assume_correct.remove(c)

def analyze_color(guesses, corrects, i, assume_correct, assume_incorrect):
    """Recursive function to return the list of potential correct colors."""
    if i >= len(guesses): return
    if i == 0:
        correct_num = corrects[0]
        guess = guesses[0]

        if correct_num == 0:
            assume_correct.clear()
            assume_correct += [c for c in color_set if c not in guess]
            return
        elif correct_num == 4:
            assume_correct.clear()
            assume_correct += guess
            return
        elif correct_num == 3:
            for guess_c in guess:
                assume_correct.clear()
                assume_correct += [c for c in guess if c != guess_c]
                assume_incorrect.clear()
                assume_incorrect += [guess_c]
                analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
            assume_correct.clear()
            assume_incorrect.clear()
            return
        elif correct_num == 2:
            for guess_c_1 in guess:
                for guess_c_2 in guess:
                    if guess_c_1 != guess_c_2:
                        assume_correct.clear()
                        assume_correct += [c for c in guess if c != guess_c_1 and c != guess_c_2]
                        assume_incorrect.clear()
                        assume_incorrect += [c for c in guess if c == guess_c_1 or c == guess_c_2]
                        analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                        if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
            assume_correct.clear()
            assume_incorrect.clear()
            return
        elif correct_num == 1:
            for guess_c in guess:
                assume_correct.clear()
                assume_correct += [guess_c]
                assume_incorrect.clear()
                assume_incorrect += [c for c in guess if c != guess_c]
                analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
            assume_correct.clear()
            assume_incorrect.clear()
            return

    if i >= 1:
        cur_guess = guesses[i]
        prev_guess = guesses[i - 1]
        cur_correct = corrects[i]
        prev_correct = corrects[i - 1]
        diff = find_color_diff(prev_guess, cur_guess)

        if cur_correct == prev_correct + 1:
            if len(diff) == 1:
                c1 = diff[0][0]
                d1 = diff[0][1]
                # c1 -> d1: incorrect -> correct
                if c1 in assume_correct or d1 in assume_incorrect:
                    assume_correct.clear()
                    assume_incorrect.clear()
                    return

                correct(d1, assume_correct, assume_incorrect)
                incorrect(c1, assume_correct, assume_incorrect)
                analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                return
            if len(diff) == 2:
                c1 = diff[0][0]
                d1 = diff[0][1]
                c2 = diff[1][0]
                d2 = diff[1][1]

                # Assume c1 -> d1: incorrect -> correct, c2 -> d2: correct -> correct
                if c1 not in assume_correct and d1 not in assume_incorrect and c2 not in assume_incorrect and d2 not in assume_incorrect:
                    incorrect(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> correct, c2 -> d2: incorrect -> incorrect
                if c1 not in assume_correct and d1 not in assume_incorrect and c2 not in assume_correct and d2 not in assume_correct:
                    incorrect(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: correct -> correct, c2 -> d2: incorrect -> correct
                if c1 not in assume_incorrect and d1 not in assume_incorrect and c2 not in assume_correct and d2 not in assume_incorrect:
                    correct(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> incorrect, c2 -> d2: incorrect -> correct
                if c1 not in assume_correct and d1 not in assume_correct and c2 not in assume_correct and d2 not in assume_incorrect:
                    incorrect(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return

                # Controversy occurs
                assume_correct.clear()
                assume_incorrect.clear()
                return

            if len(diff) == 3:
                c1 = diff[0][0]
                d1 = diff[0][1]
                c2 = diff[1][0]
                d2 = diff[1][1]
                c3 = diff[2][0]
                d3 = diff[2][1]

                # Assume c1 -> d1: incorrect -> correct, c2 -> d2: correct -> correct, c3 -> d3: correct -> correct
                if c1 not in assume_correct and d1 not in assume_incorrect and c2 not in assume_incorrect and d2 not in assume_incorrect and c3 not in assume_incorrect and d3 not in assume_incorrect:
                    incorrect(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> correct, c2 -> d2: incorrect -> incorrect, c3 -> d3: incorrect -> incorrect
                if c1 not in assume_correct and d1 not in assume_incorrect and c2 not in assume_correct and d2 not in assume_correct and c3 not in assume_correct and d3 not in assume_correct:
                    incorrect(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> correct, c2 -> d2: incorrect -> incorrect, c3 -> d3: correct -> correct
                if c1 not in assume_correct and d1 not in assume_incorrect and c2 not in assume_correct and d2 not in assume_correct and c3 not in assume_incorrect and d3 not in assume_incorrect:
                    incorrect(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> correct, c2 -> d2: correct -> correct, c3 -> d3: incorrect -> incorrect
                if c1 not in assume_correct and d1 not in assume_incorrect and c2 not in assume_incorrect and d2 not in assume_incorrect and c3 not in assume_correct and d3 not in assume_correct:
                    incorrect(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: correct -> correct, c2 -> d2: incorrect -> correct, c3 -> d3: correct -> correct
                if c1 not in assume_incorrect and d1 not in assume_incorrect and c2 not in assume_correct and d2 not in assume_incorrect and c3 not in assume_incorrect and d3 not in assume_incorrect:
                    correct(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> incorrect, c2 -> d2: incorrect -> correct, c3 -> d3: incorrect -> incorrect
                if c1 not in assume_correct and d1 not in assume_correct and c2 not in assume_correct and d2 not in assume_incorrect and c3 not in assume_correct and d3 not in assume_correct:
                    incorrect(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> incorrect, c2 -> d2: incorrect -> correct, c3 -> d3: correct -> correct
                if c1 not in assume_correct and d1 not in assume_correct and c2 not in assume_correct and d2 not in assume_incorrect and c3 not in assume_incorrect and d3 not in assume_incorrect:
                    incorrect(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: correct -> correct, c2 -> d2: incorrect -> correct, c3 -> d3: incorrect -> incorrect
                if c1 not in assume_incorrect and d1 not in assume_incorrect and c2 not in assume_correct and d2 not in assume_incorrect and c3 not in assume_correct and d3 not in assume_correct:
                    correct(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: correct -> correct, c2 -> d2: correct -> correct, c3 -> d3: incorrect -> correct
                if c1 not in assume_incorrect and d1 not in assume_incorrect and c2 not in assume_incorrect and d2 not in assume_incorrect and c3 not in assume_correct and d3 not in assume_incorrect:
                    correct(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> incorrect, c2 -> d2: incorrect -> incorrect, c3 -> d3: incorrect -> correct
                if c1 not in assume_correct and d1 not in assume_correct and c2 not in assume_correct and d2 not in assume_correct and c3 not in assume_correct and d3 not in assume_incorrect:
                    incorrect(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> incorrect, c2 -> d2: correct -> correct, c3 -> d3: incorrect -> correct
                if c1 not in assume_correct and d1 not in assume_correct and c2 not in assume_incorrect and d2 not in assume_incorrect and c3 not in assume_correct and d3 not in assume_incorrect:
                    incorrect(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: correct -> correct, c2 -> d2: incorrect -> incorrect, c3 -> d3: incorrect -> correct
                if c1 not in assume_incorrect and d1 not in assume_incorrect and c2 not in assume_correct and d2 not in assume_correct and c3 not in assume_correct and d3 not in assume_incorrect:
                    correct(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> correct, c2 -> d2: incorrect -> correct, c3 -> d3: correct -> incorrect
                if c1 not in assume_correct and d1 not in assume_incorrect and c2 not in assume_correct and d2 not in assume_incorrect and c3 not in assume_incorrect and d3 not in assume_correct:
                    incorrect(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> correct, c2 -> d2: correct -> incorrect, c3 -> d3: incorrect -> correct
                if c1 not in assume_correct and d1 not in assume_incorrect and c2 not in assume_incorrect and d2 not in assume_correct and c3 not in assume_correct and d3 not in assume_incorrect:
                    incorrect(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: correct -> incorrect, c2 -> d2: incorrect -> correct, c3 -> d3: incorrect -> correct
                if c1 not in assume_incorrect and d1 not in assume_correct and c2 not in assume_correct and d2 not in assume_incorrect and c3 not in assume_correct and d3 not in assume_incorrect:
                    correct(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return

                # Controversy occurs
                assume_correct.clear()
                assume_incorrect.clear()
                return


        elif cur_correct == prev_correct - 1:
            if len(diff) == 1:
                c1 = diff[0][0]
                d1 = diff[0][1]
                # Change from a correct one to an incorrect one
                if c1 in assume_incorrect or d1 in assume_correct:
                    assume_correct.clear()
                    assume_incorrect.clear()
                    return

                correct(c1, assume_correct, assume_incorrect)
                incorrect(d1, assume_correct, assume_incorrect)
                analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                return

            if len(diff) == 2:
                c1 = diff[0][0]
                d1 = diff[0][1]
                c2 = diff[1][0]
                d2 = diff[1][1]

                # Assume c1 -> d1: correct -> incorrect, c2 -> d2: correct -> correct
                if c1 not in assume_incorrect and d1 not in assume_correct and c2 not in assume_incorrect and d2 not in assume_incorrect:
                    correct(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: correct -> incorrect, c2 -> d2: incorrect -> incorrect
                if c1 not in assume_incorrect and d1 not in assume_correct and c2 not in assume_correct and d2 not in assume_correct:
                    correct(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: correct -> correct, c2 -> d2: correct -> incorrect
                if c1 not in assume_incorrect and d1 not in assume_incorrect and c2 not in assume_incorrect and d2 not in assume_correct:
                    correct(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> incorrect, c2 -> d2: correct -> incorrect
                if c1 not in assume_correct and d1 not in assume_correct and c2 not in assume_correct and d2 not in assume_incorrect:
                    incorrect(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return

                # Controversy occurs
                assume_correct.clear()
                assume_incorrect.clear()
                return

            if len(diff) == 3:
                c1 = diff[0][0]
                d1 = diff[0][1]
                c2 = diff[1][0]
                d2 = diff[1][1]
                c3 = diff[2][0]
                d3 = diff[2][1]

                # Assume c1 -> d1: correct -> incorrect, c2 -> d2: correct -> correct, c3 -> d3: correct -> correct
                if c1 not in assume_incorrect and d1 not in assume_correct and c2 not in assume_incorrect and d2 not in assume_incorrect and c3 not in assume_incorrect and d3 not in assume_incorrect:
                    correct(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: correct -> incorrect, c2 -> d2: incorrect -> incorrect, c3 -> d3: incorrect -> incorrect
                if c1 not in assume_incorrect and d1 not in assume_correct and c2 not in assume_correct and d2 not in assume_correct and c3 not in assume_correct and d3 not in assume_correct:
                    correct(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: correct -> incorrect, c2 -> d2: incorrect -> incorrect, c3 -> d3: correct -> correct
                if c1 not in assume_incorrect and d1 not in assume_correct and c2 not in assume_correct and d2 not in assume_correct and c3 not in assume_incorrect and d3 not in assume_incorrect:
                    correct(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: correct -> incorrect, c2 -> d2: correct -> correct, c3 -> d3: incorrect -> incorrect
                if c1 not in assume_incorrect and d1 not in assume_correct and c2 not in assume_incorrect and d2 not in assume_incorrect and c3 not in assume_correct and d3 not in assume_correct:
                    correct(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: correct -> correct, c2 -> d2: correct -> incorrect, c3 -> d3: correct -> correct
                if c1 not in assume_incorrect and d1 not in assume_incorrect and c2 not in assume_incorrect and d2 not in assume_correct and c3 not in assume_incorrect and d3 not in assume_incorrect:
                    correct(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> incorrect, c2 -> d2: correct -> incorrect, c3 -> d3: incorrect -> incorrect
                if c1 not in assume_correct and d1 not in assume_correct and c2 not in assume_incorrect and d2 not in assume_correct and c3 not in assume_correct and d3 not in assume_correct:
                    incorrect(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> incorrect, c2 -> d2: correct -> incorrect, c3 -> d3: correct -> correct
                if c1 not in assume_correct and d1 not in assume_correct and c2 not in assume_incorrect and d2 not in assume_correct and c3 not in assume_incorrect and d3 not in assume_incorrect:
                    incorrect(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: correct -> correct, c2 -> d2: correct -> incorrect, c3 -> d3: incorrect -> incorrect
                if c1 not in assume_incorrect and d1 not in assume_incorrect and c2 not in assume_incorrect and d2 not in assume_correct and c3 not in assume_correct and d3 not in assume_correct:
                    correct(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: correct -> correct, c2 -> d2: correct -> correct, c3 -> d3: correct -> incorrect
                if c1 not in assume_incorrect and d1 not in assume_incorrect and c2 not in assume_incorrect and d2 not in assume_incorrect and c3 not in assume_incorrect and d3 not in assume_correct:
                    correct(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> incorrect, c2 -> d2: incorrect -> incorrect, c3 -> d3: correct -> incorrect
                if c1 not in assume_correct and d1 not in assume_correct and c2 not in assume_correct and d2 not in assume_correct and c3 not in assume_incorrect and d3 not in assume_correct:
                    incorrect(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> incorrect, c2 -> d2: correct -> correct, c3 -> d3: correct -> incorrect
                if c1 not in assume_correct and d1 not in assume_correct and c2 not in assume_incorrect and d2 not in assume_incorrect and c3 not in assume_incorrect and d3 not in assume_correct:
                    incorrect(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: correct -> correct, c2 -> d2: incorrect -> incorrect, c3 -> d3: correct -> incorrect
                if c1 not in assume_incorrect and d1 not in assume_incorrect and c2 not in assume_correct and d2 not in assume_correct and c3 not in assume_incorrect and d3 not in assume_correct:
                    correct(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> correct, c2 -> d2: correct -> incorrect, c3 -> d3: correct -> incorrect
                if c1 not in assume_correct and d1 not in assume_incorrect and c2 not in assume_incorrect and d2 not in assume_correct and c3 not in assume_incorrect and d3 not in assume_correct:
                    incorrect(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: correct -> incorrect, c2 -> d2: incorrect -> correct, c3 -> d3: correct -> incorrect
                if c1 not in assume_incorrect and d1 not in assume_correct and c2 not in assume_correct and d2 not in assume_incorrect and c3 not in assume_incorrect and d3 not in assume_correct:
                    correct(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    inrrect(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: correct -> incorrect, c2 -> d2: correct -> incorrect, c3 -> d3: incorrect -> correct
                if c1 not in assume_incorrect and d1 not in assume_correct and c2 not in assume_incorrect and d2 not in assume_correct and c3 not in assume_correct and d3 not in assume_incorrect:
                    correct(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return

                # Controversy occurs
                assume_correct.clear()
                assume_incorrect.clear()
                return

        elif cur_correct == prev_correct:
            if len(diff) == 1:
                c1 = diff[0][0]
                d1 = diff[0][1]

                # Assume c1 -> d1: correct -> correct
                if c1 not in assume_incorrect and d1 not in assume_incorrect:
                    correct(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return

                # Assume c1 -> d1: incorrect -> correct
                if c1 not in assume_correct and d1 not in assume_correct:
                    incorrect(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return

                # Controversy occurs
                assume_correct.clear()
                assume_incorrect.clear()
                return

            if len(diff) == 2:
                c1 = diff[0][0]
                d1 = diff[0][1]
                c2 = diff[1][0]
                d2 = diff[1][1]

                # Assume c1 -> d1: correct -> correct, c2 -> d2: correct -> correct
                if c1 not in assume_incorrect and d1 not in assume_incorrect and c2 not in assume_incorrect and d2 not in assume_incorrect:
                    correct(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> incorrect, c2 -> d2: incorrect -> incorrect
                if c1 not in assume_correct and d1 not in assume_correct and c2 not in assume_correct and d2 not in assume_correct:
                    incorrect(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: correct -> correct, c2 -> d2: incorrect -> incorrect
                if c1 not in assume_incorrect and d1 not in assume_incorrect and c2 not in assume_correct and d2 not in assume_correct:
                    correct(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> incorrect, c2 -> d2: correct -> correct
                if c1 not in assume_correct and d1 not in assume_correct and c2 not in assume_incorrect and d2 not in assume_incorrect:
                    incorrect(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: correct -> incorrect, c2 -> d2: incorrect -> correct
                if c1 not in assume_incorrect and d1 not in assume_correct and c2 not in assume_correct and d2 not in assume_incorrect:
                    correct(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # Assume c1 -> d1: incorrect -> correct, c2 -> d2: correct -> incorrect
                if c1 not in assume_correct and d1 not in assume_incorrect and c2 not in assume_incorrect and d2 not in assume_correct:
                    incorrect(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return

                # Controversy occurs
                assume_correct.clear()
                assume_incorrect.clear()
                return

            if len(diff) == 3:
                c1 = diff[0][0]
                d1 = diff[0][1]
                c2 = diff[1][0]
                d2 = diff[1][1]
                c3 = diff[2][0]
                d3 = diff[2][1]

                # c1 -> d1: incorrect -> incorrect, c2 -> d2: correct -> correct, c3 -> d3: correct -> correct
                if c1 not in assume_correct and d1 not in assume_correct and c2 not in assume_incorrect and d2 not in assume_incorrect and c3 not in assume_incorrect and d3 not in assume_incorrect:
                    incorrect(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # c1 -> d1: correct -> correct, c2 -> d2: incorrect -> incorrect, c3 -> d3: correct -> correct
                if c1 not in assume_incorrect and d1 not in assume_incorrect and c2 not in assume_correct and d2 not in assume_correct and c3 not in assume_incorrect and d3 not in assume_incorrect:
                    correct(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # c1 -> d1: correct -> correct, c2 -> d2: correct -> correct, c3 -> d3: incorrect -> incorrect
                if c1 not in assume_incorrect and d1 not in assume_incorrect and c2 not in assume_incorrect and d2 not in assume_incorrect and c3 not in assume_correct and d3 not in assume_correct:
                    correct(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # c1 -> d1: correct -> correct, c2 -> d2: incorrect -> incorrect, c3 -> d3: incorrect -> incorrect
                if c1 not in assume_incorrect and d1 not in assume_incorrect and c2 not in assume_correct and d2 not in assume_correct and c3 not in assume_correct and d3 not in assume_correct:
                    correct(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # c1 -> d1: incorrect -> incorrect, c2 -> d2: correct -> correct, c3 -> d3: incorrect -> incorrect
                if c1 not in assume_correct and d1 not in assume_correct and c2 not in assume_incorrect and d2 not in assume_incorrect and c3 not in assume_correct and d3 not in assume_correct:
                    incorrect(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # c1 -> d1: incorrect -> incorrect, c2 -> d2: incorrect -> incorrect, c3 -> d3: correct -> correct
                if c1 not in assume_correct and d1 not in assume_correct and c2 not in assume_correct and d2 not in assume_correct and c3 not in assume_incorrect and d3 not in assume_incorrect:
                    incorrect(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return

                # Controversy occurs
                assume_correct.clear()
                assume_incorrect.clear()
                return

        elif cur_correct == prev_correct + 2:
            if len(diff) <= 1:
                # Controversy occurs
                assume_correct.clear()
                assume_incorrect.clear()
                return
            elif len(diff) == 2:
                c1 = diff[0][0]
                d1 = diff[0][1]
                c2 = diff[1][0]
                d2 = diff[1][1]

                # c1 -> d1: incorrect -> correct, c2 -> d2: incorrect -> correct
                if c1 in assume_correct or d1 in assume_incorrect or c2 in assume_correct or d2 in assume_incorrect:
                    assume_correct.clear()
                    assume_incorrect.clear()
                    return

                incorrect(c1, assume_correct, assume_incorrect)
                correct(d1, assume_correct, assume_incorrect)
                incorrect(c2, assume_correct, assume_incorrect)
                correct(d2, assume_correct, assume_incorrect)
                analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                return

            elif len(diff) == 3:
                c1 = diff[0][0]
                d1 = diff[0][1]
                c2 = diff[1][0]
                d2 = diff[1][1]
                c3 = diff[2][0]
                d3 = diff[2][1]

                # c1 -> d1: correct -> correct, c2 -> d2: incorrect -> correct, c3 -> d3: incorrect -> correct
                if c1 not in assume_incorrect and d1 not in assume_incorrect and c2 not in assume_correct and d2 not in assume_incorrect and c3 not in assume_correct and d3 not in assume_incorrect:
                    correct(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # c1 -> d1: incorrect -> incorrect, c2 -> d2: incorrect -> correct, c3 -> d3: incorrect -> correct
                if c1 not in assume_correct and d1 not in assume_correct and c2 not in assume_correct and d2 not in assume_incorrect and c3 not in assume_correct and d3 not in assume_incorrect:
                    incorrect(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # c1 -> d1: incorrect -> correct, c2 -> d2: correct -> correct, c3 -> d3: incorrect -> correct
                if c1 not in assume_correct and d1 not in assume_incorrect and c2 not in assume_incorrect and d2 not in assume_incorrect and c3 not in assume_correct and d3 not in assume_incorrect:
                    incorrect(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # c1 -> d1: incorrect -> correct, c2 -> d2: incorrect -> incorrect, c3 -> d3: incorrect -> correct
                if c1 not in assume_correct and d1 not in assume_incorrect and c2 not in assume_correct and d2 not in assume_correct and c3 not in assume_correct and d3 not in assume_incorrect:
                    incorrect(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # c1 -> d1: incorrect -> correct, c2 -> d2: incorrect -> correct, c3 -> d3: correct -> correct
                if c1 not in assume_correct and d1 not in assume_incorrect and c2 not in assume_correct and d2 not in assume_incorrect and c3 not in assume_incorrect and d3 not in assume_incorrect:
                    incorrect(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # c1 -> d1: incorrect -> correct, c2 -> d2: incorrect -> correct, c3 -> d3: incorrect -> incorrect
                if c1 not in assume_correct and d1 not in assume_incorrect and c2 not in assume_correct and d2 not in assume_incorrect and c3 not in assume_correct and d3 not in assume_correct:
                    incorrect(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return

                # Controversy occurs
                assume_correct.clear()
                assume_incorrect.clear()
                return

        elif cur_correct == prev_correct - 2:
            if len(diff) <= 1:
                # Controversy occurs
                assume_correct.clear()
                assume_incorrect.clear()
                return
            elif len(diff) == 2:
                c1 = diff[0][0]
                d1 = diff[0][1]
                c2 = diff[1][0]
                d2 = diff[1][1]

                # c1 -> d1: correct -> incorrect, c2 -> d2: correct -> incorrect
                if c1 in assume_incorrect or d1 in assume_correct or c2 in assume_incorrect or d2 in assume_correct:
                    assume_correct.clear()
                    assume_incorrect.clear()
                    return

                correct(c1, assume_correct, assume_incorrect)
                incorrect(d1, assume_correct, assume_incorrect)
                correct(c2, assume_correct, assume_incorrect)
                incorrect(d2, assume_correct, assume_incorrect)
                analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                return
            elif len(diff) == 3:
                c1 = diff[0][0]
                d1 = diff[0][1]
                c2 = diff[1][0]
                d2 = diff[1][1]
                c3 = diff[2][0]
                d3 = diff[2][1]

                # c1 -> d1: correct -> correct, c2 -> d2: correct -> incorrect, c3 -> d3: correct -> incorrect
                if c1 not in assume_incorrect and d1 not in assume_incorrect and c2 not in assume_incorrect and d2 not in assume_correct and c3 not in assume_incorrect and d3 not in assume_correct:
                    correct(c1, assume_correct, assume_incorrect)
                    correct(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # c1 -> d1: incorrect -> incorrect, c2 -> d2: correct -> incorrect, c3 -> d3: correct -> incorrect
                if c1 not in assume_correct and d1 not in assume_correct and c2 not in assume_incorrect and d2 not in assume_correct and c3 not in assume_incorrect and d3 not in assume_correct:
                    incorrect(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # c1 -> d1: correct -> incorrect, c2 -> d2: correct -> correct, c3 -> d3: correct -> incorrect
                if c1 not in assume_incorrect and d1 not in assume_correct and c2 not in assume_incorrect and d2 not in assume_incorrect and c3 not in assume_incorrect and d3 not in assume_correct:
                    correct(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    correct(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # c1 -> d1: correct -> incorrect, c2 -> d2: incorrect -> incorrect, c3 -> d3: correct -> incorrect
                if c1 not in assume_incorrect and d1 not in assume_correct and c2 not in assume_correct and d2 not in assume_correct and c3 not in assume_incorrect and d3 not in assume_correct:
                    correct(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    incorrect(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # c1 -> d1: correct -> incorrect, c2 -> d2: correct -> incorrect, c3 -> d3: correct -> correct
                if c1 not in assume_incorrect and d1 not in assume_correct and c2 not in assume_incorrect and d2 not in assume_correct and c3 not in assume_incorrect and d3 not in assume_incorrect:
                    correct(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    correct(c3, assume_correct, assume_incorrect)
                    correct(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return
                # c1 -> d1: correct -> incorrect, c2 -> d2: correct -> incorrect, c3 -> d3: incorrect -> incorrect
                if c1 not in assume_incorrect and d1 not in assume_correct and c2 not in assume_incorrect and d2 not in assume_correct and c3 not in assume_correct and d3 not in assume_correct:
                    correct(c1, assume_correct, assume_incorrect)
                    incorrect(d1, assume_correct, assume_incorrect)
                    correct(c2, assume_correct, assume_incorrect)
                    incorrect(d2, assume_correct, assume_incorrect)
                    incorrect(c3, assume_correct, assume_incorrect)
                    incorrect(d3, assume_correct, assume_incorrect)
                    analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                    if (len(assume_correct) != 0 and len(assume_incorrect) != 0) and not (len(assume_correct) < 4 and len(assume_correct) + len(assume_incorrect) >= 8) and not (8 - len(assume_correct) - len(assume_incorrect) < 4 - len(assume_correct)) and len(assume_correct) <= 4 and (assume_correct not in guesses): return

                # Controversy occurs
                assume_correct.clear()
                assume_incorrect.clear()
                return

        elif cur_correct == prev_correct + 3:
            if len(diff) <= 2:
                # Controversy occurs
                assume_correct.clear()
                assume_incorrect.clear()
                return
            elif len(diff) == 3:
                c1 = diff[0][0]
                d1 = diff[0][1]
                c2 = diff[1][0]
                d2 = diff[1][1]
                c3 = diff[2][0]
                d3 = diff[2][1]

                # c1 -> d1: incorrect -> correct, c2 -> d2: incorrect -> correct, c3 -> d3: incorrect -> correct
                if c1 in assume_correct or d1 in assume_incorrect or c2 in assume_correct or d2 in assume_incorrect or c3 in assume_correct or d3 in assume_incorrect:
                    assume_correct.clear()
                    assume_incorrect.clear()
                    return

                incorrect(c1, assume_correct, assume_incorrect)
                correct(d1, assume_correct, assume_incorrect)
                incorrect(c2, assume_correct, assume_incorrect)
                correct(d2, assume_correct, assume_incorrect)
                incorrect(c3, assume_correct, assume_incorrect)
                correct(d3, assume_correct, assume_incorrect)
                analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                return

        elif cur_correct == prev_correct + 3:
            if len(diff) <= 2:
                # Controversy occurs
                assume_correct.clear()
                assume_incorrect.clear()
                return
            elif len(diff) == 3:
                c1 = diff[0][0]
                d1 = diff[0][1]
                c2 = diff[1][0]
                d2 = diff[1][1]
                c3 = diff[2][0]
                d3 = diff[2][1]

                # c1 -> d1: correct -> incorrect, c2 -> d2: correct -> incorrect, c3 -> d3: correct -> incorrect
                if c1 in assume_incorrect or d1 in assume_correct or c2 in assume_incorrect or d2 in assume_correct or c3 in assume_incorrect or d3 in assume_correct:
                    assume_correct.clear()
                    assume_incorrect.clear()
                    return

                correct(c1, assume_correct, assume_incorrect)
                incorrect(d1, assume_correct, assume_incorrect)
                correct(c2, assume_correct, assume_incorrect)
                incorrect(d2, assume_correct, assume_incorrect)
                correct(c3, assume_correct, assume_incorrect)
                incorrect(d3, assume_correct, assume_incorrect)
                analyze_color(guesses, corrects, i + 1, assume_correct, assume_incorrect)
                return


color_map = {
    'red': '🟥',
    'green': '🟩',
    'blue': '🟦',
    'pink': '🟪',
    'brown': '🟫',
    'orange': '🟧',
    'white': '⬜️',
    'yellow': '🟨'
}

if __name__ == "__main__":
    # random.seed(13)
    intro_str = " ".join([color_map[c] for c in color_set])
    print(f"Think of 4 colors from the list: {intro_str}")
    print("After each of my guess, tell the the number of colors I get correct.\n")
    
    input("Press ENTER to start.\n")
    
    round = 0
    assume_correct = []
    assume_incorrect = []
    guesses = []
    corrects = []
    first_guess = random.sample(color_set, 4)
    first_guess_str = " ".join([color_map[c] for c in first_guess])
    score = int(input(f'\nGuess: {first_guess_str}\nScore: '))
    guesses.append(first_guess)
    corrects.append(score)
    analyze_color(guesses=guesses,
                  corrects=corrects,
                  i=0,
                  assume_correct=assume_correct,
                  assume_incorrect=assume_incorrect)
    
    round += 1
    others = [
        c for c in color_set
        if c not in assume_correct and c not in assume_incorrect
    ]
    
    # print(f"\tAssume correct: {assume_correct}")
    # print(f"\tAssume incorrect: {assume_incorrect}")
    # print(f"\tOther: {others}")

    while corrects[round - 1] < 4:
        next_guess = assume_correct + others[:4 - len(assume_correct)]
        if next_guess == guesses[round - 1]:
            next_guess = assume_correct + others[len(assume_correct) -
                                                 4:len(others)]

        next_guess_str = " ".join([color_map[c] for c in next_guess])
        next_score = int(input(f'\nGuess: {next_guess_str}\nScore: '))
        
        guesses.append(next_guess)
        corrects.append(next_score)
        analyze_color(guesses=guesses,
                      corrects=corrects,
                      i=0,
                      assume_correct=assume_correct,
                      assume_incorrect=assume_incorrect)
        
        others = [
            c for c in color_set
            if c not in assume_correct and c not in assume_incorrect
        ]
        
        round += 1

    correct_sol_str = " ".join([color_map[c] for c in guesses[round - 1]])
    print("\nAll correct, the chosen colors are:", correct_sol_str)