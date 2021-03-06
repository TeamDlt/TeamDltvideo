from assets.admins import admins
from helper.syntax import call_py
from pyrogram import Client, filters
from helper.decorators import authorized_users_only
from helper.filters import command, other_filters
from helper.queues import QUEUE, clear_queue
from helper.utils import skip_current_song, skip_item
from config import BOT_USERNAME, GROUP_SUPPORT, IMG_3, UPDATES_CHANNEL
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


bttn = InlineKeyboardMarkup(
    [[InlineKeyboardButton("š¤š» šš®š°šø", callback_data="cbmenu")]]
)


bcl = InlineKeyboardMarkup(
    [[InlineKeyboardButton("š šš¹š¼šš²", callback_data="cls")]]
)


@Client.on_message(command(["reload", f"reload@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        " **š„š²š¹š¼š®š±š²š± !**\nā **šš±šŗš¶š» š¹š¶šš** šµš®š šÆš²š²š» **šØš½š±š®šš²š± āš» !**"
    )


@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}", "vskip"]) & other_filters)
@authorized_users_only
async def skip(client, m: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="ā¢ š š²š»š š¤š»", callback_data="cbmenu"
                ),
                InlineKeyboardButton(
                    text="ā¢ šš¹š¼šš² š", callback_data="cls"
                ),
            ]
        ]
    )

    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("ā š»š¼ššµš¶š»š“ š¶š š°ššæšæš²š»šš¹š š½š¹š®šš¶š»š“")
        elif op == 1:
            await m.reply("ā š¤šš²šš²š is empty.\n\nā¢ ššš²šæšÆš¼š š¹š²š®šš¶š»š“ šš¼š¶š°š² š°šµš®š")
        else:
            await m.reply_photo(
                photo=f"{IMG_3}",
                caption=f"ā **š¦šøš¶š½š½š²š± šš¼ ššµš² š»š²šš ššæš®š°šø.**\n\nš· **š”š®šŗš²:** [{op[0]}]({op[1]})\nš­ **ššµš®š:** `{chat_id}`\nš” **š¦šš®ššš:** `š£š¹š®šš¶š»š“`\nš§ **š„š²š¾šš²šš šÆš:** {m.from_user.mention()}",
                reply_markup=keyboard,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "š **šæš²šŗš¼šš²š± šš¼š»š“ š³šæš¼šŗ š¾šš²šš²:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(
    command(["stopstream", f"stop@{BOT_USERNAME}", "end", f"end@{BOT_USERNAME}", "vstop"])
    & other_filters
)
@authorized_users_only
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("ā **šššæš²š®šŗš¶š»š“ šµš®š š²š»š±š²š± š¤š».**")
        except Exception as e:
            await m.reply(f"š« **error:**\n\n`{e}`")
    else:
        await m.reply("ā **š»š¼ššµš¶š»š“ š¶š šššæš²š®šŗš¶š»š“**")


@Client.on_message(
    command(["pause", f"pause@{BOT_USERNAME}", "vpause"]) & other_filters
)
@authorized_users_only
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                "š¤š» **š§šæš®š°šø š½š®ššš²š±.**\n\nā¢ **š§š¼ šæš²šššŗš² ššµš² šššæš²š®šŗ, use the**\nĀ» /resume š°š¼šŗšŗš®š»š±."
            )
        except Exception as e:
            await m.reply(f"š« **error:**\n\n`{e}`")
    else:
        await m.reply("ā **š»š¼ššµš¶š»š“ š¶š» šššæš²š®šŗš¶š»š“**")


@Client.on_message(
    command(["resume", f"resume@{BOT_USERNAME}", "vresume"]) & other_filters
)
@authorized_users_only
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                "ā¶ļø **š§šæš®š°šø šæš²šššŗš²š±.**\n\nā¢ **š§š¼ š½š®ššš² ššµš² šššæš²š®šŗ, ššš² ššµš²**\nĀ» /pause š°š¼šŗšŗš®š»š±."
            )
        except Exception as e:
            await m.reply(f"š« **error:**\n\n`{e}`")
    else:
        await m.reply("ā **š»š¼ššµš¶š»š“ š¶š» šššæš²š®šŗš¶š»š“**")


@Client.on_message(
    command(["mute", f"mute@{BOT_USERNAME}", "vmute"]) & other_filters
)
@authorized_users_only
async def mute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await m.reply(
                "š **šØšš²šæšÆš¼š šŗššš²š±.**\n\nā¢ **š§š¼ šš»šŗššš² ššµš² ššš²šæšÆš¼š, ššš² ššµš²**\nĀ» /unmute š°š¼šŗšŗš®š»š±."
            )
        except Exception as e:
            await m.reply(f"š« **error:**\n\n`{e}`")
    else:
        await m.reply("ā **š»š¼ššµš¶š»š“ š¶š» šššæš²š®šŗš¶š»š“**")


