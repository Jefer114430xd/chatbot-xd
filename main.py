from pyrogram import Client, filters
from pyrogram.types import *
from pymongo import MongoClient
import requests
import os
import re


API_ID = os.environ.get("API_ID", None) 
API_HASH = os.environ.get("API_HASH", None) 
BOT_TOKEN = os.environ.get("BOT_TOKEN", None) 
KUKI_API = os.environ.get("KUKI_API", None) 
MONGO_URL = os.environ.get("MONGO_URL", None)


bot = Client(
    "KukiBot" ,
    api_id = API_ID,
    api_hash = API_HASH ,
    bot_token = BOT_TOKEN
)

async def is_admins(chat_id: int):
    return [
        member.user.id
        async for member in bot.iter_chat_members(
            chat_id, filter="administrators"
        )
    ]


@bot.on_message(
    filters.command("setupchat", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def addchat(_, message): 
    kukidb = MongoClient(MONGO_URL)
    
    kuki = kukidb["KukiDb"]["Kuki"] 
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (
            await is_admins(chat_id)
        ):
            return await message.reply_text(
                "tu no eres administrador"
            )
    is_kuki = kuki.find_one({"chat_id": message.chat.id})
    if not is_kuki:
        kuki.insert_one({"chat_id": message.chat.id})
        await message.reply_text(f"✅ | chatbot activado correctamente @{message.chat.username}\n pedido por [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n© @thekillpro")
    else:
        await message.reply_text(f"ya estaba activado el chatbot anteriormente @{message.chat.username}")


@bot.on_message(
    filters.command("removechat", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def rmchat(_, message): 
    kukidb = MongoClient(MONGO_URL)
    
    kuki = kukidb["KukiDb"]["Kuki"] 
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (
            await is_admins(chat_id)
        ):
            return await message.reply_text(
                "tu no eres administrador"
            )
    is_kuki = kuki.find_one({"chat_id": message.chat.id})
    if not is_kuki:
        await message.reply_text("el chatbot ya estaba desactivado")
    else:
        kuki.delete_one({"chat_id": message.chat.id})
        await message.reply_text("✅ | chatbot desactivado!")


@bot.on_message(
    filters.text
    & filters.reply
    & ~filters.private
    & ~filters.bot
    & ~filters.edited,
    group=2,
)
async def kukiai(client: Client, message: Message):
  msg = message.text
  chat_id = message.chat.id

  kukidb = MongoClient(MONGO_URL)
    
  kuki = kukidb["KukiDb"]["Kuki"] 

  is_kuki = kuki.find_one({"chat_id": message.chat.id})
  if is_kuki:

      Kuki =   requests.get(f"https://kukiapi.xyz/api/apikey={KUKI_API}/message={msg}").json()

      moezilla = f"{Kuki['reply']}"

      self = await bot.get_me()
      bot_id = self.id
      if not message.reply_to_message.from_user.id == bot_id:
          return
      
      await client.send_chat_action(message.chat.id, "typing")
      await message.reply_text(moezilla)


@bot.on_message(
    filters.text
    & ~filters.reply
    & filters.private
    & ~filters.bot
    & ~filters.edited,
    group=2,
)
async def kukiai(client: Client, message: Message):
  msg = message.text
  chat_id = message.chat.id

  Kuki =   requests.get(f"https://kukiapi.xyz/api/apikey={KUKI_API}/message={msg}").json()

  moezilla = f"{Kuki['reply']}"
      
  await client.send_chat_action(message.chat.id, "typing")
  await message.reply_text(moezilla)


@bot.on_message(
    filters.command("chat", prefixes=["/", ".", "?", "-"]))
async def kukiai(client: Client, message: Message):

  msg = message.text.replace(message.text.split(" ")[0], "")
    
  Kuki =   requests.get(f"https://kukiapi.xyz/api/apikey={KUKI_API}/message={msg}").json()

  moezilla = f"{Kuki['reply']}"
      
  await client.send_chat_action(message.chat.id, "typing")
  await message.reply_text(moezilla)





@bot.on_message(filters.command(["start"], prefixes=["/", "!"]))
async def start(client, message):
    self = await bot.get_me()
    busername = self.username
    if message.chat.type != "private":
        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Click aqui",
                url=f"t.me/kukichatbot?start")]])
        await message.reply("escribeme en privado",
                            reply_markup=buttons)
        
    else:
        buttons = [[InlineKeyboardButton("Grupo", url="https://t.me/thekillpro"),
                    InlineKeyboardButton("Creador", url="https://t.me/jefer114430x"),
                    ]]
        Photo = "https://telegra.ph/file/12ef22cb960aabaa91714.jpg"
        await message.reply_photo(Photo, caption=f"ʜᴏʟᴀ 👋 [{message.from_user.first_name}](tg://user?id={message.from_user.id}),  sᴏʏ ᴜɴ ʙᴏᴛ ᴅᴇ ᴀᴅᴍɪɴɪsᴛʀᴀᴄɪᴏɴ ᴄᴏɴ ғᴜɴᴄɪᴏɴᴇs ʙᴀsɪᴄᴀs\n y tambien soy un chatbot\n", reply_markup=InlineKeyboardMarkup(buttons))



@bot.on_message(filters.command(["help"], prefixes=["/", "!"]))
async def help(client, message):
    self = await bot.get_me()
    busername = self.username
    if message.chat.type != "private":
        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Click aqui",
                url=f"t.me/kukichatbot?start=help_")]])
        await message.reply("escribeme en privado",
                            reply_markup=buttons)
        
    else:    
        await message.reply_text("/start - iniciar el bot\n/chat - enviar un mensaje a este bot\n/setupchat - activar chatbot en tu grupo\n/removechat - Desactivar chatbot en tu grupo")






bot.run()

