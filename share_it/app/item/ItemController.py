from fastapi import APIRouter, Depends, Header

from typing import Annotated

from share_it.app.item.ItemDTO import ItemDTO, ItemUpdate, ItemDB
from share_it.app.item.ItemService import ItemService
from share_it.app.core.db import AsyncSessionLocal, get_async_session

router = APIRouter(prefix="/items", tags=["Items"])
item_service = ItemService()


@router.get("/search", response_model=list[ItemDB], response_model_exclude_none=True)
async def search_items(text: str, session: AsyncSessionLocal = Depends(get_async_session)):
    items = await item_service.search_items(text=text, session=session)
    return items


@router.post("", response_model=ItemDB, response_model_exclude_none=True)
async def create_item(x_sharer_user_id: Annotated[int | None, Header()],
                      item: ItemDTO, session: AsyncSessionLocal = Depends(get_async_session)):
    item = await item_service.create_item(item=item, session=session, user=x_sharer_user_id)
    return item


@router.patch("/{itemId}", response_model=ItemDB, response_model_exclude_none=True)
async def update_item(x_sharer_user_id: Annotated[int | None, Header()], itemId: int, item: ItemUpdate,
                      session: AsyncSessionLocal = Depends(get_async_session)):
    updated_item = await item_service.update_item(user_id=x_sharer_user_id, item_id=itemId, session=session, item=item)
    return updated_item


@router.get("/{itemId}", response_model=ItemDB, response_model_exclude_none=True)
async def get_item_by_id(itemId, session: AsyncSessionLocal = Depends(get_async_session)):
    item = await item_service.get_item_by_id(id=itemId, session=session)
    return item


@router.get("", response_model=list[ItemDB], response_model_exclude_none=True)
async def get_items_of_user(x_sharer_user_id: Annotated[int | None, Header()],
                            session: AsyncSessionLocal = Depends(get_async_session)):
    items = await item_service.get_items_of_user(session=session, user_id=x_sharer_user_id)
    return items
