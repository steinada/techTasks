from http import HTTPStatus
from fastapi import HTTPException

from share_it.app.item.ItemRepository import ItemRepository
from share_it.app.item.ItemDTO import ItemDTO, ItemUpdate, ItemDB
from share_it.app.item.ItemModel import Item
from share_it.app.item.ItemUserModel import Item_User
from share_it.app.item.CommentDTO import CommentDTO, CommentDB
from share_it.app.item.CommentModel import Comment
from share_it.app.user.UserRepository import UserRepository
from share_it.app.core.db import AsyncSessionLocal
from share_it.app.booking.BookingModel import BookingStatus


import datetime

from copy import deepcopy


class ItemService:
    def __init__(self):
        self.item_repository = ItemRepository()
        self.user_repository = UserRepository()

    @staticmethod
    async def construct_item(item_model: Item, user_id: int):
        current_date = datetime.datetime.now()
        item, last_booking, next_booking = ItemDB(**vars(item_model)), None, None
        if item_model.bookings and item_model.item_owner[0].id == user_id:
            last_booking_model = sorted(list(filter(lambda x: all([x.status.name != BookingStatus.REJECTED.name,
                                                                   x.start <= current_date]), item_model.bookings)),
                                        key=lambda x: x.start)
            next_booking_model = sorted(list(filter(lambda x: all([x.status.name != BookingStatus.REJECTED.name,
                                                                   x.start >= current_date]), item_model.bookings)),
                                        key=lambda x: x.start)
            if last_booking_model:
                last_booking = {'id': last_booking_model[-1].id, "bookerId": last_booking_model[-1].booker_id}
            if next_booking_model:
                next_booking = {'id': next_booking_model[0].id, "bookerId": next_booking_model[0].booker_id}
            item.lastBooking = last_booking
            item.nextBooking = next_booking
        if item_model.item_comments:
            comments = list(map(lambda x: CommentDB(**vars(x), authorName=x.author.name), item_model.item_comments))
            item.comments = comments
        return item

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
        items_user = await self.item_repository.get_item_by_id(id=item_id, session=session)
        if not items_user:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "Item not found")
        if items_user.item_owner[0].id != user_id:
            raise HTTPException(HTTPStatus.FORBIDDEN.value, "User has not this item")
        new_params = item.model_dump(exclude_unset=True)
        if "id" in new_params:
            del new_params['id']
        updated_item = await self.item_repository.update_item(id=item_id, session=session, params=new_params)
        return updated_item

    async def search_items(self, session: AsyncSessionLocal, text: str):
        if text:
            items = await self.item_repository.search_items(session=session, text=text)
            return items
        else:
            return []

    async def get_item_with_bookings_by_id(self, item_id: int, session: AsyncSessionLocal, user_id: int):
        item_model = await self.item_repository.get_item_with_bookings_by_id(session=session, item_id=item_id)
        if not item_model:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "Item not found")
        item = await self.construct_item(item_model=item_model, user_id=user_id)
        return item

    async def get_items_with_bookings_by_user(self, session: AsyncSessionLocal, user_id: int):
        items = await self.item_repository.get_items_with_bookings_by_id(session=session, user_id=user_id)
        if not items:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "User not found")
        items_list = list()
        for item_model in items:
            item = await self.construct_item(item_model=item_model, user_id=user_id)
            items_list.append(item)
        return items_list

    async def add_comment_to_item(self, comment: CommentDTO, session: AsyncSessionLocal):
        current_time = datetime.datetime.now()
        item = await self.item_repository.get_item_by_id(session=session, id=comment.item_id)
        if not item:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "Item not found")
        bookers = set(map(lambda x: x.booker_id if x.start <= current_time else '', item.bookings))
        comment_params = comment.dict()
        comment_model = Comment(**comment_params)
        if comment.user_id not in bookers:
            raise HTTPException(HTTPStatus.BAD_REQUEST.value, "User didn't book this item")
        comment_db = await self.item_repository.add_comment(session=session, comment=comment_model)
        author_name = await self.user_repository.get_user_name(session=session, user_id=comment.user_id)
        comment = CommentDB(**vars(comment_db), authorName=author_name)
        return comment
