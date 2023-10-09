from discord.ext import commands
import discord
from discord import option
import datetime
import pytz
from sheet import load_sheet
from others import error_info, load_lunch, load_lunch_data, load_settings, save_lunch
from wallet import add_money, remove_money, set_money, add_all_money, set_all_money, remove_all_money
import time as t

intents = discord.Intents().all()
bot = discord.Bot(command_prefix='l!', intents=intents)

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.select(custom_id="1to18", options=[discord.SelectOption(label=str(i), description=f"{i}號", emoji="⚙️") for i in range(1, 19)], placeholder="選擇座號(1~18)", min_values=1, max_values=1,)
    async def first_select_callback(self, select, interaction):
        await interaction.response.send_message(f"你的座號為{select.values[0]}號")
        
    @discord.ui.select(custom_id="19to36", options=[discord.SelectOption(label=str(i), description=f"{i}號", emoji="⚙️") for i in range(19, 37)], placeholder="選擇座號(19~36)", min_values=1, max_values=1,)
    async def second_select_callback(self, select, interaction):
        await interaction.response.send_message(f"你的座號為{select.values[0]}號")

@bot.event
async def on_ready():
    print(f'機器人已上線({bot.user})')
    bot.add_view(DropdownView())
    
@bot.command(name='讀取表單', description='從Google表單上讀取最新資訊')
async def load(ctx):
    await ctx.defer(invisible=True)
    lunch_data = load_lunch()
    lunch = load_lunch_data()

    current_time = datetime.datetime.now()
    taipei_timezone = pytz.timezone('Asia/Taipei')
    current_time_taipei = current_time.astimezone(taipei_timezone)
    formatted_time = current_time_taipei.strftime("%Y/%m/%d %H:%M:%S")
    try:
        load_sheet_status = load_sheet()
        if type(load_sheet_status) is list:
            for items in load_sheet_status:
                for key, value in items.items():
                    user_id = key
                    time = value['time']
                    lunch_names = value['lunch_names']
                    previous_lunch_names = value['previous_lunch_names']
                    before_money = value['before']
                    after_money = value['now']
                    add_money(int(user_id), int(before_money))
                    remove_money(int(user_id), int(after_money))
                    lunch_data = load_lunch()
                    
                    if previous_lunch_names == ['無', '無', '無', '無', '無'] and lunch_names != ['無', '無', '無', '無', '無']:
                        embed = discord.Embed(title="新增午餐", colour=0x00f56a)
                        if lunch_data['now'][str(user_id)]['discord_id'] != '':
                            member_id = lunch_data['now'][user_id]['discord_id']
                            embed.add_field(name="座號", value=f'<@{member_id}>', inline=False)
                        else:
                            embed.add_field(name="座號", value=f'{user_id}', inline=False)
                        embed.add_field(name="午餐1", value=f"{lunch_names[0]}, {lunch[lunch_names[0]]['price']}", inline=False)
                        embed.add_field(name="午餐2", value=f"{lunch_names[1]}, {lunch[lunch_names[1]]['price']}", inline=False)
                        embed.add_field(name="午餐3", value=f"{lunch_names[2]}, {lunch[lunch_names[2]]['price']}", inline=False)
                        embed.add_field(name="午餐4", value=f"{lunch_names[3]}, {lunch[lunch_names[3]]['price']}", inline=False)
                        embed.add_field(name="午餐5", value=f"{lunch_names[4]}, {lunch[lunch_names[4]]['price']}", inline=False)
                        lunch_price = int(lunch[lunch_names[0]]['price'])+int(lunch[lunch_names[1]]['price'])+int(lunch[lunch_names[2]]['price'])+int(lunch[lunch_names[3]]['price'])+int(lunch[lunch_names[4]]['price'])
                        embed.add_field(name="花費", value=f'{lunch_price}元', inline=False)
                        embed.add_field(name="餘額", value=f'{lunch_data["now"][user_id]["wallet"]}元', inline=False)
                        embed.add_field(name="時間", value=formatted_time, inline=False)
                        channel = bot.get_channel(1147872712832856264)
                        await channel.send(embed=embed)
                        
                    elif lunch_names != previous_lunch_names:
                        embed = discord.Embed(title="更改午餐", colour=0xf59b00)
                        if lunch_data['now'][user_id]['discord_id'] != '':
                            member_id = lunch_data['now'][user_id]['discord_id']
                            embed.add_field(name="座號", value=f'<@{member_id}>', inline=False)
                        else:
                            embed.add_field(name="座號", value=f'{user_id}', inline=False)
                        embed.add_field(name="午餐1", value=f"{lunch_names[0]}, {lunch[lunch_names[0]]['price']}", inline=False)
                        embed.add_field(name="午餐2", value=f"{lunch_names[1]}, {lunch[lunch_names[1]]['price']}", inline=False)
                        embed.add_field(name="午餐3", value=f"{lunch_names[2]}, {lunch[lunch_names[2]]['price']}", inline=False)
                        embed.add_field(name="午餐4", value=f"{lunch_names[3]}, {lunch[lunch_names[3]]['price']}", inline=False)
                        embed.add_field(name="午餐5", value=f"{lunch_names[4]}, {lunch[lunch_names[4]]['price']}", inline=False)
                        lunch_price = int(lunch[lunch_names[0]]['price'])+int(lunch[lunch_names[1]]['price'])+int(lunch[lunch_names[2]]['price'])+int(lunch[lunch_names[3]]['price'])+int(lunch[lunch_names[4]]['price'])
                        embed.add_field(name="花費", value=f'{lunch_price}元', inline=False)
                        embed.add_field(name="餘額", value=f'{lunch_data["now"][user_id]["wallet"]}元', inline=False)
                        embed.add_field(name="時間", value=formatted_time, inline=False)
                        channel = bot.get_channel(1147872712832856264)
                        await channel.send(embed=embed)
                    t.sleep(1)
                    
            await ctx.respond('已完成讀取資料')
        else:
            if not load_sheet_status[6:].startswith('[{'):
                await ctx.respond(f'```發生錯誤:\n{load_sheet_status[6:]}```')
    except Exception as e:
        await ctx.respond(f'```{error_info(e)}```')

