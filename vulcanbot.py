from typing import Match
from vulcan import Keystore
from vulcan import Vulcan
from vulcan import Account
import json
from datetime import datetime
from datetime import date
import vulcan
import discord
import calendar
import schedule
import asyncio
import time
from discord.ext import tasks

dcclient = discord.Client()
days = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]
starthr = ["07:10", "08:00", "08:50", "09:35", "10:30", "11:20", "12:20", "13:10", "14:00", "14:50", "15:40", "16:30", "17:20"]
endinghr = ["07:55", "08:45", "09:35", "10:25", "11:15", "12:05", "13:05", "13:55", "14:45", "15:35", "16:25", "17:15", "18:05"]
lessonstoend = ["39", "34", "25", "18", "9"]


@dcclient.event
async def on_ready():
    print('Zalogowano {0.user}'.format(dcclient))
    await dcclient.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Panią E."))

@dcclient.event
async def on_message(message):
    if message.author == dcclient.user:
        return

    if message.content.startswith('$numerek'):
        keystore = Keystore.load(open("keystore.json"))
        account = Account.load(open("account.json"))   
        client = Vulcan(keystore, account)
        await client.select_student() 
        luckynumber = await client.data.get_lucky_number()
        await message.channel.send("Data: " + luckynumber.date.strftime("%d/%m/%Y") + ", Numerek: " + str(luckynumber.number))
        await client.close()

    if message.content.startswith('$lekcje'):
        class testt: 
            def __init__(self, pozycja, przedmiot, imienazwisko): 
                self.pozycja = pozycja 
                self.przedmiot = przedmiot
                self.imienazwisko = imienazwisko
        lekcje = [];
        
        keystore = Keystore.load(open("keystore.json"))
        account = Account.load(open("account.json"))   
        client = Vulcan(keystore, account)
        await client.select_student() 
        lessons = await client.data.get_lessons()
        async for lesson in lessons:
            lekcje.append(testt(lesson.time.position, lesson.subject.name, lesson.teacher.name + " " + lesson.teacher.surname))
        lekcje.sort(key=lambda x: x.pozycja)
        embedVar = discord.Embed(title="Plan lekcji", description=str(date.today()) + ", " + str(days[date.today().weekday()]), color=0x00ff00)
        for lesson in lekcje:
            embedVar.add_field(name=str(lesson.pozycja) + ". " + lesson.przedmiot, value=lesson.imienazwisko, inline=False)
        await message.channel.send(embed=embedVar)
        await client.close()

    if message.content.startswith('$testy'):
        class testt: 
            def __init__(self, przedmiot, temat, deadline): 
                self.przedmiot = przedmiot 
                self.temat = temat
                self.deadline = deadline
        testy = [];
        keystore = Keystore.load(open("keystore.json"))
        account = Account.load(open("account.json"))   
        client = Vulcan(keystore, account)
        await client.select_student() 
        exams = await client.data.get_exams()
        async for exam in exams:
            if exam.deadline.date >= date.today():
                testy.append(testt(str(exam.subject.name), str(exam.topic), str(exam.deadline)))
        embedVar = discord.Embed(title="Sprawdziany", description=str(date.today()) + ", " + str(days[date.today().weekday()]), color=0x00ff00)
        for exam in testy:
            embedVar.add_field(name=exam.przedmiot, value=exam.temat + ", " + str(exam.deadline), inline=False)
        await message.channel.send(embed=embedVar)
        await client.close()   

    if message.content.startswith('$domowe'):
        class testt: 
            def __init__(self, przedmiot, temat, deadline): 
                self.przedmiot = przedmiot 
                self.temat = temat
                self.deadline = deadline
        zadania = [];
        keystore = Keystore.load(open("keystore.json"))
        account = Account.load(open("account.json"))   
        client = Vulcan(keystore, account)
        await client.select_student() 
        zad = await client.data.get_homework()
        async for zad in zad:
            if zad.deadline.date >= date.today():
                zadania.append(testt(str(zad.subject.name), str(zad.content), str(zad.deadline)))
        embedVar = discord.Embed(title="Zadania domowe", description=str(date.today()) + ", " + str(days[date.today().weekday()]), color=0x00ff00)
        for zad in zadania:
            embedVar.add_field(name=zad.przedmiot, value=zad.temat + ", " + str(zad.deadline), inline=False)
        await message.channel.send(embed=embedVar)
        await client.close()    


