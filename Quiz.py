from PIL import ImageTk, Image
import matplotlib.pyplot
from tkinter import ttk
import captcha.image
import googletrans
import playsound
import threading
import datetime
import tkinter
import string
import random
import json
import gtts
import os

question_file = open("Questions.json")
question_json = json.load(question_file)
lang_and_code = {"Bengali": "bn", "Chinese": "zh-cn", "English": "en", "French": "fr", "Hindi": "hi", "Punjabi": "pa", "Russian": "ru", "Spanish": "es", "Tamil": "ta"}
key_value_pair = {32: 94, 33: 106, 34: 71, 35: 108, 36: 121, 37: 45, 38: 68, 39: 42, 40: 80, 41: 51, 42: 125, 43: 61, 44: 105, 45: 33, 46: 59, 47: 86, 48: 119, 49: 93, 50: 54, 51: 64, 52: 67, 53: 81, 54: 60, 55: 44, 56: 69, 57: 117, 58: 32, 59: 43, 60: 101, 61: 79, 62: 50, 63: 97, 64: 123, 65: 122, 66: 98, 67: 115, 68: 102, 69: 85, 70: 66, 71: 55, 72: 99, 73: 56, 74: 35, 75: 76, 76: 36, 77: 47, 78: 113, 79: 111, 80: 112, 81: 87, 82: 74, 83: 107, 84: 78, 85: 49, 86: 91, 87: 109, 88: 57, 89: 103, 90: 82, 91: 104, 92: 89, 93: 75, 94: 118, 95: 46, 96: 39, 97: 88, 98: 92, 99: 62, 100: 41, 101: 83, 102: 52, 103: 48, 104: 34, 105: 70, 106: 38, 107: 40, 108: 124, 109: 58, 110: 37, 111: 96, 112: 114, 113: 95, 114: 63, 115: 73, 116: 72, 117: 90, 118: 53, 119: 100, 120: 84, 121: 126, 122: 110, 123: 120, 124: 116, 125: 65, 126: 77}
key_list = list(key_value_pair.keys())
value_list = list(key_value_pair.values())

def encrypt(password):
    hashed_password = ""
    for i in password:
        hashed_password += chr(key_value_pair[ord(i)])
    encrypted_password = ""
    for i in hashed_password:
        encrypted_password += chr(random.choice(key_list)) + i
    return encrypted_password

def decrypt(encrypted_password):
    unsalted_password = ""
    for i in range(1, len(encrypted_password), 2):
        unsalted_password += encrypted_password[i]
    original_password = ""
    for i in unsalted_password:
        original_password += chr(key_list[value_list.index(ord(i))])
    return original_password

def find_color(per):
    if per == 100:
        return "green"
    elif 75 <= per < 100:
        return "limegreen"
    elif 50 <= per < 75:
        return "lime"
    elif 25 <= per < 50:
        return "yellow"
    elif 0 < per < 25:
        return "orange"
    elif per == 0:
        return "tomato"
    elif -25 <= per < 0:
        return "peru"
    elif -50 <= per < -25:
        return "red"
    elif -75 <= per < -50:
        return "crimson"
    elif -100 < per < -75:
        return "maroon"
    elif per == -100:
        return "black"

def show_summary_plot(summary_list):
    plot_window = tkinter.Toplevel()
    plot_window.geometry("+740+320")
    plot_window.title("Result Summary")
    title = []
    colour_list = []
    summary_list.reverse()
    for a in range(0, len(summary_list)):
        title.append(str(a+1))
        colour_list.append(find_color(summary_list[a]))
    matplotlib.pyplot.bar(title, summary_list, color = colour_list)
    matplotlib.pyplot.xlabel("Test number")
    matplotlib.pyplot.ylabel("Percentage")
    file_name = "plot.png"
    matplotlib.pyplot.savefig(file_name)
    matplotlib.pyplot.close()
    image = Image.open(file_name)
    resized_image = image.resize((int(275 / image.height * image.width), 275))
    resized_image.save(file_name)
    tkinter_image = tkinter.PhotoImage(file = file_name)
    image_label = ttk.Label(plot_window, image = tkinter_image)
    image_label.pack()
    os.remove(file_name)
    plot_window.mainloop()

def detail_result(record):
    result_window = tkinter.Toplevel()
    result_window.title("Result")
    marks_gained = (record[-1]).count(1) * int(record[-3])
    marks_loosed = abs((record[-1]).count(-1) * int(record[-2]))
    final_marks = marks_gained - marks_loosed
    if final_marks < 0:
        percentage = round((final_marks * -100) / (len(record[-1]) * int(record[-2])), 2)
    else:
        percentage = round((final_marks * 100) / (len(record[-1]) * int(record[-3])), 2)
    subject_name = ttk.Label(result_window, text = "Subject : " + record[1])
    subject_name.config(font = ("Aharoni", 18, "bold"))
    ques_no_title = ttk.Label(result_window, text = "Question number")
    ques_no_title.config(font = ("Arial Rounded MT Bold", 10))
    status_title = ttk.Label(result_window, text = "Status")
    status_title.config(font = ("Arial Rounded MT Bold", 10))
    marks_title = ttk.Label(result_window, text = "Marks\t")
    marks_title.config(font = ("Arial Rounded MT Bold", 10))
    subject_name.grid(row = 0, column = 1)
    ques_no_title.grid(row = 1, column = 0) 
    status_title.grid(row = 1, column = 1)
    marks_title.grid(row = 1, column = 2)
    for a in range(0, len(record[-1])):
        ques_no = a + 2
        if (record[-1])[a] == 0:
            status = "Unanswered"
            marks = 0
            colour = "gray"
        if (record[-1])[a] == 1:
            status = "Correct"
            marks = int(record[-3])
            colour = "green"
        if (record[-1])[a] == -1:
            status = "Incorrect"
            marks = int(record[-2])
            colour = "red"
        ques_no_label = ttk.Label(result_window, text = str(ques_no-1))
        ques_no_label.config(foreground = colour)
        status_label = ttk.Label(result_window, text = status)
        status_label.config(foreground = colour)
        marks_label = ttk.Label(result_window, text = str(marks))
        marks_label.config(foreground = colour)
        ques_no_label.grid(row = ques_no, column = 0)
        status_label.grid(row = ques_no, column = 1)
        marks_label.grid(row = ques_no, column = 2)
    file_name = "Plot.png"
    available_file = os.listdir()
    if file_name in available_file:
        os.remove(file_name)
    response_type = ["Correct : " + str((record[-1]).count(1)), "Incorrect : " + str((record[-1]).count(-1)), "Unanswered : " + str((record[-1]).count(0))]
    response_number = [(record[-1]).count(1), (record[-1]).count(-1), (record[-1]).count(0)]
    colour = ["green", "red", "gray"]
    matplotlib.pyplot.pie(response_number, labels = response_type, colors = colour)
    matplotlib.pyplot.savefig(file_name)
    matplotlib.pyplot.close()
    image = Image.open(file_name)
    resized_image = image.resize((int(275 / image.height * image.width), 275))
    croped_image = resized_image.crop((30, 30, 348, 250))
    croped_image.save(file_name)
    plot = tkinter.PhotoImage(file = file_name)
    plot_label = ttk.Label(result_window, image = plot)
    total_mark_label = ttk.Label(result_window, text = "Total marks : " + str(len(record[-1]) * int(record[-3])))
    marks_label = ttk.Label(result_window, text = "Marks : " + str(final_marks))
    percentage_label = ttk.Label(result_window, text = "Percentage : " + str(percentage))
    ok = ttk.Button(result_window, text = "OK", command = result_window.destroy)
    plot_label.grid(row = 3 + len(record[-1]), column = 1)
    os.remove(file_name)
    total_mark_label.grid(row = 4 + len(record[-1]), column = 1)
    marks_label.grid(row = 5 + len(record[-1]), column = 1)
    percentage_label.grid(row = 6 + len(record[-1]), column = 1)
    ok.grid(row = 7 + len(record[-1]), column = 1)
    result_window.geometry("+750+90")
    result_window.mainloop()

