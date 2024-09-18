from random import randint
import datetime
from invoke import task
import webbrowser
import json
from pathlib import Path

@task()
def pathcheck(c):
    jsons_path = Path('.jsons')
    jsons = ['links.json', 'tasks.json']
    if not jsons_path.is_dir():
        jsons_path.mkdir()
    for x in jsons:
        pathed = jsons_path/x
        if not pathed.is_file():
            pathed.write_text('{}')
    true_dates = jsons_path/'dates.json'
    if not true_dates.is_file():
        true_dates.write_text('{"start": "", "end": ""}')


def read_json(json_name):
    with open(f'.jsons/{json_name}.json', 'r') as file:
        output = json.load(file)
        return output


def write_json(json_name, infile):
    with open(f'.jsons/{json_name}.json', 'w') as outfile:
        json.dump(infile, outfile)

def ora(delay):
    import tkinter as tk
    from PIL import Image, ImageTk
    root = tk.Tk()
    root.title("Image Display")
    fists = []

    # for x in range(1):
    image = Image.open("assets/star_platinum_fist.png")
    image = image.resize((300, 300))  # Adjust size as needed
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=photo)
    root.geometry(f"{image.width}x{image.height}+{randint(0, 2000)}+{randint(0, 2000)}")
    fists.append(label)

    fists[0].pack()
    fists[0].after(delay, root.destroy)
    # time.sleep(2)
    # fists[1].pack()
    # fists[1].after(delay, root.destroy)
    root.mainloop()



@task()
def starplatinum(c):
    # Call the function to show the image
    print("STAR PLATINUM!")
    for x in range(10):
        print('ora')
        ora(20)

@task(pre=[pathcheck])
def stagetime(c):
    date_times = read_json('dates')
    with open('.jsons/tasks.json', 'r') as file:
        tasks = json.load(file)

    start_str = date_times['start']
    end_str = date_times['end']
    try:
        start_time = datetime.datetime.strptime(start_str, "%Y-%m-%d-%H")
        end_time = datetime.datetime.strptime(end_str, "%Y-%m-%d-%H")
    except ValueError:
        print('geen geldige datums ingevuld, probeer het te verranderen met bonnes.changedate')
        return
    now = datetime.datetime.now()


    if now < start_time:
        print("WITCH, YOU'RE A WITCH A DIRTY TIME TRAVELING WITCH!!!!!")
        return
    elif now >= end_time:
        print("You made it though the internship alive, yippee :)")
        return

    total_duration = end_time - start_time
    elapsed_time = now - start_time
    future_time = end_time - now
    time_percentage = (elapsed_time / total_duration) * 100
    progresslists = [[],[]]
    progresslists_length = 100

    for y in range(progresslists_length):
        progresslists[0].append('-')
        progresslists[1].append('-')
    i = (progresslists_length / len(progresslists[0]))

    for x in range(len(progresslists[0])):
        if time_percentage >= i:
            progresslists[0][x] = '#'
            i = i + (progresslists_length / len(progresslists[0]))

    print("Dagen:")
    print(*progresslists[0], f" {time_percentage:.2f}%", sep='')
    print("Nog " + str(future_time.days) + " dagen te gaan!")
    if not tasks:
        print('Je hebt 0 taken klaar staan :)')
        return
    done_tasks = 0
    for x in tasks:
        if tasks[x]['done']:
            done_tasks = done_tasks + 1
    task_percentage = (done_tasks / len(tasks))*100
    j = (progresslists_length / len(progresslists[1]))
    for x in range(len(progresslists[1])):
        if task_percentage >= j:
            progresslists[1][x] = '#'
            j = j + (progresslists_length / len(progresslists[0]))

    print("Taken:")
    print(*progresslists[1], f" {task_percentage:.2f}%", sep='')
    print("Nog " + str(len(tasks)-done_tasks) + " tak(en) te doen!")

