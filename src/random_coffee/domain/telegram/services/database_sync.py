from aiogram import types

from random_coffee.infrastructure.service import BaseService
from random_coffee.domain.telegram import models, repos


class DatabaseSyncService(BaseService):
    """DatabaseSyncService service

    Reflects part of the telegram backend into application database

    Note that this layer helps to clarify repositories usage, that simplifies
    future task of switching repositories backend, as that operations are
    common along application usage, and may be the bottleneck of the system.

    """

    def __init__(
            self,
            all_accounts: repos.AllAccounts,
            all_documents: repos.AllDocuments,
            all_chats: repos.AllChats,
            all_chat_members: repos.AllChatMembers,
            all_photo_sizes: repos.AllPhotoSizes,
            all_files: repos.AllFiles,
    ):
        self.all_accounts = all_accounts
        self.all_documents = all_documents
        self.all_chats = all_chats
        self.all_chat_members = all_chat_members
        self.all_photo_sizes = all_photo_sizes
        self.all_files = all_files

    async def visit_user(
            self,
            obj: types.User
    ) -> models.TelegramAccount:
        telegram_account = await self.all_accounts.with_id(obj.id)

        if telegram_account is None:
            telegram_account = models.TelegramAccount(
                id=obj.id,
            )

        telegram_account.first_name = obj.first_name
        telegram_account.last_name = obj.last_name
        telegram_account.username = obj.username
        telegram_account.is_active = True

        await self.all_accounts.save(telegram_account)
        await self.all_accounts.commit()

        return telegram_account

    async def visit_chat(
            self,
            obj: types.Chat
    ) -> models.Chat:
        telegram_chat = await self.all_chats.with_id(obj.id)

        if telegram_chat is None:
            telegram_chat = models.Chat(
                id=obj.id,
            )

        telegram_chat.type = obj.type
        telegram_chat.title = obj.title
        telegram_chat.username = obj.username

        if obj.invite_link is not None:
            telegram_chat.invitation_link = obj.invite_link

        await self.all_chats.save(telegram_chat)
        await self.all_chats.commit()

        return telegram_chat

    async def get_chat_member(
            self,
            chat: models.Chat,
            account: models.TelegramAccount,
    ) -> models.ChatMember | None:
        telegram_chat_member = await self.all_chat_members.with_chat_and_account(
            telegram_chat_id=chat.id,
            telegram_account_id=account.id,
        )
        return telegram_chat_member

    async def visit_chat_member(
            self,
            chat: types.Chat,
            obj: types.ChatMember,
    ) -> models.ChatMember | None:
        if not hasattr(obj, "user"):
            raise RuntimeError("I can't explain you would not understand, this is not how I am...", obj)
        else:
            user: types.User = obj.user

        is_admin = isinstance(obj, (types.ChatMemberAdministrator, types.ChatMemberOwner))

        telegram_chat_member = await self.all_chat_members.with_chat_and_account(
            telegram_chat_id=chat.id,
            telegram_account_id=user.id,
        )

        if telegram_chat_member is None:
            telegram_chat_member = models.ChatMember(
                telegram_chat_id=chat.id,
                telegram_account_id=user.id,
            )

        telegram_chat_member.is_admin = is_admin

        await self.all_chat_members.save(telegram_chat_member)
        await self.all_chat_members.commit()

        return telegram_chat_member

    async def visit_photo_size(
            self,
            chat: types.Chat,
            obj: types.PhotoSize,
    ):
        robj = models.PhotoSize(
            file_id=obj.file_id,
            file_size=obj.file_size,
            width=obj.width,
            height=obj.height,
            from_chat_id=chat.id,
        )
        await self.all_photo_sizes.save(robj)
        await self.all_photo_sizes.commit()

    async def visit_document(
            self,
            chat: types.Chat,
            obj: types.Document,
    ):
        robj = models.Document(
            file_id=obj.file_id,
            file_size=obj.file_size,
            from_chat_id=chat.id,
        )
        await self.all_documents.save(robj)
        await self.all_documents.commit()

    async def visit_file(
            self,
            from_chat_id: int,
            obj: types.File,
    ):
        robj = models.File(
            id=obj.file_id,
            size=obj.file_size,
            path=obj.file_path,
            from_chat_id=from_chat_id,
        )
        await self.all_files.save(robj)
        await self.all_files.commit()