def split(date_time):
    date = (date_time.split())[0]
    time = (date_time.split())[1]
    date_split = date.split("/")
    time_split = time.split(":")
    return [int(date_split[2]), int(date_split[1]), int(date_split[0]), int(time_split[0]), int(time_split[1])]

def sort_by_time(unsorted_list):
    for i in range(0, len(unsorted_list)):
        for j in range(i+1, len(unsorted_list)):
            if split((unsorted_list[i])[0]) < split((unsorted_list[j])[0]):
                temp = unsorted_list[i]
                unsorted_list[i] = unsorted_list[j]
                unsorted_list[j] = temp
    return unsorted_list

def find_per(responses):
    total_pos_marks = len(responses[2]) * responses[0]
    total_neg_marks = len(responses[2]) * responses[1]
    marks_gained = (responses[2]).count(1) * responses[0]
    marks_loosed = abs((responses[2]).count(-1) * responses[1])
    final_marks = marks_gained - marks_loosed
    if final_marks >= 0:
        return round(final_marks * 100 / total_pos_marks, 2)
    else:
        return round(final_marks * -100 / total_neg_marks, 2)

def show_record(user_name):
    history_window = tkinter.Toplevel()
    history_window.title("Previous Quizzes")
    record_file = open("History.txt")
    is_present = False
    for account in record_file:
        try:
            json_account = json.loads(account)
        except json.decoder.JSONDecodeError:
            break
        if json_account["user_name"] == user_name:
            is_present = True
            percentage_list = []
            record = []
            time_title = ttk.Label(history_window, text = "      Date and Time\t")
            time_title.config(font = ("Arial Rounded MT Bold", 10))
            subject_title = ttk.Label(history_window, text = "Subject\t")
            subject_title.config(font = ("Arial Rounded MT Bold", 10))
            no_of_ques_title = ttk.Label(history_window, text = "Number of questions  ")
            no_of_ques_title.config(font = ("Arial Rounded MT Bold", 10))
            correct_title = ttk.Label(history_window, text = "Correct\t")
            correct_title.config(font = ("Arial Rounded MT Bold", 10))
            incorrect_title = ttk.Label(history_window, text = "Incorect\t")
            incorrect_title.config(font = ("Arial Rounded MT Bold", 10))
            skipped_title = ttk.Label(history_window, text = "Unanswered   ")
            skipped_title.config(font = ("Arial Rounded MT Bold", 10))
            percentage_title = ttk.Label(history_window, text = "Percentage    ")
            percentage_title.config(font = ("Arial Rounded MT Bold", 10))
            time_title.grid(row = 0, column = 0)
            subject_title.grid(row = 0, column = 1)
            no_of_ques_title.grid(row = 0, column = 2)
            correct_title.grid(row = 0, column = 3)
            incorrect_title.grid(row = 0, column = 4)
            skipped_title.grid(row = 0, column = 5)
            percentage_title.grid(row = 0, column = 6)
            for subject in json_account["subject"]:
                for test_no in eval((json_account["subject"])[subject]):
                    date_and_time = str(test_no[3][0]) + "/" + str(test_no[3][1]) + "/" + str(test_no[3][2]) + " " + str(test_no[3][3]) + ":" + str(test_no[3][4])
                    test_list = [date_and_time, subject, str(len(test_no[2])), str((test_no[2]).count(1)), str((test_no[2]).count(-1)), str((test_no[2]).count(0)), str(find_per(test_no)), str(test_no[0]), str(test_no[1]), test_no[2]]
                    record.append(test_list)
            sr_no = 0
            record = sort_by_time(record)
            for i in range(0, len(record)):
                sr_no += 1
                time_label = ttk.Label(history_window, text = (record[i])[0])
                subject_label = ttk.Label(history_window, text = (record[i])[1])
                no_of_ques_label = ttk.Label(history_window, text = (record[i])[2])
                correct_label = ttk.Label(history_window, text = (record[i])[3])
                incorrect_label = ttk.Label(history_window, text = (record[i])[4])
                skipped_label = ttk.Label(history_window, text = (record[i])[5])
                percentage_label = ttk.Label(history_window, text = (record[i])[6])
                percentage_list.append(float((record[i])[6]))
                more_details = ttk.Button(history_window, text = "More Details", command = lambda j = i : detail_result(record[j]))
                time_label.grid(row = sr_no, column = 0)
                subject_label.grid(row = sr_no, column = 1)
                no_of_ques_label.grid(row = sr_no, column = 2)
                correct_label.grid(row = sr_no, column = 3)
                incorrect_label.grid(row = sr_no, column = 4)
                skipped_label.grid(row = sr_no, column = 5)
                percentage_label.grid(row = sr_no, column = 6)
                more_details.grid(row = sr_no, column = 7)
            button = ttk.Button(history_window, text = "Analyze your progress", command = lambda : show_summary_plot(percentage_list))
            button.grid(row = sr_no+1, column = 2, columnspan = 2)
            history_window.geometry("+345+10")
            history_window.mainloop()
            break
    if is_present == False:
        history_window.geometry("+345+240")
        empty_label = ttk.Label(history_window, text = "You have not given any quiz before")
        ok = ttk.Button(history_window, text = "OK", command = history_window.destroy)
        empty_label.grid(row = 0, column = 0)
        ok.grid(row = 1, column = 0)
        history_window.mainloop()

def add_marks(id, sub, cor, ico, det_res, time):
    curr_time = [time.day, time.month, time.year, time.hour, time.minute]
    history_file = open("History.txt", "a")
    to_write = '{"user_name" : ' + '"' + id + '"' + ', "subject" : {' + '"' + sub.get() + '" :' + ' "[[' + str(cor.get()) + ', ' + str(ico.get()) + ', ' + str(det_res) + ', ' + str(curr_time) + '' + ']]"}}\n'
    history_file.write(to_write)
    history_file.close()

def modify_marks(id, sub, cor, ico, det_res, time):
    curr_time = [time.day, time.month, time.year, time.hour, time.minute]
    history_file = open("History.txt", "r+")
    account_and_result = []
    for account in history_file:
        try:
            json_account = json.loads(account)
        except json.decoder.JSONDecodeError:
            break
        if json_account["user_name"] == id:
            pre_sub = list((json_account["subject"]).keys())
            if sub.get() in pre_sub:
                to_add = '[' + str(cor.get()) + ', ' + str(ico.get()) + ', ' + str(det_res) + ', ' + str(curr_time) + '], '
                index = account.find(sub.get())
                modified = account[: index + len(sub.get()) + 6] + to_add + account[index + len(sub.get()) + 6 :]
                account_and_result.append(modified)
            else:
                to_add = ', "' + sub.get() + '" : ' + '"[[' + str(cor.get()) + ', ' + str(ico.get()) + ', ' + str(det_res) + ', ' + str(curr_time) + ']]"}'
                modified = account[:-3] + to_add + account[-2:]
                account_and_result.append(modified)
        else:
            account_and_result.append(account)
    history_file.seek(0)
    history_file.writelines(account_and_result)
    history_file.close()

