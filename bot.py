import re
import json
import discord
import random

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} funfando e bombando')

die_values = [[2, 6],[2,8],[2,10],[2,12],[3,8],[3,10],[3,12],[4,10],[4,12]]

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('>'):
        prompt = message.content[1:]

        if str.isnumeric(prompt):
            values = level_to_values(int(prompt))
            await message.channel.send(roll(values)[0])
            return
        if set(prompt) == {'a'}:
            await message.channel.send('>[número] - rola um teste do nível selecionado \n>d6 rola um dado do valor selecionado\n>2d6 rola a quantidade de dados do valor selecionado\n>1v1 rola um teste oposto com os níveis selecionados\n>1a1 rola um teste do nível do primeiro número e soma o dano de uma arma do nível do segundo número\n>2a1v2 Rola um teste com o nível do primeiro número e soma o dano de uma arma do nível do segundo número. Então reduz o resultado por um teste do nível do terceiro número')
            return
        if prompt == 'link':
            await message.channel.send('https://docs.google.com/document/d/1y5dMaCNWcjQxG3jFXhZ9HjMTWWUEoP00vSQxFUBcI9s/edit?usp=sharing')
            return
        
        if re.fullmatch(r'\d+d\d+', prompt):
            numbers = re.findall("[0-9]+", prompt)
            numbers = [int(numeric_string) for numeric_string in numbers]
            values = [numbers[1] for i in range(numbers[0])]
            await message.channel.send(roll(values)[0])
            return

        if re.fullmatch(r'd\d+', prompt):
            numbers = re.findall("[0-9]+", prompt)
            numbers = [int(numeric_string) for numeric_string in numbers]
            await message.channel.send(roll([numbers[0]])[0])
            return

        if re.fullmatch(r'\d+a\d+', prompt):
            numbers = re.findall("[0-9]+", prompt)
            numbers = [int(numeric_string) for numeric_string in numbers]
            values = level_to_values(numbers[0]) + attack_to_values(numbers[1])

            await message.channel.send(roll(values)[0])
            return

        if re.fullmatch(r'\d+v\d+', prompt):
            numbers = re.findall('[0-9]+', prompt)
            numbers = [int(numeric_string) for numeric_string in numbers]
            test_a = level_to_values(numbers[0])
            test_b = level_to_values(numbers[1])
            message_a, result_a = roll(test_a)
            message_b, result_b = roll(test_b)
            result = message_a + '\n' + message_b + '\n' + str(result_a) + ' - ' + str(result_b) + ' = ' + str(result_a - result_b)
            await message.channel.send(result)

        if re.fullmatch(r'\d+a\d+v\d+', prompt):
            numbers = re.findall('[0-9]+', prompt)
            numbers = [int(numeric_string) for numeric_string in numbers]
            test_a = level_to_values(numbers[0]) + attack_to_values(numbers[1])
            test_b = level_to_values(numbers[2])
            message_a, result_a = roll(test_a)
            message_b, result_b = roll(test_b)
            result = message_a + '\n' + message_b + '\n' + str(result_a) + ' - ' + str(result_b) + ' = ' + str(result_a - result_b)
            await message.channel.send(result)

def attack_to_values(level):
    value = die_values[level-1][1]
    return [value]

def level_to_values(level):
    if level > len(die_values) or level < 1:
        pass#raise error
    values = [die_values[level-1][1] for i in range(die_values[level-1][0])]
    return values


def roll(values):
    acc = 0
    amts = {}
    values_text = ""
    first_time = True
    for i in values:
        key = str(i)
        if key not in amts.keys():
            amts[key] = 1
        else:
            amts[key] += 1
        
        a = random.randint(1, i)
        if first_time:
            first_time = False
        else:
            values_text += ' + '

        values_text += str(a)
        acc +=a

    die_text = ''
    first_time = True
    for i in amts:
        if first_time:
            first_time = False
        else:
            die_text += ' + '
        die_text += f'{amts[i]}d{i}'
    return_value = die_text + ': ' + values_text + ' = ' + str(acc)

    return return_value, acc

with open('.config.json', 'r') as f:
    data = json.load(f)
    client.run(data['token'])
    
