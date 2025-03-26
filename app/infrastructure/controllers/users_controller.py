from fastapi import APIRouter, Query

from app.application.query.get_user_by_key_query_handler import (
    GetUserByKeyQuery,
    UserQueryModel,
    getUserByKeyQueryHandler,
)

users_router = APIRouter()


@users_router.get("/users", response_model=UserQueryModel)
async def get_user(
    key: str = Query(..., description="The user key to retrieve user information")
):
    query = GetUserByKeyQuery(key=key)
    return getUserByKeyQueryHandler.execute(query)