def show_result(id, sub, cor, ico, det_res, to_save, to_des):
    if to_save == True:
        history_file = open("History.txt")
        present = False
        for account in history_file:
            try:
                json_account = json.loads(account)
            except json.decoder.JSONDecodeError:
                break
            if json_account["user_name"] == id:
                present = True
                break
        current_time = datetime.datetime.now()
        if present:
            modify_marks(id, sub, cor, ico, det_res, current_time)
        else:
            add_marks(id, sub, cor, ico, det_res, current_time)
    else:
        to_des.destroy()
    result_window = tkinter.Toplevel()
    result_window.title("Result")
    marks_gained = det_res.count(1) * cor.get()
    marks_loosed = abs(det_res.count(-1) * ico.get())
    final_marks = marks_gained - marks_loosed
    if final_marks < 0:
        percentage = round((final_marks * -100) / (len(det_res) * ico.get()), 2)
    else:
        percentage = round((final_marks * 100) / (len(det_res) * cor.get()), 2)
    subject_name = ttk.Label(result_window, text = "Subject : " + sub.get())
    subject_name.config(font = ("Aharoni", 18, "bold"))
    ques_no_title = ttk.Label(result_window, text = "Question number")
    ques_no_title.config(font = ("Arial Rounded MT Bold", 10))
    status_title = ttk.Label(result_window, text = "Status")
    status_title.config(font = ("Arial Rounded MT Bold", 10))
    marks_title = ttk.Label(result_window, text = "Marks\t")
    marks_title.config(font = ("Arial Rounded MT Bold", 10))
    subject_name.grid(row = 0, column = 1)
    ques_no_title.grid(row = 1, column = 0) 
    status_title.grid(row = 1, column = 1)
    marks_title.grid(row = 1, column = 2)
    for a in range(0, len(det_res)):
        ques_no = a + 2
        if det_res[a] == 0:
            status = "Unanswered"
            marks = 0
            colour = "gray"
        if det_res[a] == 1:
            status = "Correct"
            marks = cor.get()
            colour = "green"
        if det_res[a] == -1:
            status = "Incorrect"
            marks = ico.get()
            colour = "red"
        ques_no_label = ttk.Label(result_window, text = str(ques_no-1))
        ques_no_label.config(foreground = colour)
        status_label = ttk.Label(result_window, text = status)
        status_label.config(foreground = colour)
        marks_label = ttk.Label(result_window, text = str(marks))
        marks_label.config(foreground = colour)
        ques_no_label.grid(row = ques_no, column = 0)
        status_label.grid(row = ques_no, column = 1)
        marks_label.grid(row = ques_no, column = 2)
    file_name = "Plot.png"
    available_file = os.listdir()
    if file_name in available_file:
        os.remove(file_name)
    response_type = ["Correct : " + str(det_res.count(1)), "Incorrect : " + str(det_res.count(-1)), "Unanswered : " + str(det_res.count(0))]
    response_number = [det_res.count(1), det_res.count(-1), det_res.count(0)]
    colour = ["green", "red", "gray"]
    matplotlib.pyplot.pie(response_number, labels = response_type, colors = colour)
    matplotlib.pyplot.savefig(file_name)
    matplotlib.pyplot.close()
    image = Image.open(file_name)
    resized_image = image.resize((int(275 / image.height * image.width), 275))
    croped_image = resized_image.crop((30, 30, 348, 250))
    croped_image.save(file_name)
    plot = tkinter.PhotoImage(file = file_name)
    plot_label = ttk.Label(result_window, image = plot)
    total_mark_label = ttk.Label(result_window, text = "Total marks : " + str(len(det_res) * cor.get()))
    marks_label = ttk.Label(result_window, text = "Marks : " + str(final_marks))
    percentage_label = ttk.Label(result_window, text = "Percentage : " + str(percentage))
    ok = ttk.Button(result_window, text = "OK", command = result_window.destroy)
    plot_label.grid(row = 3 + len(det_res), column = 1)
    os.remove(file_name)
    total_mark_label.grid(row = 4 + len(det_res), column = 1)
    marks_label.grid(row = 5 + len(det_res), column = 1)
    percentage_label.grid(row = 6 + len(det_res), column = 1)
    ok.grid(row = 7 + len(det_res), column = 1)
    result_window.geometry("+750+90")
    result_window.mainloop()

def find_response(op1, op2, op3, op4):
    try:
        if op1[0] == "selected":
            return 1
    except IndexError:
        try:
            if op2[0] == "selected":
                return 2
        except IndexError:
            try:
                if op3[0] == "selected":
                    return 3
            except IndexError:
                try:
                    if op4[0] == "selected":
                        return 4
                except IndexError:
                    return 0

def submit_quiz(id, sub, cor, ico, pre_pre_win, pre_win, corr_opt, sel_opt):
    pre_win.destroy()
    pre_pre_win.destroy()
    det_res = []
    for i in range(0, len(sel_opt)):
        if sel_opt[i] == 0:
            det_res.append(0)
        elif sel_opt[i] == corr_opt[i]:
            det_res.append(1)
        else:
            det_res.append(-1)
    show_result(id, sub, cor, ico, det_res, True, "")

def not_submit(conf_win, pre_win):
    conf_win.destroy()
    pre_win.deiconify()

def confirm_submit_quiz(id, sub, cor, ico, pre_win, corr_opt, sel_opt):
    pre_win.withdraw()
    confirm_window = tkinter.Toplevel()
    confirm_window.geometry("+700+170")
    confirm_window.title("Confirm your Submission")
    confirm_message = ttk.Label(confirm_window, text = "Are you sure, you want to submit")
    yes_button = ttk.Button(confirm_window, text = "Yes", command = lambda : submit_quiz(id, sub, cor, ico, pre_win, confirm_window, corr_opt, sel_opt))
    no_button = ttk.Button(confirm_window, text = "No", command = lambda : not_submit(confirm_window, pre_win))
    confirm_message.grid(row = 0, column = 0, columnspan = 2)
    yes_button.grid(row = 1, column = 0)
    no_button.grid(row = 1, column = 1)
    confirm_window.mainloop()

def change_lang(event):
    translator = googletrans.Translator()
    to_translate = ((question_json[subject.get()])["question"])[que_ord[cur]] + "\n" + (((question_json[subject.get()])["options"])[que_ord[cur]])[0] + "\n" + (((question_json[subject.get()])["options"])[que_ord[cur]])[1] + "\n" + (((question_json[subject.get()])["options"])[que_ord[cur]])[2] + "\n" + (((question_json[subject.get()])["options"])[que_ord[cur]])[3]
    translated_text = translator.translate(to_translate, scr = "en", dest = lang_and_code[lang_var.get()])
    translated_text_split = (translated_text.text).split("\n")
    question_label.config(text = translated_text_split[0])
    option_1.config(text = translated_text_split[1])
    option_2.config(text = translated_text_split[2])
    option_3.config(text = translated_text_split[3])
    option_4.config(text = translated_text_split[4])

def change_ques(to_save, sub, ques_seq, sel_opt, mark_list, to_mark, pre_que_idx, que_idx, question_no_label, question_label, option_1, option_2, option_3, option_4, to_clear, lang_var):
    if pre_que_idx == len(ques_seq) - 1 and que_idx == len(ques_seq):
        que_idx = 0
    question_no_label.config(text = str(que_idx+1) + ".")
    translator = googletrans.Translator()
    to_translate = ((question_json[sub.get()])["question"])[ques_seq[que_idx]] + "\n" + (((question_json[sub.get()])["options"])[ques_seq[que_idx]])[0] + "\n" + (((question_json[sub.get()])["options"])[ques_seq[que_idx]])[1] + "\n" + (((question_json[sub.get()])["options"])[ques_seq[que_idx]])[2] + "\n" + (((question_json[sub.get()])["options"])[ques_seq[que_idx]])[3]
    translated_text = translator.translate(to_translate, scr = "en", dest = lang_and_code[lang_var.get()])
    translated_text_split = (translated_text.text).split("\n")
    question_label.config(text = translated_text_split[0])
    if to_save == True:
        pre_res = find_response(option_1.state(), option_2.state(), option_3.state(), option_4.state())
        sel_opt[pre_que_idx] = pre_res
    if to_mark == True:
        mark_list[pre_que_idx] = 1
    if to_clear == True:
        sel_opt[que_idx] = 0
        mark_list[que_idx] = 0
    global response, cur, subject, que_ord
    que_ord = ques_seq
    subject = sub
    cur = que_idx
    response.set(sel_opt[que_idx])
    option_1.config(text = translated_text_split[1])
    option_2.config(text = translated_text_split[2])
    option_3.config(text = translated_text_split[3])
    option_4.config(text = translated_text_split[4])
    ans = unans = ans_mark = unans_mark = 0
    for i in range(0, len(ques_seq)):
        if sel_opt[i] != 0 and mark_list[i] == 0:
            ans += 1
            colour = "lime"
        elif sel_opt[i] != 0 and mark_list[i] == 1:
            ans_mark += 1
            colour = "yellow"
        elif sel_opt[i] == 0 and mark_list[i] == 0:
            unans += 1
            colour = "red"
        elif sel_opt[i] == 0 and mark_list[i] == 1:
            unans_mark += 1
            colour = "orange"
        if i == que_idx:
            colour = "white"
        ques_but = tkinter.Button(question_window, text = i+1, bg = colour, command = lambda j = i : change_ques(False, sub, ques_seq, sel_opt, mark_list, False, cur, j, question_no_label, question_label, option_1, option_2, option_3, option_4, False, lang_var))
        ques_but.config(width = 3)
        ques_but.place(x = 850, y = 150+((225-50)/len(ques_seq))*(i))
    ans_label = tkinter.Label(question_window, text = "Answered : " + str(ans), bg = "lime")
    unans_label = tkinter.Label(question_window, text = "Unanswered : " + str(unans), bg = "red")
    ans_mark_label = tkinter.Label(question_window, text = "Answered and Marked for Review : " + str(ans_mark), bg = "yellow")
    unans_mark_label = tkinter.Label(question_window, text = "Unanswered and Marked for Review : " + str(unans_mark), bg = "orange")
    ans_label.place(x = 20, y = 20)
    unans_label.place(x = 320, y = 20)
    ans_mark_label.place(x = 20, y = 50)
    unans_mark_label.place(x = 320, y = 50)
    language_label = ttk.Label(question_window, text = "Language")
    language_label.place(x = 620, y = 10)
    language = ttk.Combobox(question_window, textvariable = lang_var, width = 10)
    language.config(values = ["Bengali", "Chinese", "English", "French", "Hindi", "Punjabi", "Russian", "Spanish", "Tamil"])
    language.bind("<<ComboboxSelected>>", change_lang)
    language.place(x = 680, y = 10)