@Client.on_message(
    command(["unmute", f"unmute@{BOT_USERNAME}", "vunmute"]) & other_filters
)
@authorized_users_only
async def unmute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await m.reply(
                "š **šØšš²šæšÆš¼š šš»šŗššš²š±.**\n\nā¢ **š§š¼ šŗššš² ššµš² ššš²šæšÆš¼š, ššš² ššµš²**\nĀ» /mute š°š¼šŗšŗš®š»š±."
            )
        except Exception as e:
            await m.reply(f"š« **error:**\n\n`{e}`")
    else:
        await m.reply("ā **š»š¼ššµš¶š»š“ š¶š» šššæš²š®šŗš¶š»š“**")


@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("š” š¼š»š¹š š®š±šŗš¶š» šš¶ššµ šŗš®š»š®š“š² šš¼š¶š°š² š°šµš®šš š½š²šæšŗš¶ššš¶š¼š» ššµš®š š°š®š» šš®š½ ššµš¶š šÆšššš¼š» !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await query.edit_message_text(
                "āø šššæš²š®šŗš¶š»š“ šµš®š š½š®ššš²š±", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"š« **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.edit_message_text("ā **š»š¼ššµš¶š»š“ š¶š» šššæš²š®šŗš¶š»š“**", reply_markup=bcl)


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("š” š¼š»š¹š š®š±šŗš¶š» šš¶ššµ šŗš®š»š®š“š² šš¼š¶š°š² š°šµš®šš š½š²šæšŗš¶ššš¶š¼š» ššµš®š š°š®š» šš®š½ ššµš¶š šÆšššš¼š» !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await query.edit_message_text(
                "ā¶ļø šššæš²š®šŗš¶š»š“ šµš®š šæš²šššŗš²š±", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"š« **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.edit_message_text("ā **š»š¼ššµš¶š»š“ š¶š» šššæš²š®šŗš¶š»š“**", reply_markup=bcl)


@Client.on_callback_query(filters.regex("cbstop"))
async def cbstop(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("š” š¼š»š¹š š®š±šŗš¶š» šš¶ššµ šŗš®š»š®š“š² šš¼š¶š°š² š°šµš®šš š½š²šæšŗš¶ššš¶š¼š» ššµš®š š°š®š» šš®š½ ššµš¶š šÆšššš¼š»!", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("ā **šššæš²š®šŗš¶š»š“ šµš®š š²š»š±š²š±**", reply_markup=bcl)
        except Exception as e:
            await query.edit_message_text(f"š« **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.edit_message_text("ā **š»š¼ššµš¶š»š“ š¶š» šššæš²š®šŗš¶š»š“**", reply_markup=bcl)


@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("š” š¼š»š¹š š®š±šŗš¶š» šš¶ššµ šŗš®š»š®š“š² šš¼š¶š°š² š°šµš®šš š½š²šæšŗš¶ššš¶š¼š» ššµš®š š°š®š» šš®š½ ššµš¶š šÆšššš¼š» !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await query.edit_message_text(
                "š ššš²šæšÆš¼š ššš°š°š²šš³šš¹š¹š šŗššš²š±", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"š« **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.edit_message_text("ā **š»š¼ššµš¶š»š“ š¶š» šššæš²š®šŗš¶š»š“**", reply_markup=bcl)


@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("š” š¼š»š¹š š®š±šŗš¶š» šš¶ššµ šŗš®š»š®š“š² šš¼š¶š°š² š°šµš®šš š½š²šæšŗš¶ššš¶š¼š» ššµš®š š°š®š» šš®š½ ššµš¶š šÆšššš¼š» !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await query.edit_message_text(
                "š ššš²šæšÆš¼š ššš°š°š²šš³šš¹š¹š šš»šŗššš²š±", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"š« **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.edit_message_text("ā **š»š¼ššµš¶š»š“ š¶š» šššæš²š®šŗš¶š»š“**", reply_markup=bcl)


@Client.on_message(
    command(["volume", f"volume@{BOT_USERNAME}", "vol"]) & other_filters
)
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(range))
            await m.reply(
                f"ā **šš¼š¹ššŗš² šš²š šš¼** `{range}`%"
            )
        except Exception as e:
            await m.reply(f"š« **error:**\n\n`{e}`")
    else:
        await m.reply("ā **š»š¼ššµš¶š»š“ š¶š» šššæš²š®šŗš¶š»š“**")
