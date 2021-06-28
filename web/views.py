from django.db.models.expressions import OrderBy
from django.shortcuts import render, redirect
import pyautogui
import requests
import time
import json
from .models import bot, click, scroll, write, press, loop, wait, status, drag, control
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from pynput import keyboard
from threading import Timer
import unicodedata

pyautogui.FAILSAFE = False

def index(request):
    #bot.objects.all().delete()
    #click.objects.all().delete()
    #scroll.objects.all().delete()
    #write.objects.all().delete()
    #press.objects.all().delete()
    #loop.objects.all().delete()
    #wait.objects.all().delete()
    return render(request, "web/index.html")

def explore(request):
    delete_empty_bots()
    bots = Paginator(bot.objects.all().order_by('id').reverse(), 24)
    if request.method == "POST":
        if request.POST['page_action'] == 'next':
            page = int(request.POST['page']) + 1
            bots_objects = bots.page(page).object_list
            next = bots.page(page).has_next()
            previous = bots.page(page).has_previous()
            return render(request, "web/explore.html", {"bots": bots_objects, "page": page,
            "next": next, "previous": previous})
        elif request.POST['page_action'] == 'previous':
            page = int(request.POST['page']) - 1
            bots_objects = bots.page(page).object_list
            next = bots.page(page).has_next()
            previous = bots.page(page).has_previous()
            return render(request, "web/explore.html", {"bots": bots_objects, "page": page, 
            "next": next, "previous": previous})
    bots_objects = bots.page(1).object_list
    next = bots.page(1).has_next()
    previous = bots.page(1).has_previous()
    return render(request, "web/explore.html", {"bots": bots_objects, "page": 1,
    "next": next, "previous": previous, "b":bots})

def create(request):
    
    if request.method == "GET":
        new_bot = bot()
        new_bot.save()
        return render(request, "web/create.html", {"bot_id": new_bot.id})

    # include PUT request later
    elif request.method == "POST":
        if request.POST["action"] == "save":
            try:
                image = requests.get(request.POST["image"])
                valid_image = image.status_code == 200
            except:
                valid_image = False

            bot.objects.filter(id=request.POST["bot_id"]).update(title=request.POST["title"], description=request.POST["description"], image=request.POST["image"], valid_image=valid_image, failsafe=request.POST["failsafe"], saved=True)
            return redirect("/explore")
        elif request.POST["action"] == "run":
            run(list_actions(int(request.POST["bot_id"]), True))
            return HttpResponse(status=204)


def appendaction(type, data, actions):
    for i in data:
        acc = (str(type),) + i[:]
        actions.append(acc)
    return actions

def find_contents(loop_contents, s):
    for loop_content in loop_contents:
        try:
            loop_content[s]
            same = True
        except:
            same = False
        if same:
            return loop_content[s]
    
    

def loopactions(actions):
    loop_contents = []
    loops = []
    loops_exist = False
    for action in actions:
        if action[0] == 'loop':
            loops_exist = True
            loops.append(str(action))
            start = int(action[1])
            end = int(action[2])
            this_loop = {}
            contents = []
            for loop_action in actions:
                if (loop_action[0]) == "loop" and loop_action[1] > start and loop_action[1] < end:
                    contents.append(loop_action)
                    start = int(loop_action[2])
                if loop_action[1] > start and loop_action[1] < end:
                    contents.append(loop_action)
            this_loop[str(action)] = contents
            loop_contents.append(this_loop)
    while loops_exist:
        for loop in loops:
            for loop_content in loop_contents:
                try:
                    loop_content[loop]
                    same = True
                except:
                    same = False
                if same:
                    contents = loop_content[loop]
                    inner_loop = False
                    for content in contents:
                        if content[0] == "loop":
                            inner_loop = True
                            to_change = content
                    if not inner_loop:
                        loops.remove(loop)
                    else:
                        contents[contents.index(to_change):contents.index(to_change) + 1] =  find_contents(loop_contents, str(to_change)) * int(to_change[3])
                 
        loops_exist = len(loops) > 0
        
    loops = 1
    while loops:
        loops = 0
        for action in actions:
            if action[0] == "loop":
                loops = 1
                loop = action
                for action_ in actions.copy():
                    if int(action_[1]) > int(loop[1]) and int(action_[1]) < int(loop[2]):
                        actions.remove(action_)
                break
        if loops:
            actions[actions.index(action):actions.index(action) + 1] = find_contents(loop_contents, str(action)) * int(loop[3])
        
    return actions