def change_time(timer_label, id, sub, cor, ico, corr_opt, sel_opt, pre_win):
    old_text = timer_label["text"]
    old_min = int(old_text.split(":")[0])
    old_sec = int(old_text.split(":")[1])
    time_in_sec = old_min * 60 + old_sec
    time_in_sec -= 1
    new_min = time_in_sec // 60
    new_sec = time_in_sec % 60
    if time_in_sec == -1:
        current_time = datetime.datetime.now()
        det_res = []
        for i in range(0, len(sel_opt)):
            if sel_opt[i] == 0:
                det_res.append(0)
            elif sel_opt[i] == corr_opt[i]:
                det_res.append(1)
            else:
                det_res.append(-1)
        history_file = open("History.txt")
        present = False
        for account in history_file:
            try:
                json_account = json.loads(account)
            except json.decoder.JSONDecodeError:
                break
            if json_account["user_name"] == id:
                present = True
                break
        if present:
            modify_marks(id, sub, cor, ico, det_res, current_time)
        else:
            add_marks(id, sub, cor, ico, det_res, current_time)
        pre_win.destroy()
        time_up_window = tkinter.Toplevel()
        time_up_window.geometry("+600+200")
        time_up_window.title("Time's up")
        message_label = ttk.Label(time_up_window, text = "  Time's up, Your quiz is submitted")
        result_button = ttk.Button(time_up_window, text = "Show Result", command = lambda : show_result(id, sub, cor, ico, det_res, False, time_up_window))
        message_label.grid(row = 0, column = 0)
        result_button.grid(row = 1, column = 0)
        time_up_window.mainloop()
    else:
        time_text = "0" * (2 - len(str(new_min))) + str(new_min) + " : " + "0" * (2 - len(str(new_sec))) + str(new_sec)
        timer_label.config(text = time_text)
        timer_label.after(1000, lambda : change_time(timer_label, id, sub, cor, ico, corr_opt, sel_opt, pre_win))

def is_fine(to_test):
    try:
        int(to_test)
        return True
    except ValueError:
        return False

def speak(question_label):
    global audio_no
    sound = gtts.gTTS(question_label["text"])
    file_name = "Audio_" + str(audio_no) + ".mp3"
    audio_no += 1
    sound.save(file_name)
    playsound.playsound(file_name)
    os.remove(file_name)

def threaded_sound(question_label):
    t1 = threading.Thread(target = lambda : speak(question_label))
    t1.start()

def start_quiz(id, sub, ques_count, cor, ico, min, sec, window):
    correct = 0
    if is_fine(ques_count.get()) == True:
        correct += 1
    if is_fine(cor.get()) == True:
        correct += 1
    if is_fine(ico.get()) == True:
        correct += 1
    if is_fine(min.get()) == True:
        correct += 1
    if is_fine(sec.get()) == True:
        correct += 1
    subject_available = ["Geography", "History", "Chemistry", "Physics", "General Knowledge"]
    if correct == 5:
        int_count = int(ques_count.get())
        int_cor = int(cor.get())
        int_ico = int(ico.get())
        int_min = int(min.get())
        int_sec = int(sec.get())
        ques_count = tkinter.IntVar()
        cor = tkinter.IntVar()
        ico = tkinter.IntVar()
        min = tkinter.IntVar()
        sec = tkinter.IntVar()
        ques_count.set(int_count)
        cor.set(int_cor)
        ico.set(int_ico)
        min.set(int_min)
        sec.set(int_sec)
        if sub.get() in subject_available:
            no_of_ques = len((question_json[sub.get()])["question"])
            if ques_count.get() <= no_of_ques and ques_count.get() > 0 and cor.get() > 0 and ico.get() <= 0:
                ques_avail = list(range(no_of_ques))
                ques_seq = []
                corr_opt = []
                sel_opt = []
                mark_list = []
                for i in range(0, ques_count.get()):
                    ques_no = random.choice(ques_avail)
                    ques_seq.append(ques_no)
                    corr_opt.append(((question_json[sub.get()])["answer"])[ques_no])
                    ques_avail.remove(ques_no)
                    sel_opt.append(0)
                    mark_list.append(0)
                window.destroy()
                global question_window, response, cur, question_label, option_1, option_2, option_3, option_4, lang_var
                question_window = tkinter.Toplevel()
                def disable_close():
                    pass
                question_window.protocol("WM_DELETE_WINDOW", disable_close)
                question_window.geometry("900x375+350+30")
                question_window.title("Quiz")
                time_text = "0" * (2 - len(str(min.get()))) + str(min.get()) + " : " + "0" * (2 - len(str(sec.get()))) + str(sec.get())
                timer_label = ttk.Label(question_window, text = time_text)
                timer_label.config(font = ("Cambria Math", 15))
                timer_label.place(x = 250, y = 65)
                timer_label.after(1000, lambda : change_time(timer_label, id, sub, cor, ico, corr_opt, sel_opt, question_window))
                submit = ttk.Button(question_window, text = "Submit", command = lambda : confirm_submit_quiz(id, sub, cor, ico, question_window, corr_opt, sel_opt))
                submit.place(x = 450, y = 110)
                question_no_label = ttk.Label(question_window, text = "")
                question_label = ttk.Label(question_window, text = "")
                cur = 0
                speak_image = tkinter.PhotoImage(file = "Speak.png")
                speak_button = ttk.Button(question_window, image = speak_image, command = lambda : threaded_sound(question_label))
                response = tkinter.IntVar()
                option_1 = ttk.Radiobutton(question_window, text = "", variable = response, value = 1)
                option_2 = ttk.Radiobutton(question_window, text = "", variable = response, value = 2)
                option_3 = ttk.Radiobutton(question_window, text = "", variable = response, value = 3)
                option_4 = ttk.Radiobutton(question_window, text = "", variable = response, value = 4)
                question_no_label.place(x = 5, y = 165)
                question_label.place(x = 25, y = 165)
                speak_button.place(x = 40, y = 228)
                option_1.place(x = 100, y = 200)
                option_2.place(x = 100, y = 225)
                option_3.place(x = 100, y = 250)
                option_4.place(x = 100, y = 275)
                next = ttk.Button(question_window, text = "Save and Next", command = lambda : change_ques(True, sub, ques_seq, sel_opt, mark_list, False, cur, cur+1, question_no_label, question_label, option_1, option_2, option_3, option_4, False, lang_var))
                clear_res = ttk.Button(question_window, text = "Clear Response", command = lambda : change_ques(False, sub, ques_seq, sel_opt, mark_list, False, cur, cur, question_no_label, question_label, option_1, option_2, option_3, option_4, True, lang_var))
                mark = ttk.Button(question_window, text = "Mark for Review", command = lambda : change_ques(True, sub, ques_seq, sel_opt, mark_list, True, cur, cur+1, question_no_label, question_label, option_1, option_2, option_3, option_4, False, lang_var))
                clear_res.place(x = 200, y = 330)
                mark.place(x = 350, y = 330)
                next.place(x = 500, y = 330)
                lang_var = tkinter.StringVar()
                lang_var.set("English")
                change_ques(True, sub, ques_seq, sel_opt, mark_list, False, 0, 0, question_no_label, question_label, option_1, option_2, option_3, option_4, False, lang_var)
                question_window.mainloop()
                return
    error = tkinter.Toplevel()
    error.title("Error")
    error_count = -1
    if is_fine(ques_count.get()) == False:
        error_count += 1
        name = ttk.Label(error, text = "Number of questions should be an integer")
        name.place(x = 80, y = error_count*20)
    else:
        if sub.get() in subject_available:
            no_of_ques = len((question_json[sub.get()])["question"])
            if int(ques_count.get()) > no_of_ques:
                error_count += 1
                name = ttk.Label(error, text = "Sorry, we have only " + str(no_of_ques) + " questions for " + sub.get() + ", please enter less")
                name.place(x = 30, y = error_count*20)
        if int(ques_count.get()) < 1:
            error_count += 1
            name = ttk.Label(error, text = "Enter at least one question")
            name.place(x = 130, y = error_count*20)
    if is_fine(cor.get()) == False:
        error_count += 1
        name = ttk.Label(error, text = "Marks for each correct answer should be an integer")
        name.place(x = 60, y = error_count*20)
    else:
        if int(cor.get()) <= 0:
            error_count += 1
            name = ttk.Label(error, text = "Enter greater than 0 for each correct answer")
            name.place(x = 60, y = error_count*20)
    if is_fine(ico.get()) == False:
        error_count += 1
        name = ttk.Label(error, text = "Marks for each incorrect answer should be an integer")
        name.place(x = 55, y = error_count*20)
    else:
        if int(ico.get()) > 0:
            error_count += 1
            name = ttk.Label(error, text = "Enter smaller than or equal to 0 for each incorrect answer")
            name.place(x = 45, y = error_count*20)
    if sub.get() not in subject_available:
        error_count += 1
        name = ttk.Label(error, text = "Invalid subject")
        name.place(x = 150, y = error_count*20)
    if is_fine(min.get()) == False:
        error_count += 1
        name = ttk.Label(error, text = "Minute should be an integer")
        name.place(x = 120, y = error_count*20)
    else:
        if int(min.get()) < 0:
            error_count += 1
            name = ttk.Label(error, text = "Minute can't be negative")
            name.place(x = 125, y = error_count*20)
    if is_fine(sec.get()) == False:
        error_count += 1
        name = ttk.Label(error, text = "Second should be an integer")
        name.place(x = 120, y = error_count*20)
    else:
        if int(sec.get()) < 0:
            error_count += 1
            name = ttk.Label(error, text = "Second can't be negative")
            name.place(x = 125, y = error_count*20)
        if int(sec.get()) > 59:
            error_count += 1
            name = ttk.Label(error, text = "Second can't be greater than 59")
            name.place(x = 110, y = error_count*20)
    ok = ttk.Button(error, text = "OK", command = error.destroy)
    ok.place(x = 155, y = (error_count+1)*20)
    error.geometry("+345+40")