@bot.command(name='發送選單', description='這是測試功能')
@commands.is_owner()
async def send_select(ctx: discord.ApplicationContext):
    try:
        # Sending a message containing our View
        await ctx.respond("請選擇你的座號", view=DropdownView())
    except Exception as e:
        error_info(e)
    
@send_select.error
async def send_select_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.respond('```發生錯誤:\n無使用權限```')
        
@bot.command(name='清除所有午餐', description='把所有使用者的午餐清空')
@commands.is_owner()
async def clearalllunch(ctx):
    await ctx.defer(invisible=True)
    lunch_data = load_lunch()
    try:
        for i in range(1, 37):
            lunch_data["now"][str(i)]["lunch_name"] = ["無", "無", "無", "無", "無"]
            lunch_data["previous"][str(i)]["lunch_name"] = ["無", "無", "無", "無", "無"]
        save_lunch(lunch_data)
        await ctx.respond(f'執行成功')
    except Exception as e:
        await ctx.respond(f'```{error_info(e)}```')

@clearalllunch.error
async def clearalllunch_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.respond('```發生錯誤:\n無使用權限```')
        
@bot.command(name='清除指定使用者午餐', description='把指定使用者的午餐清空')
@option("id", description="座號")
@commands.is_owner()
async def clearlunch(ctx, id: int):
    await ctx.defer(invisible=True)
    try:
        lunch_data = load_lunch()
        lunch_data["now"][str(id)]["lunch_name"] = ["無", "無", "無", "無", "無"]
        lunch_data["previous"][str(id)]["lunch_name"] = ["無", "無", "無", "無", "無"]
        save_lunch()
    except Exception as e:
        await ctx.respond(f'```{error_info(e)}```')

@clearlunch.error
async def clearlunch_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.respond('```發生錯誤:\n無使用權限```')
        
