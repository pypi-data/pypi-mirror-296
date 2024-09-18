from random import randint
import datetime
from invoke import task
import webbrowser
import json
from pathlib import Path

@task()
def pathcheck(c):
    jsons_path = Path('jsons')
    jsons = ['links.json', 'tasks.json']
    if not jsons_path.is_dir():
        jsons_path.mkdir()
    for x in jsons:
        pathed = jsons_path/x
        if not pathed.is_file():
            pathed.write_text('{}')
    true_dates = jsons_path/'dates.json'
    if not true_dates.is_file():
        true_dates.write_text('{"start_time": "", "end_time": ""}')



def ora(delay):
    import tkinter as tk
    from PIL import Image, ImageTk
    # Create the main window
    root = tk.Tk()
    root.title("Image Display")
    fists = []

    # Load and resize the image
    for x in range(3):
        image = Image.open("assets/star_platinum_fist.png")
        image = image.resize((300, 300))  # Adjust size as needed
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(root, image=photo)
        root.geometry(f"{image.width}x{image.height}+{randint(0, 2000)}+{randint(0, 2000)}")
        fists.append(label)

    fists[0].pack()
    fists[0].after(delay, root.destroy)
    # time.sleep(2)
    fists[1].pack()
    fists[1].after(delay, root.destroy)


    # Start the Tkinter event loop
    root.mainloop()
    # Create a label to display the image



@task()
def starplatinum(c):
    # Call the function to show the image
    print("STAR PLATINUM!")
    for x in range(10):
        print('ora')
        ora(20)


@task(pre=[pathcheck])
def stagetime(c):
    with open('jsons/dates.json', 'r') as file:
        date_times = json.load(file)
    with open('jsons/tasks.json', 'r') as file:
        tasks = json.load(file)

    start_str = date_times['start_time']
    end_str = date_times['end_time']
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

    print("Dagen:")
    print(*progresslists[0], f" {time_percentage:.2f}%", sep='')
    print("Nog " + str(future_time.days) + " dagen te gaan!")
    print("Taken:")
    print(*progresslists[1], f" {task_percentage:.2f}%", sep='')
    print("Nog " + str(len(tasks)-done_tasks) + " tak(en) te doen!")

@task(pre=[pathcheck])
def changedate(c, date_name, new_time):
    with open('jsons/dates.json', 'r') as infile:
        dates = json.load(infile)
    if date_name not in dates:
        print('Geef aan of je start_time of end_time wilt verranderen')
        return
    dates[date_name] = new_time
    with open('jsons/dates.json', 'r') as outfile:
        json.dump(dates, outfile)
    print(str(date_name) + ' verranderd, er is geen check of het een ok datum is dus als die nu kapot is is dat jouw schuld :)')

@task(pre=[pathcheck])
def addtask(c, taskname, task_info):
    new_task = {
        taskname: {"info:": task_info, "done": False},
    }
    with open('jsons/tasks.json', 'r') as infile:
        old_tasks = json.load(infile)
    tasks = old_tasks | new_task
    with open('jsons/tasks.json', 'w') as output:
        json.dump(tasks, output)

@task(pre=[pathcheck])
def showtasks(c):
    undfinished_tasks = []
    with open('jsons/tasks.json', 'r') as infile:
        tasks = json.load(infile)
    for x in tasks:
        if not tasks[x]['done']:
            undfinished_tasks.append(str(x) + ': ' + str(tasks[x]['info']))
    print('Aantal taken al gedaan: ' + str(len(tasks) - len(undfinished_tasks)))
    print('Taken nog te doen:')
    for x in undfinished_tasks:
        print(x)

@task(pre=[pathcheck])
def finishtask(c, taskname):
    with open('jsons/tasks.json', 'r') as infile:
        tasks = json.load(infile)

    if taskname not in tasks:
        print(str(taskname) + ' is niet gevonden.')
        return
    tasks[taskname]['done'] = not tasks[taskname]['done']

    with open('jsons/tasks.json', 'w') as outfile:
        json.dump(tasks, outfile)

    print(str(taskname) + ' is nu ' + str(tasks[taskname]['done']))

@task(pre=[pathcheck])
def deletetask(c, taskname):
    with open('jsons/tasks.json', 'r') as infile:
        tasks = json.load(infile)
    if taskname not in tasks:
        print('Naam niet gevonden :(')
        return
    del tasks[taskname]
    with open('jsons/tasks.json', 'w') as outfile:
        json.dump(tasks, outfile)
    print(str(taskname) + " is verwijderd")

@task(pre=[pathcheck])
def yell(c):
    print("AAAAAAAaaaafdffAHHH")

@task(name='open', pre=[pathcheck])
def openlink(c, link):

    with open('jsons/links.json', 'r') as infile:
        list = json.load(infile)

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
def addlink(c, linkname, link):
    new_link = {linkname: link,}
    with open('jsons/links.json', 'r') as infile:
        old_links = json.load(infile)
    links = old_links | new_link
    with open('jsons/links.json', 'w') as output:
        json.dump(links, output)

@task(pre=[pathcheck])
def deletelink(c, linkname):
    with open('jsons/links.json', 'r') as infile:
        links = json.load(infile)
    if linkname not in links:
        print('Naam niet gevonden :(')
        return
    del links[linkname]
    with open('jsons/links.json', 'w') as outfile:
        json.dump(links, outfile)
    print(str(linkname) + " is verwijderd")