def set_quiz(username):
    quiz_window = tkinter.Toplevel()
    quiz_window.geometry("+350+250")
    quiz_window.title("Customize your Quiz")
    subject_var = tkinter.StringVar()
    subject_label = ttk.Label(quiz_window, text = "Select subject")
    subject = ttk.Combobox(quiz_window, textvariable = subject_var, width = 30)
    subject.config(values = ["Geography", "History", "Chemistry", "Physics", "General Knowledge"])
    no_of_ques_label = ttk.Label(quiz_window, text = "Number of questions")
    no_of_ques_var = tkinter.StringVar()
    no_of_ques_var.set("3")
    no_of_ques = tkinter.Spinbox(quiz_window, from_ = 1, to = len((question_json["Geography"])["question"]), text = no_of_ques_var, width = 31)
    correct_marks_label = ttk.Label(quiz_window, text = "Marks for each correct answer")
    correct_marks_var = tkinter.StringVar()
    correct_marks_var.set("4")
    correct_marks = tkinter.Spinbox(quiz_window, from_ = 1, to = 8, text = correct_marks_var, width = 31)
    incorrect_marks_label = ttk.Label(quiz_window, text = "Marks for each incorrect answer  ")
    incorrect_marks_var = tkinter.StringVar()
    incorrect_marks_var.set("-1")
    incorrect_marks = tkinter.Spinbox(quiz_window, from_ = -4, to = 0, text = incorrect_marks_var, width = 31)
    time_label = ttk.Label(quiz_window, text = "Set time for the quiz")
    min_var = tkinter.StringVar()
    sec_var = tkinter.StringVar()
    min_var.set("1")
    sec_var.set("30")
    min = tkinter.Spinbox(quiz_window, from_ = 0, to = 10, text = min_var, width = 3)
    sec = tkinter.Spinbox(quiz_window, from_ = 0, to = 60, text = sec_var, width = 3)
    min_label = ttk.Label(quiz_window, text = "min")
    sec_label = ttk.Label(quiz_window, text = "sec")
    start_button = ttk.Button(quiz_window, text = "Start Quiz", command = lambda : start_quiz(username, subject_var, no_of_ques_var, correct_marks_var, incorrect_marks_var, min_var, sec_var, quiz_window))
    subject_label.grid(row = 0, column = 0)
    subject.grid(row = 0, column = 1, columnspan = 4)
    no_of_ques_label.grid(row = 1, column = 0)
    no_of_ques.grid(row = 1, column = 1, columnspan = 4)
    correct_marks_label.grid(row = 2, column = 0)
    correct_marks.grid(row = 2, column = 1, columnspan = 4)
    incorrect_marks_label.grid(row = 3, column = 0)
    incorrect_marks.grid(row = 3, column = 1, columnspan = 4)
    time_label.grid(row = 4, column = 0)
    min.grid(row = 4, column = 1)
    min_label.grid(row = 4, column = 2)
    sec.grid(row = 4, column = 3)
    sec_label.grid(row = 4, column = 4)
    start_button.grid(row = 5, column = 1, columnspan = 3)
    quiz_window.mainloop()

def gen_str():
    order = list(range(5))
    captcha_text = ""
    upper_case = string.ascii_uppercase
    digits = string.digits
    for times in range(5):
        to_add_type = random.choice(order)
        order.remove(to_add_type)
        if to_add_type in [1, 3]:
            captcha_text += random.choice(digits)
        else:
            captcha_text += random.choice(upper_case)
    return captcha_text

def gen_cap(captcha_text):
    captcha_win = captcha.image.ImageCaptcha(width = 150, height = 70)
    captcha_image = captcha_win.generate(captcha_text)
    captcha_image_py = ImageTk.PhotoImage(Image.open(captcha_image))
    return captcha_image_py

def save_rate_summary():
    rate_name = ["1 Star", "2 Star", "3 Star", "4 Star", "5 Star"]
    rate_file = open("Rate.txt")
    rate_count = []
    rate_per = []
    for i in range(0, 5):
        rate_count.append(0)
    for account in rate_file:
        try:
            json_rating = json.loads(account)
        except json.decoder.JSONDecodeError:
            break
        rating = int(json_rating["rating"])
        rate_count[rating-1] += 1
    total_rate = sum(rate_count)
    for i in rate_count:
        if total_rate == 0:
            rate_per.append(0)
        else:
            rate_per.append(i*100/total_rate)
    colour_list = ["red", "orange", "yellow", "greenyellow", "lime"]
    matplotlib.pyplot.bar(rate_name, rate_per, color = colour_list)
    matplotlib.pyplot.xlabel("Rating")
    matplotlib.pyplot.ylabel("Percentage")
    matplotlib.pyplot.savefig("Rating Summary.png")
    matplotlib.pyplot.close()
    rate_file.close()