@bot.command(name='顯示所有使用者的資訊', description='顯示所有使用者的資訊')
async def load_info(ctx):
    await ctx.defer(invisible=True)
    lunch_data = load_lunch()
    lunch_info = load_lunch_data()
    try:
        embed1 = discord.Embed(title="午餐資訊(1~18號)", colour=0x00b0f4, timestamp=datetime.datetime.now())
        formatted_lunches = []
        for i in range(1, 19):
            for lunch in lunch_data["now"][str(i)]["lunch_name"]:
                price = lunch_info[lunch]["price"]
                formatted_lunch = f'{lunch}, {price}元'
                formatted_lunches.append(formatted_lunch)
            embed1.add_field(name=f"{i}號", value='\n'.join(formatted_lunches), inline=False)
        embed1.set_footer(text="午餐機器人")
        
        embed2 = discord.Embed(title="午餐資訊(19~36號)", colour=0x00b0f4, timestamp=datetime.datetime.now())
        formatted_lunches = []
        for i in range(19, 37):
            for lunch in lunch_data["now"][str(i)]["lunch_name"]:
                price = lunch_info[lunch]["price"]
                formatted_lunch = f'{lunch}, {price}元'
                formatted_lunches.append(formatted_lunch)
            embed2.add_field(name=f"{i}號", value='\n'.join(formatted_lunches), inline=False)
        embed2.set_footer(text="午餐機器人")
        await ctx.respond(embeds=[embed1, embed2])
    except Exception as e:
        await ctx.respond(f'```{error_info(e)}```')
        
@bot.command(name='顯示指定使用者的資訊', description='顯示指定使用者的資訊')
@option("id", description="座號")
async def load_all_info(ctx, id: int):
    await ctx.defer(invisible=True)
    lunch_data = load_lunch()
    lunch_info = load_lunch_data()
    try:
        embed = discord.Embed(title=f"午餐資訊({id}號)", colour=0x00b0f4, timestamp=datetime.datetime.now())
        formatted_lunches = []
        for lunch in lunch_data["now"][str(id)]["lunch_name"]:
            price = lunch_info[lunch]["price"]
            formatted_lunch = f'{lunch}, {price}元'
            formatted_lunches.append(formatted_lunch)
        embed.add_field(name=f"{id}號", value='\n'.join(formatted_lunches), inline=False)
        embed.set_footer(text="午餐機器人")
        await ctx.respond(embed=embed)
    except Exception as e:
        await ctx.respond(f'```{error_info(e)}```')
        
@bot.command(name='統計午餐', description='統計午餐')
@option("week", description="星期", choices=["一", "二", "三", "四", "五"])
async def count_lunch(ctx, week=None):
    await ctx.defer(invisible=True)
    lunch_data = load_lunch()
    try:
        embed = discord.Embed(title="午餐統計", colour=0x00b0f4, timestamp=datetime.datetime.now())
        for id in range(1, 37):
            for lunch in lunch_data["now"][str(id)]["lunch_name"]:
                embed.add_field(name=f"號", value='hi', inline=False)
        embed.set_footer(text="午餐機器人")
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.respond(f'```{error_info(e)}```')
        
@bot.command(name='新增錢', description='新增指定使用者的錢錢')
@option("id", description="座號")
@option("money", description="金額")
@commands.is_owner()
async def addmoney(ctx, id: int, money: int):
    if id is not None and money is not None:
        await ctx.defer(invisible=True)
        try:
            add_money_status = add_money(id, money)
            if str(add_money_status).startswith('error'):
                await ctx.respond(f'```發生錯誤:\n{add_money_status[6:]}```')
            else:
                await ctx.respond(f'已將{id}的錢包新增{money}元')
        except Exception as e:
            await ctx.respond(f'```{error_info(e)}```')

@addmoney.error
async def addmoney_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.respond('```發生錯誤:\n無使用權限```')
        
@bot.command(name='移除錢', description='移除指定使用者的錢錢')
@option("id", description="座號")
@option("money", description="金額")
@commands.is_owner()
async def removemoney(ctx, id: int, money: int):
    if id is not None and money is not None:
        await ctx.defer(invisible=True)
        try:
            remove_money_status = remove_money(id, money)
            if str(remove_money_status).startswith('error'):
                await ctx.respond(f'```發生錯誤:\n{remove_money_status[6:]}```')
            else:
                await ctx.respond(f'已將{id}的錢包移除{money}元')
        except Exception as e:
            error_info(e)

