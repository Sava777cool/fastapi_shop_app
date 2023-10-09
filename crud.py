import asyncio
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User, Profile, Post


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    user: User | None = await session.scalar(stmt)
    print("found user", username, user)
    return user


async def create_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
    bio: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id, first_name=first_name, last_name=last_name, bio=bio
    )
    session.add(profile)
    await session.commit()
    print("profile", profile)
    return profile


async def show_users_with_profile(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.first_name)


async def create_posts(
    session: AsyncSession,
    user_id: int,
    *posts_titles: str,
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    print("posts", posts)
    return posts


async def get_users_with_posts(session: AsyncSession):
    stmt = select(User).options(joinedload(User.posts)).options(User.id)
    users = await session.scalars(stmt)

    for user in users.unique():
        print("**" * 10)
        print(user)
        for post in user.posts:
            print("-", post)


async def main():
    async with db_helper.session_factory() as session:
        await create_user(session=session, username="rob")
        await create_user(session=session, username="jack ")
        user_tom = await get_user_by_username(session=session, username="tom")
        user_jack = await get_user_by_username(session=session, username="jack")
        await get_user_by_username(session=session, username="michel")
        await create_profile(
            session=session,
            user_id=user_tom.id,
            first_name="dan",
            last_name="bond",
        )
        await create_profile(
            session=session,
            user_id=user_jack.id,
            first_name="tom",
            last_name="cruse",
        )
        await show_users_with_profile(session=session)
        await create_posts(
            session,
            user_tom.id,
            "SQLA 3.0",
            "SQLA Having",
        )

        await create_posts(
            session,
            user_jack.id,
            "FastAPI celery",
            "FastAPI asyncio",
        )
        await get_users_with_posts(session=session)


if __name__ == "__main__":
    asyncio.run(main())