def modify_rating(id, rate, feed):
    rate_file = open("Rate.txt")
    accounts_and_rate = []
    for account in rate_file:
        try:
            json_account = json.loads(account)
        except json.decoder.JSONDecodeError:
            break
        if json_account["user_name"] == id:
            modified = '{"user_name" : ' + '"' + id + '"' + ', "rating" : ' + '"' + str(rate) + '"' + ', "feedback" : ' + '"' + feed + '"}\n'
            accounts_and_rate.append(modified)
        else:
            accounts_and_rate.append(account)
    rate_file.close()
    rate_file = open("Rate.txt", "w")
    rate_file.writelines(accounts_and_rate)
    rate_file.close()
    save_rate_summary()

def add_rating(id, rate, feed):
    rate_file = open("Rate.txt", "r+")
    lines = []
    for account in rate_file:
        try:
            json_account = json.loads(account)
        except json.decoder.JSONDecodeError:
            break
        lines.append(account)
    to_write = '{"user_name" : ' + '"' + id + '"' + ', "rating" : ' + '"' + str(rate) + '"' + ', "feedback" : ' + '"' + feed + '"}\n'
    lines.append(to_write)
    rate_file.seek(0)
    rate_file.writelines(lines)
    rate_file.close()
    save_rate_summary()

def take_feedback(id, rating, feedback, window):
    if rating == 0:
        error = tkinter.Toplevel()
        error.geometry("+415+190")
        error.title("Error")
        message = ttk.Label(error, text = "Please select rating")
        ok = ttk.Button(error, text = "OK", command = error.destroy)
        message.grid(row = 0, column = 0)
        ok.grid(row = 1, column = 0)
        error.mainloop()
    else:
        rate_file = open("Rate.txt")
        present = False
        for account in rate_file:
            try:
                json_account = json.loads(account)
            except json.decoder.JSONDecodeError:
                break
            if json_account["user_name"] == id:
                present = True
        if present:
            modify_rating(id, rating, feedback.get())
        else:
            add_rating(id, rating, feedback.get())
        window.destroy()
        confirm = tkinter.Toplevel()
        confirm.geometry("+365+190")
        confirm.title("Confirmation")
        message = ttk.Label(confirm, text = "Feedback submitted")
        ok = ttk.Button(confirm, text = "OK", command = confirm.destroy)
        message.grid(row = 0, column = 0)
        ok.grid(row = 1, column = 0)
        confirm.mainloop()

def change_view(j):
    global unselected_image, selected_image, cur_rat
    cur_rat = j + 1
    unselected_image = tkinter.PhotoImage(file = "Unselected Star.png")
    selected_image = tkinter.PhotoImage(file = "Selected Star.png")
    for i in range(0, j+1):
        star_button = tkinter.Button(rate_window, image = selected_image, command = lambda j = i : change_view(j))
        star_button.grid(row = 0, column = i+1)
    for i in range(j+1, 5):
        star_button = tkinter.Button(rate_window, image = unselected_image, command = lambda j = i : change_view(j))
        star_button.grid(row = 0, column = i+1)

def rate_command(username):
    global rate_window, cur_rat
    rate_file = open("Rate.txt")
    present = False
    for account in rate_file:
        try:
            json_account = json.loads(account)
        except json.decoder.JSONDecodeError:
            break
        if json_account["user_name"] == username:
            cur_rat = int(json_account["rating"])
            present = True
            break
    if present == False:
        cur_rat = 0
    rate_file.close()
    rate_window = tkinter.Toplevel()
    rate_window.geometry("+350+180")
    rate_window.title("Rate us")
    rating_label = ttk.Label(rate_window, text = "Select Rating  ")
    unselected_image = tkinter.PhotoImage(file = "Unselected Star.png")
    selected_image = tkinter.PhotoImage(file = "Selected Star.png")
    for i in range(0, cur_rat):
        star_button = tkinter.Button(rate_window, image = selected_image, command = lambda j = i : change_view(j))
        star_button.grid(row = 0, column = i+1)
    for i in range(cur_rat, 5):
        star_button = tkinter.Button(rate_window, image = unselected_image, command = lambda j = i : change_view(j))
        star_button.grid(row = 0, column = i+1)
    feedback = ttk.Label(rate_window, text = "Feedback")
    user_feedback = ttk.Entry(rate_window, width = 23)
    submit = ttk.Button(rate_window, text = "Submit", command = lambda : take_feedback(username, cur_rat, user_feedback, rate_window))
    rating_label.grid(row = 0, column = 0)
    feedback.grid(row = 1, column = 0)
    user_feedback.grid(row = 1, column = 1, columnspan = 5)
    submit.grid(row = 2, column = 1, columnspan = 3)
    rate_window.mainloop()

def verify_reset(id, name):
    account_file = open("Account.txt")
    for account in account_file:
        try:
            json_text = json.loads(account)
        except json.decoder.JSONDecodeError:
            break
        if json_text["user_name"] == id:
            if json_text["name"] == name:
                account_file.close()
                return True
    account_file.close()
    return False

def new_pass_submitted(username, password, confirm_password, window):
    if check_password(password.get(), confirm_password.get()) == "True":
        file = open("Account.txt")
        new_list = []
        for account in file:
            try:
                json_account = json.loads(account)
            except json.decoder.JSONDecodeError:
                break
            if json_account["user_name"] == username:
                modified = '{"name" : ' + '"' + json_account["name"] + '"' + ', "user_name" : ' + '"' + username + '"' + ', "gender" : ' + '"' + json_account["gender"] + '", "password" : ' + '"' + encrypt(password.get()) + '"}\n'
                new_list.append(modified)
            else:
                new_list.append(account)
        file.close()
        file = open("Account.txt", "w")
        file.writelines(new_list)
        file.close()
        window.destroy()
        confirmation = tkinter.Toplevel()
        confirmation.geometry("+30+30")
        confirmation.title("Confirmation")
        message = ttk.Label(confirmation, text = "Password successfully changed")
        button = ttk.Button(confirmation, text = "OK", command = confirmation.destroy)
        message.grid(row = 0, column = 0)
        button.grid(row = 1, column = 0)
        confirmation.mainloop()
    else:
        error = tkinter.Toplevel()
        error.geometry("+70+35")
        error.title("Error")
        if check_password(password.get(), confirm_password.get()) == 1:
            password1 = ttk.Label(error, text = "Passwords do not match")
            password1.grid(row = 0, column = 0)
        if check_password(password.get(), confirm_password.get()) == 2:
            password2 = ttk.Label(error, text = "Passwords cannot be empty")
            password2.grid(row = 0, column = 0)
        ok = ttk.Button(error, text = "OK", command = error.destroy)
        ok.grid(row = 1, column = 0)

def reset_submitted(id, name, reset_window):
    if verify_reset(id, name) == True:
        username = id
        reset_window.destroy()
        new_password_window = tkinter.Toplevel()
        new_password_window.geometry("+10+25")
        new_password_window.title("Reset your password")
        global show_confirm_password, show_password
        show_confirm_password = False
        show_password = False
        password_label = ttk.Label(new_password_window, text = "Enter new password ")
        password_entry = ttk.Entry(new_password_window, width = 30)
        password_entry.config(show = "*")
        password_image = tkinter.PhotoImage(file = "Show Password.png")
        password_button = ttk.Button(new_password_window, image = password_image, command = lambda : alter_pass_view(password_entry, password_button))
        confirm_password_label = ttk.Label(new_password_window, text = "Confirm your new password ")
        confirm_password_entry = ttk.Entry(new_password_window, width = 30)
        confirm_password_entry.config(show = "*")
        confirm_password_image = tkinter.PhotoImage(file = "Show Password.png")
        confirm_password_button = ttk.Button(new_password_window, image = confirm_password_image, command = lambda : alter_conf_pass_view(confirm_password_entry, confirm_password_button))
        submit = ttk.Button(new_password_window, text = "Change password", command = lambda : new_pass_submitted(username, password_entry, confirm_password_entry, new_password_window))
        password_label.grid(row = 0, column = 0)
        password_entry.grid(row = 0, column = 1)
        password_button.grid(row = 0, column = 2)
        confirm_password_label.grid(row = 1, column = 0)
        confirm_password_entry.grid(row = 1, column = 1)
        confirm_password_button.grid(row = 1, column = 2)
        submit.grid(row = 2, column = 1)
        new_password_window.mainloop()
    else:
        error = tkinter.Toplevel()
        error.title("Invalid Details")
        error.geometry("+85+40")
        error_message = ttk.Label(error, text = "User name or name don't matches")
        ok = ttk.Button(error, text = "OK", command = error.destroy)
        error_message.grid(row = 0, column = 0)
        ok.grid(row = 1, column = 0)
        error.mainloop()