def run(actions):
    time.sleep(3)
    for action in actions:
        if action[0] == "click":
            pyautogui.click(x=int(action[2]), y=int(action[3]))
        elif action[0] == "scroll":
            pyautogui.scroll(int(action[2]))
        elif action[0] == "write":
            pyautogui.write(str(action[2]))
        elif action[0] == "press":
            pyautogui.press(str(action[2]))
        elif action[0] == "wait":
            time.sleep(int(action[2]) / 1000)
        elif action[0] == "drag":
            if bool(action[7]):
                pyautogui.moveTo(int(action[2]), int(action[3]))
                pyautogui.dragTo(int(action[4]), int(action[5]), (int(action[6]) / 1000), button="left")
            else: 
                pyautogui.moveTo(int(action[2]), int(action[3]))
                pyautogui.moveTo(int(action[4]), int(action[5]), int(action[6]) / 1000)
        elif action[0] == "control":
            if str(action[2]) != "none" and str(action[3]) != "none":
                pyautogui.hotkey('command', str(action[2]), str(action[3]))
            elif str(action[2]) != "none" and str(action[3]) == "none":
                pyautogui.hotkey('command', str(action[2]))
            elif str(action[3] != "none") and str(action[2]) == "none":
                pyautogui.hotkey('command', str(action[3]))
            else:
                pyautogui.hotkey('command')
            
            
        #elif action[0] == "new_action":
        #   'do action'


        if not bool(status.objects.values_list("status",flat=True)[0]):
            return None

    status.objects.all().update(status=False)

    return None


def list_actions(bot_id, loop_action):
    
    actions = []
    loops = loop.objects.filter(bot_id=bot_id).values_list("order_start", "order_end", "iterations")
    actions = appendaction("loop", loops, actions)
    clicks = click.objects.filter(bot_id=bot_id).values_list("order", "x_position", "y_position")
    actions = appendaction("click", clicks, actions)
    scrolls = scroll.objects.filter(bot_id=bot_id).values_list("order", "amount")
    actions = appendaction("scroll", scrolls, actions)
    writes = write.objects.filter(bot_id=bot_id).values_list("order", "string")
    actions = appendaction("write", writes, actions)
    press_s = press.objects.filter(bot_id=bot_id).values_list("order", "button")
    actions = appendaction("press", press_s, actions)
    waits = wait.objects.filter(bot_id=bot_id).values_list("order", "milliseconds")
    actions = appendaction("wait", waits, actions)
    drags = drag.objects.filter(bot_id=bot_id).values_list("order", "startx", "starty", "endx", "endy", "time", "hold")
    actions = appendaction("drag", drags, actions)
    controls = control.objects.filter(bot_id=bot_id).values_list("order", "button", "key")
    actions = appendaction("control", controls, actions)

    #new_actions = new_action.objects.filter(bot_id=bot_id).values_list("order", "info", etc)
    #actions = appendaction("new_action", new_actions, actions)


    actions = sorted(actions, key=lambda x: int(x[1]))
    if loop_action:
        actions = loopactions(actions)
    
    return actions

def include_endloops(actions):
    loop = 0
    for action in actions:
        if action[0] == "loop":
            loop += 1
            actions[actions.index(action)] = action + (loop,)
            for action_ in actions.copy():
                if action_[1] == action[2] - 1:
                    element = action_
                    break
            actions.insert(actions.index(element) + 1, ("endloop", -1, loop))
    return actions


def delete_empty_bots():
    bots = bot.objects.all()
    for bot_ in bots:
        if not bot_.saved:
            bot.objects.get(id=bot_.id).delete()
    return None

@csrf_exempt
def bot_(request, id):
    if request.method == "GET":
        bot_info = bot.objects.get(id=id)
        actions = list_actions(id, False)
        looped_actions = list_actions(id, True)
        actions = include_endloops(actions)
        actions_html = inner_html(actions)
        looped_actions_html = inner_html(looped_actions)
        return render(request, "web/bot.html", {"bot": bot_info, "looped_actions_html": looped_actions_html, "actions_html": actions_html, "bot_id": id})
    elif request.method == "POST":
        run(list_actions(int(request.POST["bot_id"]), True))
        return HttpResponse(status=204)


