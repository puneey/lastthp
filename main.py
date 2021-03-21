
'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import multiprocessing
import threading
import concurrent

#BOT_OWNER_ROLE = '' # change to what you need
#BOT_OWNER_ROLE_ID = "583573353978265610" 
  
 

 
oot_channel_id_list =[
"459842150323060736","620472229846712371","694093289317597265","695994325938733138","694353173409824813","568617830258442255","693960182803333150","568617830258442255","694137428214022204","709231606430171196"
]

answer_pattern = re.compile(r'(not|n)?([1-3]{1})(\?)?(cnf)?(\?)?$', re.IGNORECASE)

apgscore = 60
nomarkscore = 30
markscore = 15

async def update_scores(content, answer_scores):
    global answer_pattern

    m = answer_pattern.match(content)
    if m is None:
        return False

    ind = int(m[2])-1

    if m[1] is None:
        if m[3] is None:
            if m[4] is None:
                answer_scores[ind] += nomarkscore
            else: # apg
                if m[5] is None:
                    answer_scores[ind] += apgscore
                else:
                    answer_scores[ind] += markscore

        else: # 1? ...
            answer_scores[ind] += markscore

    else: # contains not or n
        if m[3] is None:
            answer_scores[ind] -= nomarkscore
        else:
            answer_scores[ind] -= markscore

    return True

class SelfBot(discord.Client):

    def __init__(self, update_event, answer_scores):
        super().__init__()
        global oot_channel_id_list
        #global wrong
        self.oot_channel_id_list = oot_channel_id_list
        self.update_event = update_event
        self.answer_scores = answer_scores

    async def on_ready(self):
        print("======================")
        print("Nelson Trivia Self Bot")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

    # @bot.event
    # async def on_message(message):
    #    if message.content.startswith('-debug'):
    #         await message.channel.send('d')

        def is_scores_updated(message):
            if message.guild == None or \
                str(message.channel.id) not in self.oot_channel_id_list:
                return False

            content = message.content.replace(' ', '').replace("'", "")
            m = answer_pattern.match(content)
            if m is None:
                return False

            ind = int(m[2])-1

            if m[1] is None:
                if m[3] is None:
                    if m[4] is None:
                        self.answer_scores[ind] += nomarkscore
                    else: # apg
                        if m[5] is None:
                            self.answer_scores[ind] += apgscore
                        else:
                            self.answer_scores[ind] += markscore

                else: # 1? ...
                    self.answer_scores[ind] += markscore

            else: # contains not or n
                if m[3] is None:
                    self.answer_scores[ind] -= nomarkscore
                else:
                    self.answer_scores[ind] -= markscore

            return True

        while True:
            await self.wait_for('message', check=is_scores_updated)
            self.update_event.set()

class Bot(discord.Client):

    def __init__(self, answer_scores):
        super().__init__()
        self.bot_channel_id_list = []
        self.embed_msg = None
        self.embed_channel_id = None
        #global wrong
        self.answer_scores = answer_scores

        
        #await self.bot.add_reaction(embed,':spy:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):
      #  global wrong

         

        one_check = ""

        two_check = ""

        three_check = ""

        four_check= ""

        bold1=""

        bold2=""

        bold3=""

        bold4=""

        line1=""

        line2=""

        line3=""
   
        line4=""

        

        lst_scores = list(self.answer_scores)

        highest = max(lst_scores)

#         lowest = min(lst_scores)

        answer = lst_scores.index(highest)+1

        suggest_answer="🔍🔍"
        
        wrong_answer="🔍🔍"

        if highest >0:

          if answer ==1:

            one_check="☑️"

            suggest_answer="Answer 1️⃣☑️ "
            
            wrong_answer="Answer 3️⃣❎"

          if answer==1:

            bold1=""

          else:

            bold1=""

          if answer ==2:

            two_check="☑️"

            suggest_answer="Answer 2️⃣☑️"
            
            wrong_answer="Answer 1️⃣❎"

          if answer ==2:

            bold2=""

          else:

            bold2=""

          

          if answer ==3:

            three_check="☑️"

            suggest_answer="Answer 3️⃣☑️ "
            
            wrong_answer="Answer 2️⃣❎"

          if answer ==3:

            bold3=""

          else:

            bold3=""

             if answer==4:

               four_check="<a:ii:714506561187217489>"

               suggest_answer="Answer 4⃣:white_check_mark:"

               wrong_answer="Answer 2️⃣<:emoji_14:716227488266846259>"	

            if answer==4:

              bold4=""

            else:

             bold4=""

 #add your games deailts and server name etc. what you need you can change         

			

        self.embed=discord.Embed(title="**HQ TRIVIA**\n Crowd Result....", description=f"Option 1⃣: {lst_scores[0]}{one_check}{bold1}\nOption 2⃣: {lst_scores[1]}{two_check}{bold2}\nOption 3⃣: {lst_scores[2]} {three_check}{bold3}\nOption 4: {lst_scores[1]}{four_check}{bold4}\n**Suggest Answer:-**\n{suggest_answer}\n**Wrong Answer:-**\n{wrong_answer}\n",color=2577281)

        self.embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/720845263111061545/721748526144421949/721352445019684977.gif")

        self.embed.set_footer(text=f"ADITYA#0958",icon_url="https://cdn.discordapp.com/attachments/717881240304484393/718844622985494638/hq_logo.png")
	
        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("Nelson Trivia")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

        await self.clear_results()
        await self.update_embeds()
        #await self.change_presence(activity=discord.Game(name='with '+str(len(set(self.get_all_members())))+' users'))
        await self.change_presence(activity=discord.Activity(type=1,name="HQ Trivia"))

    async def on_message(self, message):

        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "hq":
            #await message.delete()
           # if BOT_OWNER_ROLE in []:
            self.embed_msg = None
            await self.clear_results()
            await self.update_embeds()
            self.embed_msg = \
                await message.channel.send('',embed=self.embed)
            await self.embed_msg.add_reaction("☑️")
            await self.embed_msg.add_reaction("❎")
            self.embed_channel_id = message.channel.id
            #else:
                #await message.channel.send("**Lol** You Not Have permission To Use This **cmd!** :stuck_out_tongue_winking_eye:")
            #return

          

        # process votes
        if message.channel.id == self.embed_channel_id:
            content = message.content.replace(' ', '').replace("'", "")
            updated = await update_scores(content, self.answer_scores)
            if updated:
                await self.update_embeds()

def bot_with_cyclic_update_process(update_event, answer_scores):

    def cyclic_update(bot, update_event):
        f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
        while True:
            update_event.wait()
            update_event.clear()
            f.cancel()
            f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
            #res = f.result()

    bot = Bot(answer_scores)

    upd_thread = threading.Thread(target=cyclic_update, args=(bot, update_event))
    upd_thread.start()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('NzI2Nzc3ODc0NzE1MjQ2NjUy.XviOvA.dtFfmi-RttQvvX4wMHrD-rgSiU0'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('NjExNzg0NTA2ODM5NTMxNTIw.Xt-joA.C8uPIbKH5iVcCpFk3jWXqKQgZck',
                                   bot=False))
    loop.run_forever()

if __name__ == '__main__':

    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=7)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()




 
 