def reset_password(window):
    window.destroy()
    reset = tkinter.Toplevel()
    reset.geometry("+25+25")
    reset.title("Reset your password")
    id = ttk.Label(reset, text = "User Name")
    user_id = ttk.Entry(reset, width = 30)
    message = ttk.Label(reset, text = "To confirm your identity \n       enter your name")
    user_name = ttk.Entry(reset, width = 30)
    submit = ttk.Button(reset, text = "Submit", command = lambda : reset_submitted(user_id.get(), user_name.get(), reset))
    id.grid(row = 0, column = 0)
    user_id.grid(row = 0, column = 1)
    message.grid(row = 1, column = 0)
    user_name.grid(row = 1, column = 1)
    submit.grid(row = 2, column = 1)
    reset.mainloop()

def verify_log_in(id, password):
    account_file = open("Account.txt")
    for account in account_file:
        try:
            json_text = json.loads(account)
        except json.decoder.JSONDecodeError:
            break
        if json_text["user_name"] == id.get():
            if decrypt(json_text["password"]) == password.get():
                account_file.close()
                return True
    account_file.close()
    return False

def delete_account(id, pre_win, account_window):
    to_open = ["Account.txt", "History.txt", "Rate.txt"]
    for i in to_open:
        file = open(i)
        to_write = []
        lines = file.readlines()
        for account in lines:
            try:
                json_account = json.loads(account)
            except json.decoder.JSONDecodeError:
                break
            if json_account["user_name"] != id:
                to_write.append(account)
        file.close()
        file = open(i, "w")
        file.writelines(to_write)
        file.close()
    save_rate_summary()
    pre_win.destroy()
    account_window.destroy()
    inform = tkinter.Toplevel()
    inform.geometry("+350+300")
    mess = ttk.Label(inform, text = "Account successfully deleted")
    ok = ttk.Button(inform, text = "OK", command = inform.destroy)
    mess.pack()
    ok.pack()
    inform.mainloop()

def ask_conf(id, account_window):
    conf_win = tkinter.Toplevel()
    conf_win.title("Confirmation")
    conf_win.geometry("+350+300")
    message = ttk.Label(conf_win, text = "Are you sure, you want to delete your account")
    yes = ttk.Button(conf_win, text = "Yes", command = lambda : delete_account(id, conf_win, account_window))
    no = ttk.Button(conf_win, text = "No", command = conf_win.destroy)
    message.grid(row = 0, column = 0, columnspan = 2)
    yes.grid(row = 1, column = 0)
    no.grid(row = 1, column = 1)
    conf_win.mainloop()

def log_in_submitted(id, password, window):
    if verify_log_in(id, password):
        active_id = id.get()
        window.destroy()
        account_window = tkinter.Toplevel()
        account_window.geometry("+340+450")
        account_window.title("Welcome")
        account_logo_pic = tkinter.PhotoImage(file = "Account Logo.png")
        account_logo = ttk.Label(account_window, image = account_logo_pic)
        account_label = ttk.Label(account_window, text = active_id)
        start = ttk.Button(account_window, text = "Start quiz", command = lambda : set_quiz(active_id))
        previous = ttk.Button(account_window, text = "Your previous quizzes", command = lambda : show_record(active_id))
        rate = ttk.Button(account_window, text = "Rate us", command = lambda : rate_command(active_id))
        delete = ttk.Button(account_window, text = "Delete Account", command = lambda : ask_conf(active_id, account_window))
        account_logo.grid(row = 0, column = 1)
        account_label.grid(row = 0, column = 2)
        start.grid(row = 1, column = 0)
        previous.grid(row = 2, column = 0)
        rate.grid(row = 3, column = 0)
        delete.grid(row = 4, column = 0)
        account_window.mainloop()
    else:
        error = tkinter.Toplevel()
        error.geometry("+365+200")
        error.title("Error")
        error_message = ttk.Label(error, text = "User name or password don't matches\n       You can reset your password")
        ok = ttk.Button(error, text = "OK", command = error.destroy)
        error_message.grid(row = 0, column = 0)
        ok.grid(row = 1, column = 0)
        error.mainloop()

def log_in_command(to_des, pre_win):
    if to_des == True:
        pre_win.destroy()
    global show_password
    show_password = False
    log_in_window = tkinter.Toplevel()
    log_in_window.geometry("+350+350")
    log_in_window.title("Log in")
    id = ttk.Label(log_in_window, text = "User Name ")
    user_id = ttk.Entry(log_in_window, width = 30)
    password = ttk.Label(log_in_window, text = "Password ")
    user_password = ttk.Entry(log_in_window, width = 30)
    user_password.config(show = "*")
    password_image = tkinter.PhotoImage(file = "Show Password.png")
    password_button = ttk.Button(log_in_window, image = password_image, command = lambda : alter_pass_view(user_password, password_button))
    button = ttk.Button(log_in_window, text = "Log in", command = lambda : log_in_submitted(user_id, user_password, log_in_window))
    forgot_password = ttk.Button(log_in_window, text = "Forgot Password", command = lambda : reset_password(log_in_window))
    id.grid(row = 0, column = 0)
    user_id.grid(row = 0, column = 1)
    password.grid(row = 1, column = 0)
    user_password.grid(row = 1, column = 1)
    password_button.grid(row = 1, column = 2)
    button.grid(row = 2, column = 1)
    forgot_password.grid(row = 3, column = 1)
    log_in_window.mainloop()

def check_name(name):
    if len(name) == 0:
        return False
    return True

def check_user_name(user_name):
    if len(user_name) == 0:
        return 1
    if " " in user_name:
        return 2
    file = open("Account.txt")
    for account in file:
        try:
            json_file = json.loads(account)
        except json.decoder.JSONDecodeError:
            break
        if json_file["user_name"] == user_name:
            return 3
    file.close()
    return "True"

def check_password(pas, con_pas):
    if pas != con_pas:
        return 1
    if pas == con_pas == "":
        return 2
    return "True"

def check_gender(male, female, other):
    try:
        if male[0] == "selected":
            return "male"
    except IndexError:
        try:
            if female[0] == "selected":
                return "female"
        except IndexError:
            try:
                if other[0] == "selected":
                    return "other"
            except IndexError:
                return "none"

def add_account(name, id, password, gender):
    account_file = open("Account.txt", "r+")
    lines = []
    for account in account_file:
        try:
            json_account = json.loads(account)
        except json.decoder.JSONDecodeError:
            break
        lines.append(account)
    to_write = '{"name" : ' + '"' + name + '"' + ', "user_name" : ' + '"' + id + '"' + ', "gender" : ' + '"' + gender + '", "password" : ' + '"' + encrypt(password) + '"}\n'
    lines.append(to_write)
    account_file.seek(0)
    account_file.writelines(lines)
    account_file.close()

