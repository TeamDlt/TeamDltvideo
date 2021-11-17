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
    [[InlineKeyboardButton("🤘🏻 𝗕𝗮𝗰𝗸", callback_data="cbmenu")]]
)


bcl = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🗑 𝗖𝗹𝗼𝘀𝗲", callback_data="cls")]]
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
        " **𝗥𝗲𝗹𝗼𝗮𝗱𝗲𝗱 !**\n✅ **𝗔𝗱𝗺𝗶𝗻 𝗹𝗶𝘀𝘁** 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 **𝗨𝗽𝗱𝗮𝘁𝗲𝗱 ✌🏻 !**"
    )


@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}", "vskip"]) & other_filters)
@authorized_users_only
async def skip(client, m: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="• 𝗠𝗲𝗻𝘂 🤟🏻", callback_data="cbmenu"
                ),
                InlineKeyboardButton(
                    text="• 𝗖𝗹𝗼𝘀𝗲 🗑", callback_data="cls"
                ),
            ]
        ]
    )

    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("❌ 𝗻𝗼𝘁𝗵𝗶𝗻𝗴 𝗶𝘀 𝗰𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝗽𝗹𝗮𝘆𝗶𝗻𝗴")
        elif op == 1:
            await m.reply("✅ 𝗤𝘂𝗲𝘂𝗲𝘀 is empty.\n\n• 𝘂𝘀𝗲𝗿𝗯𝗼𝘁 𝗹𝗲𝗮𝘃𝗶𝗻𝗴 𝘃𝗼𝗶𝗰𝗲 𝗰𝗵𝗮𝘁")
        else:
            await m.reply_photo(
                photo=f"{IMG_3}",
                caption=f"✅ **𝗦𝗸𝗶𝗽𝗽𝗲𝗱 𝘁𝗼 𝘁𝗵𝗲 𝗻𝗲𝘅𝘁 𝘁𝗿𝗮𝗰𝗸.**\n\n🏷 **𝗡𝗮𝗺𝗲:** [{op[0]}]({op[1]})\n💭 **𝗖𝗵𝗮𝘁:** `{chat_id}`\n💡 **𝗦𝘁𝗮𝘁𝘂𝘀:** `𝗣𝗹𝗮𝘆𝗶𝗻𝗴`\n🎧 **𝗥𝗲𝗾𝘂𝗲𝘀𝘁 𝗯𝘆:** {m.from_user.mention()}",
                reply_markup=keyboard,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "🗑 **𝗿𝗲𝗺𝗼𝘃𝗲𝗱 𝘀𝗼𝗻𝗴 𝗳𝗿𝗼𝗺 𝗾𝘂𝗲𝘂𝗲:**"
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
            await m.reply("✅ **𝘀𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴 𝗵𝗮𝘀 𝗲𝗻𝗱𝗲𝗱 🤟🏻.**")
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝗻𝗼𝘁𝗵𝗶𝗻𝗴 𝗶𝘀 𝘀𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴**")


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
                "🤟🏻 **𝗧𝗿𝗮𝗰𝗸 𝗽𝗮𝘂𝘀𝗲𝗱.**\n\n• **𝗧𝗼 𝗿𝗲𝘀𝘂𝗺𝗲 𝘁𝗵𝗲 𝘀𝘁𝗿𝗲𝗮𝗺, use the**\n» /resume 𝗰𝗼𝗺𝗺𝗮𝗻𝗱."
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝗻𝗼𝘁𝗵𝗶𝗻𝗴 𝗶𝗻 𝘀𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴**")


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
                "▶️ **𝗧𝗿𝗮𝗰𝗸 𝗿𝗲𝘀𝘂𝗺𝗲𝗱.**\n\n• **𝗧𝗼 𝗽𝗮𝘂𝘀𝗲 𝘁𝗵𝗲 𝘀𝘁𝗿𝗲𝗮𝗺, 𝘂𝘀𝗲 𝘁𝗵𝗲**\n» /pause 𝗰𝗼𝗺𝗺𝗮𝗻𝗱."
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝗻𝗼𝘁𝗵𝗶𝗻𝗴 𝗶𝗻 𝘀𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴**")


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
                "🔇 **𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗺𝘂𝘁𝗲𝗱.**\n\n• **𝗧𝗼 𝘂𝗻𝗺𝘂𝘁𝗲 𝘁𝗵𝗲 𝘂𝘀𝗲𝗿𝗯𝗼𝘁, 𝘂𝘀𝗲 𝘁𝗵𝗲**\n» /unmute 𝗰𝗼𝗺𝗺𝗮𝗻𝗱."
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝗻𝗼𝘁𝗵𝗶𝗻𝗴 𝗶𝗻 𝘀𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴**")


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
                "🔊 **𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝘂𝗻𝗺𝘂𝘁𝗲𝗱.**\n\n• **𝗧𝗼 𝗺𝘂𝘁𝗲 𝘁𝗵𝗲 𝘂𝘀𝗲𝗿𝗯𝗼𝘁, 𝘂𝘀𝗲 𝘁𝗵𝗲**\n» /mute 𝗰𝗼𝗺𝗺𝗮𝗻𝗱."
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝗻𝗼𝘁𝗵𝗶𝗻𝗴 𝗶𝗻 𝘀𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴**")


@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 𝗼𝗻𝗹𝘆 𝗮𝗱𝗺𝗶𝗻 𝘄𝗶𝘁𝗵 𝗺𝗮𝗻𝗮𝗴𝗲 𝘃𝗼𝗶𝗰𝗲 𝗰𝗵𝗮𝘁𝘀 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻 𝘁𝗵𝗮𝘁 𝗰𝗮𝗻 𝘁𝗮𝗽 𝘁𝗵𝗶𝘀 𝗯𝘂𝘁𝘁𝗼𝗻 !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await query.edit_message_text(
                "⏸ 𝘀𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴 𝗵𝗮𝘀 𝗽𝗮𝘂𝘀𝗲𝗱", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.edit_message_text("❌ **𝗻𝗼𝘁𝗵𝗶𝗻𝗴 𝗶𝗻 𝘀𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴**", reply_markup=bcl)


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 𝗼𝗻𝗹𝘆 𝗮𝗱𝗺𝗶𝗻 𝘄𝗶𝘁𝗵 𝗺𝗮𝗻𝗮𝗴𝗲 𝘃𝗼𝗶𝗰𝗲 𝗰𝗵𝗮𝘁𝘀 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻 𝘁𝗵𝗮𝘁 𝗰𝗮𝗻 𝘁𝗮𝗽 𝘁𝗵𝗶𝘀 𝗯𝘂𝘁𝘁𝗼𝗻 !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await query.edit_message_text(
                "▶️ 𝘀𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴 𝗵𝗮𝘀 𝗿𝗲𝘀𝘂𝗺𝗲𝗱", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.edit_message_text("❌ **𝗻𝗼𝘁𝗵𝗶𝗻𝗴 𝗶𝗻 𝘀𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴**", reply_markup=bcl)


@Client.on_callback_query(filters.regex("cbstop"))
async def cbstop(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 𝗼𝗻𝗹𝘆 𝗮𝗱𝗺𝗶𝗻 𝘄𝗶𝘁𝗵 𝗺𝗮𝗻𝗮𝗴𝗲 𝘃𝗼𝗶𝗰𝗲 𝗰𝗵𝗮𝘁𝘀 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻 𝘁𝗵𝗮𝘁 𝗰𝗮𝗻 𝘁𝗮𝗽 𝘁𝗵𝗶𝘀 𝗯𝘂𝘁𝘁𝗼𝗻!", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("✅ **𝘀𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴 𝗵𝗮𝘀 𝗲𝗻𝗱𝗲𝗱**", reply_markup=bcl)
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.edit_message_text("❌ **𝗻𝗼𝘁𝗵𝗶𝗻𝗴 𝗶𝗻 𝘀𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴**", reply_markup=bcl)


@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 𝗼𝗻𝗹𝘆 𝗮𝗱𝗺𝗶𝗻 𝘄𝗶𝘁𝗵 𝗺𝗮𝗻𝗮𝗴𝗲 𝘃𝗼𝗶𝗰𝗲 𝗰𝗵𝗮𝘁𝘀 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻 𝘁𝗵𝗮𝘁 𝗰𝗮𝗻 𝘁𝗮𝗽 𝘁𝗵𝗶𝘀 𝗯𝘂𝘁𝘁𝗼𝗻 !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await query.edit_message_text(
                "🔇 𝘂𝘀𝗲𝗿𝗯𝗼𝘁 𝘀𝘂𝗰𝗰𝗲𝘀𝗳𝘂𝗹𝗹𝘆 𝗺𝘂𝘁𝗲𝗱", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.edit_message_text("❌ **𝗻𝗼𝘁𝗵𝗶𝗻𝗴 𝗶𝗻 𝘀𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴**", reply_markup=bcl)


@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 𝗼𝗻𝗹𝘆 𝗮𝗱𝗺𝗶𝗻 𝘄𝗶𝘁𝗵 𝗺𝗮𝗻𝗮𝗴𝗲 𝘃𝗼𝗶𝗰𝗲 𝗰𝗵𝗮𝘁𝘀 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻 𝘁𝗵𝗮𝘁 𝗰𝗮𝗻 𝘁𝗮𝗽 𝘁𝗵𝗶𝘀 𝗯𝘂𝘁𝘁𝗼𝗻 !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await query.edit_message_text(
                "🔊 𝘂𝘀𝗲𝗿𝗯𝗼𝘁 𝘀𝘂𝗰𝗰𝗲𝘀𝗳𝘂𝗹𝗹𝘆 𝘂𝗻𝗺𝘂𝘁𝗲𝗱", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.edit_message_text("❌ **𝗻𝗼𝘁𝗵𝗶𝗻𝗴 𝗶𝗻 𝘀𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴**", reply_markup=bcl)


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
                f"✅ **𝘃𝗼𝗹𝘂𝗺𝗲 𝘀𝗲𝘁 𝘁𝗼** `{range}`%"
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝗻𝗼𝘁𝗵𝗶𝗻𝗴 𝗶𝗻 𝘀𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴**")