@tasks.loop(seconds = 1)
async def send():
    lnumber = -1
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time)
    if current_time == "07:00:00":
        lnumber = -2
    elif current_time == "07:10:00":
        lnumber = 0
    elif current_time == "08:00:00":
        lnumber = 1
    elif current_time == "08:50:00":
        lnumber = 2
    elif current_time == "09:35:00":
        lnumber = 3
    elif current_time == "10:30:00":
        lnumber = 4
    elif current_time == "11:20:00":
        lnumber = 5
    elif current_time == "12:20:00":
        lnumber = 6
    elif current_time == "13:10:00":
        lnumber = 7
    elif current_time == "14:00:00":
        lnumber = 8
    elif current_time == "14:50:00":
        lnumber = 9
    elif current_time == "15:40:00":
        lnumber = 10
    elif current_time == "16:30:00":
        lnumber = 11
    elif current_time == "17:20:00":
        lnumber = 12
    if lnumber >= 0:
        keystore = Keystore.load(open("keystore.json"))
        account = Account.load(open("account.json"))   
        client = Vulcan(keystore, account)
        await client.select_student() 
        class testt: 
            def __init__(self, pozycja, przedmiot, imienazwisko): 
                self.pozycja = pozycja 
                self.przedmiot = przedmiot
                self.imienazwisko = imienazwisko
        lessons = await client.data.get_lessons()
        lekcje = [];
        async for lesson in lessons:
            lekcje.append(testt(lesson.time.position, lesson.subject.name, lesson.teacher.name + " " + lesson.teacher.surname))
        lekcje.sort(key=lambda x: x.pozycja)
        if len(lekcje) == 0:
            await client.close()
        else:
            embedVar = discord.Embed(title="Lekcja rozpoczęta", description=str(date.today()) + ", " + str(days[date.today().weekday()]), color=0x00ff00)
            for lesson in lekcje:
                embedVar.add_field(name=lesson.rpartition("||")[0], value=lesson.rpartition("||")[2], inline=False)
            channel = dcclient.get_channel(777899451914125342)
            await channel.send(embed=embedVar)
            await client.close()
    elif lnumber == -2:
        keystore = Keystore.load(open("keystore.json"))
        account = Account.load(open("account.json"))
        client = Vulcan(keystore, account)
        await client.select_student() 
        lessons = await client.data.get_lessons()
        lekcje = [];
        class testt: 
            def __init__(self, pozycja, przedmiot, imienazwisko): 
                self.pozycja = pozycja 
                self.przedmiot = przedmiot
                self.imienazwisko = imienazwisko
        lessons = await client.data.get_lessons()
        async for lesson in lekcje:
            lekcje.append(testt(lesson.time.position, lesson.subject.name, lesson.teacher.name + " " + lesson.teacher.surname))
        lekcje.sort(key=lambda x: x.pozycja)
        embedVar = discord.Embed(title=str(date.today()) + ", " + str(days[date.today().weekday()]), description="Do końca tygodnia pozostało " + lessonstoend[date.today().weekday()] + " lekcji", color=0x00ff00)
        embedVar.add_field(name="Plan lekcji na dziś:", value=starthr[lekcje[0].pozycja] + " - " + endinghr[lekcje[len(lekcje)].pozycja], inline=False)
        for lesson in lekcje:
            embedVar.add_field(name=str(lesson.pozycja) + ". " + lesson.przedmiot, value=lesson.imienazwisko, inline=False)
            channel = dcclient.get_channel(777899451914125342)
        luckynumber = await client.data.get_lucky_number()
        embedVar.add_field(name="‎", value="Szczęśliwy numerek: " + str(luckynumber.number), inline=False)
        testy = [];
        keystore = Keystore.load(open("keystore.json"))
        account = Account.load(open("account.json"))   
        client = Vulcan(keystore, account)
        await client.select_student() 
        exams = await client.data.get_exams()
        async for exam in exams:
            if exam.deadline.date == date.today():
                testy.append(testt(str(exam.subject.name), str(exam.topic), str(exam.deadline)))
        if len(testy) == 0:
            embedVar.add_field(name="‎", value="Dzisiejsze testy: brak", inline=False)
        else:
            embedVar.add_field(name="‎", value="Dzisiejsze testy: " + str(len(testy)), inline=False)
        for exam in testy:
            embedVar.add_field(name=exam.przedmiot, value=exam.temat + ", " + str(exam.deadline), inline=False)

        class testt: 
            def __init__(self, przedmiot, temat, deadline): 
                self.przedmiot = przedmiot 
                self.temat = temat
                self.deadline = deadline
        zadania = [];
        keystore = Keystore.load(open("keystore.json"))
        account = Account.load(open("account.json"))   
        client = Vulcan(keystore, account)
        await client.select_student() 
        zad = await client.data.get_homework()
        async for zad in zad:
            if zad.deadline.date >= date.today():
                zadania.append(testt(str(zad.subject.name), str(zad.content), str(zad.deadline)))
        if len(zadania) == 0:
            embedVar.add_field(name="‎", value="Dzisiejsze zadania: brak", inline=False)
        else:
            embedVar.add_field(name="‎", value="Dzisiejsze zadania: " + str(len(zadania)), inline=False)
        for zad in zadania:
            embedVar.add_field(name=zad.przedmiot, value=zad.temat + ", " + str(zad.deadline), inline=False)

        await channel.send(embed=embedVar)
        await client.close()


@send.before_loop
async def before():
    await dcclient.wait_until_ready()

send.start()

dcclient.run()