def inner_html(actions):
    actions_html = "<ul class='list-group' id='list-group'>"
    for action in actions:
        li = "<li class=list-group-item style='border-color: rgba(229,229,229,255); border-style: solid; border-width: 1px; "

        if action[0] == "click":
            li += 'background-color: rgb(253, 211, 211)'
        elif action[0] == "scroll":
            li += 'background-color: rgb(255, 202, 141)'
        elif action[0] == "press":
            li += 'background-color: rgb(141, 255, 147)'
        elif action[0] == "write":
            li += 'background-color: rgb(255, 249, 130)'
        elif action[0] == "loop":
            li += 'background-color: linen'
        elif action[0] == "endloop":
            li += 'background-color: linen'   
        elif action[0] == "wait":
            li += 'background-color: rgb(203, 211, 248)' 
        elif action[0] == "drag":
            li += 'background-color: rgb(236, 179, 235)' 
        elif action[0] == "control":
            li += 'background-color: rgb(172, 255, 214);'

        #elif action[0] == "new_action":
        #   li += 'background-color: rgb()'

        li += "';><strong>"+ str(action[0]) +" </strong> "
        if action[0] == "click":
            li += 'at x: <strong>'+ str(action[2]) +'</strong>, y: <strong>' + str(action[3]) +' </strong>'
        elif action[0] == "scroll":
            li += "for <strong>" + str(action[2]) +"</strong> clicks"
        elif action[0] == "write":
            li += "<span style='font-style: italic;'>" + str(action[2]) +"</span>"
        elif action[0] == "press":
            li += "<strong>" + str(action[2]) +"</strong>"
        elif action[0] == "loop":
            li += "<sup>"  + str(action[4]) + "</sup> for <strong>" + str(action[3]) + "</strong> iterations"
        elif action[0] == "endloop":
            li += "<sup>" + str(action[2]) + "</sup>"   
        elif action[0] == "wait":
            li += "for <strong>" + str(action[2])  + "</strong>"
            if int(action[2]) == 1:
                li += " millisecond"
            else:
                li += " milliseconds"
        elif action[0] == "drag":
            li += 'from x: <strong>'+ str(action[2]) +'</strong>, y: <strong>' + str(action[3]) +' </strong>to x: <strong>'+ str(action[4]) +'</strong>, y: <strong>' + str(action[5]) +' </strong> for <strong>' + str(action[6]) + '</strong> milliseconds '
            if bool(action[7]):
                li += 'and <strong>hold</strong> down mouse.'
            else:
                li += '.'
        elif action[0] == "control":
            li += 'press <strong>command</strong> + <strong>' + str(action[2]) + '</strong> + <strong>' + str(action[3]) + '</strong>'
        #elif action[0] == "new_action":
        #   li += "style of new_action"
        
        li += "</li>"
        actions_html += li
    actions_html += "</ul>"
    return actions_html

@csrf_exempt
def delete(request):
    if request.method == "POST":
        data = json.loads(request.body)
        bot_id = int(data["bot_id"])
        loop.objects.filter(bot_id=bot_id).delete()
        click.objects.filter(bot_id=bot_id).delete()
        scroll.objects.filter(bot_id=bot_id).delete()
        write.objects.filter(bot_id=bot_id).delete()
        press.objects.filter(bot_id=bot_id).delete()
        wait.objects.filter(bot_id=bot_id).delete()
        drag.objects.filter(bot_id=bot_id).delete()
        control.objects.filter(bot_id=bot_id).delete()
        #new_action.objects.filter(bot_id=bot_id).delete()
        return HttpResponse(status=204)

global listener 
global keys 
listener = []
keys = []

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def on_press(key):
    empty()
    if len(listener) - 1:
        listener.pop(0)
    string = ""
    try:
        string = key.char

    except AttributeError:
        
        if str(key) == "Key.backspace":
            string = "delete"
        if str(key) == "Key.space":
            string = "space"
            
    listener[0].stop()
    keys.append(string)

def empty():
    a = []
    for key in keys:
        a.append(key)
    for s in a:
        keys.remove(s)

def listen(request):
    Timer(0.2, end).start()
    with keyboard.Listener(on_press=on_press) as l:
        listener.append(l)
        l.join()
    return JsonResponse([keys[-1]], safe=False)

def end():
    empty()
    if len(listener) - 1:
        listener.pop(0)
    listener[0].stop()
    keys.append("none")

@csrf_exempt
def jsonclick(request):
    clicks = click.objects.all()
    if request.method == "GET":
        return JsonResponse([click_.serialize() for click_ in clicks], safe=False)
    elif request.method == "POST":
        data = json.loads(request.body)

        clic = click(bot_id=int(data["bot_id"]), order=int(data["order"]), x_position=int(data["x_position"]), y_position=int(data["y_position"]))
        clic.save()
        return HttpResponse(status=204)