def data_submitted(name, user_name, password, conf_pass, pre_win, male, female, other, captcha_text, user_captcha):
    if check_name(name.get()) and check_user_name(user_name.get()) == "True":
        if check_password(password.get(), conf_pass.get()) == "True" and user_captcha.get() == captcha_text:
            if check_gender(male.state(), female.state(), other.state()) != "none":
                add_account(name.get(), user_name.get(), password.get(), check_gender(male.state(), female.state(), other.state()))
                pre_win.destroy()
                created = tkinter.Toplevel()
                created.geometry("+350+200")
                created.title("Confirmation")
                success = ttk.Label(created, text = "Account successfully created, you can now log in")
                log = ttk.Button(created, text = "Log in", command = lambda : log_in_command(True, created))
                success.grid(row = 0, column = 0)
                log.grid(row = 1, column = 0)
                return
    error = tkinter.Toplevel()
    error.title("Error")
    error_count = -1
    if not check_name(name.get()):
        error_count += 1
        name = ttk.Label(error, text = "Name cannot be empty")
        name.grid(row = error_count, column = 0)
    if check_user_name(user_name.get()) == 1:
        error_count += 1
        username1 = ttk.Label(error, text = "Username cannot be empty")
        username1.grid(row = error_count, column = 0)
    if check_user_name(user_name.get()) == 2:
        error_count += 1
        username2 = ttk.Label(error, text = "Username cannot have spaces")
        username2.grid(row = error_count, column = 0)
    if check_user_name(user_name.get()) == 3:
        error_count += 1
        username3 = ttk.Label(error, text = "Username already taken")
        username3.grid(row = error_count, column = 0)
    if check_password(password.get(), conf_pass.get()) == 1:
        error_count += 1
        password1 = ttk.Label(error, text = "Passwords do not match")
        password1.grid(row = error_count, column = 0)
    if check_password(password.get(), conf_pass.get()) == 2:
        error_count += 1
        password2 = ttk.Label(error, text = "Passwords cannot be empty")
        password2.grid(row = error_count, column = 0)
    if check_gender(male.state(), female.state(), other.state()) == "none":
        error_count += 1
        gender = ttk.Label(error, text = "select your gender")
        gender.grid(row = error_count, column = 0)
    if len(user_captcha.get()) == 0:
        error_count += 1
        captcha1 = ttk.Label(error, text = "Captcha code cannot be empty")
        captcha1.grid(row = error_count, column = 0)
    if len(user_captcha.get()) != 0 and user_captcha.get() != captcha_text:
        error_count += 1
        captcha2 = ttk.Label(error, text = "Invalid captcha code")
        captcha2.grid(row = error_count, column = 0)
    ok = ttk.Button(error, text = "OK", command = error.destroy)
    ok.grid(row = error_count+1, column = 0)
    error.geometry("+415+100")

def my_info():
    info_window = tkinter.Toplevel()
    info_window.title("Credit")
    info_window.geometry("+20+10")
    ttk.Label(info_window, text = "SUNNY KUMAR", font = ("Times New Roman", 18)).pack()
    ttk.Label(info_window, text = "B Tech in CSE", font = ("Times New Roman", 16)).pack()
    ttk.Label(info_window, text = "Chandigarh University", font = ("Times New Roman", 14)).pack()
    ttk.Label(info_window, text = "2021-2025", font = ("Times New Roman", 12)).pack()
    info_window.mainloop()

def change_captcha(image, captcha_entry):
    global random_text, new_img
    random_text = gen_str()
    new_img = gen_cap(random_text)
    image.config(image = new_img)
    captcha_entry.delete(0, tkinter.END)

def alter_conf_pass_view(user_confirm_password, confirm_password_image):
    global show_confirm_password, conf_pass_image
    if show_confirm_password == True:
        conf_pass_image = tkinter.PhotoImage(file = "Show Password.png")
        user_confirm_password.config(show = "*")
        show_confirm_password = False
    else:
        conf_pass_image = tkinter.PhotoImage(file = "Hide Password.png")
        user_confirm_password.config(show = "")
        show_confirm_password = True
    confirm_password_image.config(image = conf_pass_image)

def alter_pass_view(user_password,  password_image):
    global show_password, pass_image
    if show_password == True:
        pass_image = tkinter.PhotoImage(file = "Show Password.png")
        user_password.config(show = "*")
        show_password = False
    else:
        pass_image = tkinter.PhotoImage(file = "Hide Password.png")
        user_password.config(show = "")
        show_password = True
    password_image.config(image = pass_image)

def create_account():
    create_window = tkinter.Toplevel()
    create_window.title("Create an account")
    create_window.geometry("+350+10")
    name = ttk.Label(create_window, text = "Name")
    user_name = ttk.Entry(create_window, width = 35)
    id = ttk.Label(create_window, text = "User Name")
    user_id = ttk.Entry(create_window, width = 35)
    gender = ttk.Label(create_window, text = "Select your gender ")
    gender_var = tkinter.StringVar()
    male = ttk.Radiobutton(create_window, text = "Male", variable = gender_var, value = "M")
    female = ttk.Radiobutton(create_window, text = "Female", variable = gender_var, value = "F")
    other = ttk.Radiobutton(create_window, text = "Other", variable = gender_var, value = "O")
    password = ttk.Label(create_window, text = "Password")
    user_password = ttk.Entry(create_window, width = 35)
    global show_confirm_password, show_password, random_text
    show_confirm_password = False
    show_password = False
    user_password.config(show = "*")
    password_image = tkinter.PhotoImage(file = "Show Password.png")
    password_button = ttk.Button(create_window, image = password_image, command = lambda : alter_pass_view(user_password, password_button))
    confirm_password = ttk.Label(create_window, text = "Confirm Password")
    user_confirm_password = ttk.Entry(create_window, width = 35)
    user_confirm_password.config(show = "*")
    confirm_password_image = tkinter.PhotoImage(file = "Show Password.png")
    confirm_password_button = ttk.Button(create_window, image = confirm_password_image, command = lambda : alter_conf_pass_view(user_confirm_password, confirm_password_button))
    random_text = gen_str()
    captcha = gen_cap(random_text)
    captcha_image = ttk.Label(create_window, image = captcha)
    refresh_pic = tkinter.PhotoImage(file = "Refresh.png")
    refresh = ttk.Button(create_window, image = refresh_pic, command = lambda : change_captcha(captcha_image, captcha_text))
    captcha_message = ttk.Label(create_window, text = "  Enter captcha\nKeep CapsLock on ")
    captcha_text = ttk.Entry(create_window, width = 35)
    create = ttk.Button(create_window, text = "Create an account", command = lambda : data_submitted(user_name, user_id, user_password, user_confirm_password, create_window, male, female, other, random_text, captcha_text))
    name.grid(row = 0, column = 0)
    user_name.grid(row = 0, column = 1, columnspan = 2)
    id.grid(row = 1, column = 0)
    user_id.grid(row = 1, column = 1, columnspan = 2)
    gender.grid(row = 2, column = 0)
    male.grid(row = 2, column = 1)
    female.grid(row = 3, column = 1)
    other.grid(row = 4, column = 1)
    password.grid(row = 5, column = 0)
    user_password.grid(row = 5, column = 1, columnspan = 2)
    password_button.grid(row = 5, column = 3)
    confirm_password.grid(row = 6, column = 0)
    user_confirm_password.grid(row = 6, column = 1, columnspan = 2)
    confirm_password_button.grid(row = 6, column = 3)
    captcha_image.grid(row = 7, column = 1)
    refresh.grid(row = 7, column = 2)
    captcha_message.grid(row = 8, column = 0)
    captcha_text.grid(row = 8, column = 1, columnspan = 2)
    create.grid(row = 9, column = 1)
    create_window.mainloop()

window = tkinter.Tk()
audio_no = 0
window.geometry("+20+150")
window.title("Quiz")
pic = tkinter.PhotoImage(file = "Quiz.png")
pic_label = ttk.Label(window, image = pic)
account_create = ttk.Button(window, text = "Create an account", command = create_account)
log_in = ttk.Button(window, text = "Log in", command = lambda : log_in_command(False, window))
credit = ttk.Button(window, text = "Credit", command = my_info)
quit = ttk.Button(window, text = "Quit", command = window.destroy)
pic_label.grid(row = 0, column = 0)
credit.grid(row = 1, column = 0)
account_create.grid(row = 2, column = 0)
log_in.grid(row = 3, column = 0)
quit.grid(row = 4, column = 0)
translator = googletrans.Translator()
window.mainloop()