@task(pre=[pathcheck])
def changedate(c):
    with open('.jsons/dates.json', 'r') as infile:
        dates = json.load(infile)
    print('Wil je de start of einddatum editen? (start of end)')
    name = input()
    if name not in dates:
        print('DAT IS GEEN start OF end GODVERDOMME')
        return
    print('Ok, geef nu je nieuwe datum aan. (voorbeeld: 2024-09-02-10)')
    time = input()
    dates[name] = time
    with open('.jsons/dates.json', 'w') as outfile:
        json.dump(dates, outfile)
    print(str(name) + ' verranderd, er is geen check of het een ok datum is dus als die nu kapot is is dat jouw schuld :)')

@task(pre=[pathcheck])
def addtask(c):
    old_tasks = read_json('tasks')
    print('Hoe zal het nieuwe taak heten?')
    taskname = input()
    if taskname in old_tasks:
        print('Deze naam bestaat al')
        return
    print('geef een beschrijving van de taak:')
    task_info = input()
    new_task = {taskname: {"info": task_info, "done": False},}
    tasks = old_tasks | new_task
    write_json('tasks', tasks)

@task(pre=[pathcheck])
def showtasks(c):
    tasks = read_json('tasks')
    finished_tasks = []
    unfinished_tasks = []
    print('Aantal taken al gedaan:')
    for x in tasks:
        if tasks[x]['done']:
            finished_tasks.append((str(x) + ': ' + str(tasks[x]['info'])))
        else:
            unfinished_tasks.append((str(x) + ': ' + str(tasks[x]['info'])))
    print(str(len(finished_tasks)) + ' gecomplete taken:')
    for x in finished_tasks:
        print(x)
    print(str(len(unfinished_tasks)) + ' ongecomplete taken:')
    for x in unfinished_tasks:
        print(x)

@task(pre=[pathcheck])
def finishtask(c):
    tasks = read_json('tasks')
    for x in tasks:
        print(x)
    print('Welke task wil je afchecken?')
    taskname = input()
    if taskname not in tasks:
        print(str(taskname) + ' is niet gevonden.')
        return
    tasks[taskname]['done'] = not tasks[taskname]['done']
    write_json('tasks', tasks)
    print(str(taskname) + ' is nu ' + str(tasks[taskname]['done']))

@task(pre=[pathcheck])
def removetask(c):
    tasks = read_json('tasks')
    for x in tasks:
        print(x)
    print('Welke task wil je verwijderen?')
    taskname = input()
    if taskname not in tasks:
        print('Naam niet gevonden :(')
        return
    del tasks[taskname]
    write_json('tasks', tasks)
    print(str(taskname) + " is verwijderd")

@task(pre=[pathcheck])
def yell(c):
    print("AAAAAAAaaaafdffAHHH")

@task(name='open', pre=[pathcheck])
def openlink(c, link):
    list = read_json('links')
    if link == 'all':
        for x in list:
            webbrowser.open(list[x])
            return
    elif link == '--help':
        print(list)
        return
    elif link not in list:
        webbrowser.open('https://www.' + link + '.com/')
        return
    webbrowser.open(list[link])
    return

@task(pre=[pathcheck])
def addlink(c):
    old_links = read_json('links')
    print('Hoe zal de nieuwe link gaan heten?')
    linkname = input()
    if linkname in old_links:
        print('Deze naam bestaat al.')
        return
    print('vul nu de link in waar die je heen moet sturen')
    link = input()
    new_link = {linkname: link,}
    links = old_links | new_link
    write_json('links', links)

@task(pre=[pathcheck])
def deletelink(c):
    links = read_json('links')
    for x in links:
        print(x)
    print('Welke link wil jij verwijderen?')
    linkname = input()
    if linkname not in links:
        print('Naam niet gevonden :(')
        return
    del links[linkname]
    write_json('links', links)
    print(str(linkname) + " is verwijderd")
