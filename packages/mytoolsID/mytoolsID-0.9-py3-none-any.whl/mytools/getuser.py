from pyrogram import enums


class User:
    @staticmethod
    async def get_user_id(message, username):
        entities = message.entities
        app = message._client

        if entities:
            entity_index = 1 if message.text.startswith("/") else 0
            entity = entities[entity_index]

            if entity.type == enums.MessageEntityType.MENTION:
                return (await app.get_chat(username)).id
            elif entity.type == enums.MessageEntityType.TEXT_MENTION:
                return entity.user.id
        return username

    @staticmethod
    async def user_id(message, text):
        if text.isdigit():
            return int(text)
        else:
            return await User.get_user_id(message, text)

    @staticmethod
    async def ger_rid(message, sender_chat=False):
        text = message.text.strip()
        args = text.split()

        if message.reply_to_message:
            reply = message.reply_to_message
            if reply.from_user:
                user_id = reply.from_user.id
            elif sender_chat and reply.sender_chat and reply.sender_chat.id != message.chat.id:
                user_id = reply.sender_chat.id
            else:
                return None, None

            reason = text.split(None, 1)[1] if len(args) > 1 else None
            return user_id, reason

        if len(args) == 2:
            user = args[1]
            return await User.user_id(message, user), None

        if len(args) > 2:
            user, reason = args[1], " ".join(args[2:])
            return await User.user_id(message, user), reason

        return None, None

    @staticmethod
    async def get_admin(message):
        member = await message._client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER)

    @staticmethod
    async def get_id(message):
        return (await User.ger_rid(message))[0]

    @staticmethod
    def mention(user):
        name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        link = f"tg://user?id={user.id}"
        return f"[{name}]({link})"