@removemoney.error
async def removemoney_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.respond('```發生錯誤:\n無使用權限```')
        
@bot.command(name='設定錢', description='設定指定使用者的錢錢')
@option("id", description="座號")
@option("money", description="金額")
@commands.is_owner()
async def setmoney(ctx, id: int, money: int):
    if id is not None and money is not None:
        await ctx.defer(invisible=True)
        try:
            set_money_status = set_money(id, money)
            if set_money_status.startswith('error'):
                await ctx.respond(f'```發生錯誤:\n{set_money_status}```')
            else:
                await ctx.respond(f'已將{id}的錢包設為{money}元')
        except Exception as e:
            error_info(e)

@setmoney.error
async def setmoney_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.respond('```發生錯誤:\n無使用權限```')
        
@bot.command(name='新增所有人的錢', description='新增所有使用者的錢錢')
@option("money", description="金額")
@commands.is_owner()
async def addallmoney(ctx, money: int):
    if id is not None and money is not None:
        await ctx.defer(invisible=True)
        try:
            add_all_money_status = add_all_money(money)
            if add_all_money_status is None:
                await ctx.respond(f'已成功把所有人的錢包新增{money}元')
            elif add_all_money_status.startswith('error'):
                await ctx.respond(f'```發生錯誤:\n{add_all_money_status}```')
        except Exception as e:
            await ctx.respond(f'發生了一個錯誤\n{error_info(e)}')

@addallmoney.error
async def addallmoney_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.respond('```發生錯誤:\n無使用權限```')
        
@bot.command(name='移除所有人的錢', description='移除所有使用者的錢錢')
@option("money", description="金額")
@commands.is_owner()
async def removeallmoney(ctx, money: int):
    if id is not None and money is not None:
        await ctx.defer(invisible=True)
        try:
            remove_all_money_status = remove_all_money(money)
            if remove_all_money_status is None:
                await ctx.respond(f'已成功把所有人的錢包設為{money}元')
            elif remove_all_money_status.startswith('error'):
                await ctx.respond(f'```發生錯誤:\n{remove_all_money_status}```')
        except Exception as e:
            await ctx.respond(f'發生了一個錯誤\n{error_info(e)}')

@removeallmoney.error
async def removeallmoney_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.respond('```發生錯誤:\n無使用權限```')
        
@bot.command(name='設定所有人的錢', description='設定所有使用者的錢錢')
@option("money", description="金額")
@commands.is_owner()
async def setallmoney(ctx, money: int):
    if id is not None and money is not None:
        await ctx.defer(invisible=True)
        try:
            set_all_money_status = set_all_money(money)
            if set_all_money_status is None:
                await ctx.respond(f'已成功把所有人的錢包設為{money}元')
            elif set_all_money_status.startswith('error'):
                await ctx.respond(f'```發生錯誤:\n{set_all_money_status}```')
        except Exception as e:
            await ctx.respond(f'發生了一個錯誤\n{error_info(e)}')

@setallmoney.error
async def setallmoney_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.respond('```發生錯誤:\n無使用權限```')
        
@bot.command(name='關於我', description='午餐機器人2.0正式啟動')
async def info(ctx):
    try:
        embed = discord.Embed(title="關於我", colour=0x00b0f4, timestamp=datetime.datetime.now())
        embed.add_field(name=f"我的名字", value='快點點午餐', inline=False)
        embed.add_field(name=f"我的作者", value='<@971730686685880322>', inline=False)
        embed.add_field(name=f"版本", value='2.0', inline=False)
        embed.add_field(name=f"神奇的資訊", value='||這||||個||||資||||訊||||比||||神||||奇||||的||||海||||螺||||還||||神||||奇||||所||||以||||你||||點||||到||||這||||裡||||幹||||嘛||||?||', inline=False)
        embed.add_field(name=f"如何取得免費Nitro(可能已失效)", value='https://www.youtube.com/watch?v=dQw4w9WgXcQ', inline=False)
        embed.set_footer(text="午餐機器人")
        await ctx.respond(embed=embed)
    except Exception as e:
        await ctx.respond(f'```{error_info(e)}```')
        
if __name__ == "__main__":
    settings = load_settings()
    bot.run(settings['bot_token'])