@csrf_exempt
def jsonscroll(request):
    scrolls = scroll.objects.all()
    if request.method == "GET":
        return JsonResponse([scroll_.serialize() for scroll_ in scrolls], safe=False)
    elif request.method == "POST":
        data = json.loads(request.body)

        scroll__ = scroll(bot_id=int(data["bot_id"]), order=int(data["order"]), amount=int(data["amount"]))
        scroll__.save()
        return HttpResponse(status=204)

@csrf_exempt
def jsonwrite(request):
    writes = write.objects.all()
    if request.method == "GET":
        return JsonResponse([write_.serialize() for write_ in writes], safe=False)
    elif request.method == "POST":
        data = json.loads(request.body)

        write__ = write(bot_id=int(data["bot_id"]), order=int(data["order"]), string=data["string"])
        write__.save()
        return HttpResponse(status=204)

@csrf_exempt
def jsonpress(request):
    presss = press.objects.all()
    if request.method == "GET":
        return JsonResponse([press_.serialize() for press_ in presss], safe=False)
    elif request.method == "POST":
        data = json.loads(request.body)

        press__ = press(bot_id=int(data["bot_id"]), order=int(data["order"]), button=data["button"])
        press__.save()
        return HttpResponse(status=204)

@csrf_exempt
def jsonloop(request):
    loops = loop.objects.all()
    if request.method == "GET":
        return JsonResponse([loop_.serialize() for loop_ in loops], safe=False)
    elif request.method == "POST":
        data = json.loads(request.body)

        loop__ = loop(bot_id=int(data["bot_id"]), order_start=int(data["order_start"]), order_end=int(data["order_end"]), iterations=int(data["iterations"]))
        loop__.save()
        return HttpResponse(status=204)

@csrf_exempt
def jsonwait(request):
    waits = wait.objects.all()
    if request.method == "GET":
        return JsonResponse([wait_.serialize() for wait_ in waits], safe=False)
    elif request.method == "POST":
        data = json.loads(request.body)

        wait__ = wait(bot_id=int(data["bot_id"]), order=int(data["order"]), milliseconds=int(data["milliseconds"]))
        wait__.save()
        return HttpResponse(status=204)

@csrf_exempt
def jsondrag(request):
    drags = drag.objects.all()
    if request.method == "GET":
        return JsonResponse([drag_.serialize() for drag_ in drags], safe=False)
    elif request.method == "POST":
        data = json.loads(request.body)
        drag__ = drag(bot_id=int(data["bot_id"]), order=int(data["order"]), startx=int(data["startx"]), starty=int(data["starty"]), endx=int(data["endx"]), endy=int(data["endy"]), time=int(data["time"]), hold=bool(data["hold"]))
        drag__.save()
        return HttpResponse(status=204)

@csrf_exempt
def jsoncontrol(request):
    controls = control.objects.all()
    if request.method == "GET":
        return JsonResponse([control_.serialize() for control_ in controls], safe=False)
    elif request.method == "POST":
        data = json.loads(request.body)

        control__ = control(bot_id=int(data["bot_id"]), order=int(data["order"]), button=str(data["button"]), key=str(data["key"]))
        control__.save()
        return HttpResponse(status=204)



#@csrf_exempt
#def jsonnew_action(request):
#    new_actions = new_action.objects.all()
#    if request.method == "GET":
#        return JsonResponse([new_action_.serialize() for new_action_ in new_actions], safe=False)
#    elif request.method == "POST":
#        data = json.loads(request.body)

#        new_action__ = new_action(bot_id=int(data["bot_id"]), order=int(data["order"]), "info"=info))
#        wait__.save()
#        return HttpResponse(status=204)

@csrf_exempt
def jsonbot(request):
    bots = bot.objects.all()
    if request.method == "GET":
        return JsonResponse([bot_.serialize() for bot_ in bots], safe=False)

@csrf_exempt
def jsonstatus(request):
    if not len(list(status.objects.all())):
            current = status(status=False)
            current.save() 
    if request.method == "GET":
        current_status = list(status.objects.all())[0]
        return JsonResponse(current_status.serialize())
    elif request.method == "PUT":
        status_ = list(status.objects.all())[0]
        data = json.loads(request.body)
        status_.status = data["status"]
        status_.save()
        return HttpResponse(status=204)


def mousecoords(request):
    return JsonResponse({"x": pyautogui.position()[0], "y": pyautogui.position()[1]})

    
    

        