all_questions = []

ans_array = [["<60kg", 0], ["60-70kg", 2], ["70-90", 1], [">90kg", 0]]
all_questions.append(["What is your weight?", ans_array])

ans_array = [["<150cm", 0], ["150-165cm", 1], ["165-180cm", 2], [">180cm", 1]]
all_questions.append(["What is your height?", ans_array])

ans_array = [["full", 0], ["athletic", 2], ["thin", 1]]
all_questions.append(["What is your physique?", ans_array])

ans_array = [["I have never practiced", 0], ["I have been doing it for up to half a year", 1], ["I have been doing it for more than half a year", 2]]
all_questions.append(["What is your practice experience?", ans_array])

ans_array = [["up to 10", 0], [" 10-30", 1], ["30+", 2]]
all_questions.append(["How much can you push up?", ans_array])

ans_array = [["up to 3", 0], ["3-8", 1], ["8+", 2]]
all_questions.append(["How much do you pull up?", ans_array])

ans_array = [["increase the number of repetitions", 1], ["gain muscle mass", 2], ["lose weight", 0]]
all_questions.append(["What is the goal of your training?", ans_array])

ans_array = [["up to 20", 0], ["up to 50", 1], ["up to 100", 2], ["100+", 3]]
all_questions.append(["How many times can you sit down?", ans_array])

ans_array = [["Yes, practicing it every day", 3], ["Partially", 1], ["Nope", 0]]
all_questions.append(["Do you like walking/running in the morning?", ans_array])

ans_array = [["Yes", 2], ["No", 0]]
all_questions.append(["Have you been doing cardio lately?", ans_array])

ans_array = [["High, accurately created", 2], ["Medium, nothing special", 1], ["Low, a lot of fast-food", 0]]
all_questions.append(["What do you think is the quality of your diet?", ans_array])

ans_array = [["Yes, severe", -3], ["A few", 0], ["I have a decent health", 2], ["I have an exceptional health ", 5]]
all_questions.append(["do you have serious health problems?", ans_array])
