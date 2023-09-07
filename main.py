import discord
import random
import os
from datetime import *

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)
plan_message_id = 0
#lists
subjects = []
s_emojis = []


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  print(date.today())


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!plan'):
    # waits for user to input a plan of assignments and sends it to the channel after !end is typed
    await message.channel.send('What is the plan?')
    plan = await client.wait_for('message')
    # one line of plan looks like this: |Subject|Assignment|Starting Date|Ending Date|Points|
    # plan is a list of lines
    plant = plan.content.split('\n')
    #Give every subject a colored Square emoji
    emojis = ['🟥', '🟧', '🟨', '🟩', '🟦', '🟪']
    for i in range(len(plant)):
      #remove the | from plan
      plant[i] = plant[i].split('|')
      #remove the leading and ending spaces from the plan
      plant[i] = [j.strip() for j in plant[i]]
      #add the emoji to the subject every subject gets a different emoji and lines with same subject get same emoji
      if plant[i][1] not in subjects:
        subjects.append(plant[i][1])
        emoj = random.choice(emojis)
        s_emojis.append(emoj)
        emojis.remove(emoj)
        plant[i].insert(0, s_emojis[subjects.index(plant[i][1])])
        plant[i].insert(0, "- ")
      else:
        plant[i].insert(0, s_emojis[subjects.index(plant[i][1])])
        plant[i].insert(0, "- ")
   
    #sort the plan by ending date
    def parse_date(date_str):
      return datetime.strptime(date_str, "%d.%m.%Y").date()

    def get_ending_date(line):
      return parse_date(line[6])

    plant = sorted(plant, key=get_ending_date)

    #generate a string for every line of plan
    for i in range(len(plant)):
      plant[i] = ' '.join(plant[i])
      print(plant[i])

    #send all the lines of plan in one message
    planM = '\n\n'.join(i for i in plant)
    #get mesage id of the plan message
    await message.channel.send(planM)
    #save the message id of the plan message to be able to edit it later (global variable)
    global plan_message_id
    plan_message_id = message.channel.last_message_id
    print(plan_message_id)

  if message.content.startswith('!ID'):
    await message.channel.send(plan_message_id)

  if message.content.startswith('!add'):
    await message.channel.send('What do u wanna add?')
    add = await client.wait_for('message')
    print(add.content)
    #edit the plan message with the new line in the right place
    msg = await message.channel.fetch_message(plan_message_id)
    await msg.edit(content=add.content)
    await message.channel.send('Added')



client.run('TOKEN')
