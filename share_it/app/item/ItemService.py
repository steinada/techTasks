from http import HTTPStatus
from fastapi import HTTPException

from share_it.app.item.ItemRepository import ItemRepository
from share_it.app.item.ItemDTO import ItemDTO, ItemUpdate, ItemDB
from share_it.app.item.ItemModel import Item
from share_it.app.item.ItemUserModel import Item_User
from share_it.app.item.CommentDTO import CommentDTO
from share_it.app.item.CommentModel import Comment
from share_it.app.user.UserRepository import UserRepository
from share_it.app.core.db import AsyncSessionLocal

import datetime

from copy import deepcopy


class ItemService:
    def __init__(self):
        self.item_repository = ItemRepository()
        self.user_repository = UserRepository()

    async def create_item(self, item: ItemDTO, user: int, session: AsyncSessionLocal):
        user_exists = await self.user_repository.get_user_by_id(id=user, session=session)
        if not user_exists:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "User not found")
        item_params = item.dict()
        item = Item(**item_params)
        item_db = await self.item_repository.create_item(item=item, session=session)
        item_id = item_db.id
        created_item = deepcopy(item_db)
        item_user = Item_User(item_id=item_id, user_id=user)
        await self.item_repository.create_item_user(item_user=item_user, session=session)
        return created_item

    async def update_item(self, user_id: int, item_id: int, item: ItemUpdate, session: AsyncSessionLocal):
        items_user = await self.item_repository.get_user_by_item(item_id=item_id, session=session)
        if items_user != user_id:
            raise HTTPException(HTTPStatus.FORBIDDEN.value, "User has not this item")
        item_for_update = await self.item_repository.get_item_by_id(id=item_id, session=session)
        if item_for_update:
            new_params = item.model_dump(exclude_unset=True)
            if "id" in new_params:
                del new_params['id']
            updated_item = await self.item_repository.update_item(id=item_id, session=session, params=new_params)
            return updated_item
        else:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "Item not found")

    async def get_item_by_id(self, id: int, session: AsyncSessionLocal):
        item = await self.item_repository.get_item_by_id(session=session, id=id)
        if not item:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "Item not found")
        return item

    async def get_items_of_user(self, user_id: int, session: AsyncSessionLocal):
        user_exists = await self.user_repository.get_user_by_id(id=user_id, session=session)
        if not user_exists:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "User not found")
        items = await self.item_repository.get_items_of_user(session=session, user_id=user_id)
        return items

    async def search_items(self, session: AsyncSessionLocal, text: str):
        if text:
            items = await self.item_repository.search_items(session=session, text=text)
            return items
        else:
            return []

    async def get_item_with_bookings_by_id(self, item_id: int, session: AsyncSessionLocal, user_id: int):
        current_date = datetime.datetime.now()
        item = await self.item_repository.get_item_with_bookings_by_id(session=session, item_id=item_id,
                                                                       current_date=current_date)
        if not item:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "Item not found")
        item_model, last_booking_id, last_booking_booker_id, next_booking_id, next_booking_booker_id, owner_id = item
        item = ItemDB(**vars(item_model))
        if owner_id == user_id and (last_booking_id or next_booking_id):
            item.lastBooking = {'id': last_booking_id, 'bookerId': last_booking_booker_id}
            item.nextBooking = {'id': next_booking_id, 'bookerId': next_booking_booker_id}
        return item

    async def get_items_with_bookings_by_user(self, session: AsyncSessionLocal, user_id: int):
        current_date = datetime.datetime.now()
        user_exists = await self.user_repository.get_user_by_id(id=user_id, session=session)
        if not user_exists:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "User not found")
        items = await self.item_repository.get_items_with_bookings_by_id(session=session, user_id=user_id,
                                                                       current_date=current_date)
        items_list = list()
        for item in items:
            item_model, last_booking_id, last_booking_booker_id, next_booking_id, next_booking_booker_id, owner_id = item
            item = ItemDB(**vars(item_model))
            if last_booking_id or next_booking_id:
                item.lastBooking = {'id': last_booking_id, 'bookerId': last_booking_booker_id}
                item.nextBooking = {'id': next_booking_id, 'bookerId': next_booking_booker_id}
            items_list.append(item)
        return items_list

    async def add_comment_to_item(self, comment: CommentDTO, session: AsyncSessionLocal):
        item = await self.item_repository.get_item_by_id(session=session, id=comment.item_id)
        if not item:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "Item not found")
        bookers = await self.item_repository.get_bookers_of_item(session=session, item_id=comment.item_id)
        comment_params = comment.dict()
        comment_model = Comment(**comment_params)
        if comment.user_id not in bookers:
            raise HTTPException(HTTPStatus.FORBIDDEN.value, "User didn't book this item")
        comment_db = await self.item_repository.add_comment(session=session, comment=comment_model)
        author_name = await self.user_repository.get_comment_author_name(session=session, user_id=comment.user_id)
