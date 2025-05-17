import asyncio
import json

import httpx
import keyboard
import pyodbc

from src.RedditAccess import RedditAccess
from src.loaders.author_loader import AuthorLoader
from src.loaders.comment_loader import CommentLoader
from src.loaders.flair_loader import FlairLoader
from src.loaders.original_post_loader import OriginalPostLoader
from src.loaders.subreddit_loader import SubredditLoader
from src.transformers.object.author_object_transformer import AuthorObjectObjectTransformer
from src.transformers.object.comment_object_transformer import CommentObjectTransformer
from src.transformers.object.flair_object_transformer import FlairObjectTransformer
from src.transformers.object.original_post_object_transformer import OriginalPostObjectTransformer
from src.transformers.object.subreddit_object_transformer import SubredditObjectTransformer
from src.transformers.staging.author_staging_transformer import AuthorStagingTransformer
from src.transformers.staging.comment_staging_transformer import CommentStagingTransformer
from src.transformers.staging.flair_staging_transformer import FlairStagingTransformer
from src.transformers.staging.original_post_staging_transformer import OriginalPostStagingTransformer
from src.transformers.staging.subreddit_staging_transformer import SubredditStagingTransformer
from dotenv import load_dotenv
import os

load_dotenv()

connection_string = (
    f'DRIVER={{{os.getenv("DRIVER")}}};'
    f'SERVER={os.getenv("SERVER")};'
    f'DATABASE={os.getenv("DATABASE")};'
    f'Trusted_Connection=yes;'
)

async def get_subreddit_data(reddit_access,
                             subreddit_name,
                             subreddit_object_transformer,
                             post_object_transformer,
                             comment_object_transformer):
    subreddit_json = await reddit_access.get_subreddit_data(subreddit_name)
    subreddit = subreddit_object_transformer.transform(subreddit_json)

    post_list_json = await reddit_access.get_post_list(subreddit.name, "year", 10)
    post_list_json = post_list_json.get("data").get("children", [])

    posts = [post_object_transformer.transform(p) for p in post_list_json]
    comment_coroutines = [reddit_access.get_comments(subreddit.name, post.post_id) for post in posts]

    comment_jsons = await asyncio.gather(*comment_coroutines)
    comment_jsons = [json[1] for json in comment_jsons]

    for post, comment_json in zip(posts, comment_jsons):
        comments = comment_object_transformer.transform(comment_json)

        post.comments = comments

    subreddit.posts = posts

    return subreddit

async def main():
    reddit_access = RedditAccess(httpx.AsyncClient())
    await reddit_access.get_token()

    # DB Connection

    db_connection = pyodbc.connect(connection_string)

    print("Connected to the database")

    # Object transformers instantiation

    post_flair_object_transformer = FlairObjectTransformer(field_name="link_flair_text")
    author_flair_object_transformer = FlairObjectTransformer(field_name="author_flair_text")

    author_object_transformer = AuthorObjectObjectTransformer(author_flair_object_transformer)

    post_object_transformer = OriginalPostObjectTransformer(author_object_transformer, post_flair_object_transformer)
    comment_object_transformer = CommentObjectTransformer(author_object_transformer)

    subreddit_object_transformer = SubredditObjectTransformer()

    print("Object transformers instantiated")

    # Staging transformers instantiation

    flair_staging_transformer = FlairStagingTransformer()

    author_staging_transformer = AuthorStagingTransformer()

    original_post_staging_transformer = OriginalPostStagingTransformer()
    comment_staging_transformer = CommentStagingTransformer()

    subreddit_staging_transformer = SubredditStagingTransformer()

    staging_transformers = [
        flair_staging_transformer,
        author_staging_transformer,
        original_post_staging_transformer,
        comment_staging_transformer,
        subreddit_staging_transformer
    ]

    print("Staging transformers instantiated")

    # Loaders instantiation

    flair_loader = FlairLoader(db_connection)

    author_loader = AuthorLoader(db_connection)

    original_post_loader = OriginalPostLoader(db_connection)
    comment_loader = CommentLoader(db_connection)

    subreddit_loader = SubredditLoader(db_connection)

    loaders = [
        flair_loader,
        author_loader,
        original_post_loader,
        comment_loader,
        subreddit_loader
    ]

    print("Loaders instantiated")

    subreddit_names = json.load(open("src/subreddits.json"))


    finish = False

    def finish_program(e):
        if e.name == "esc":
            nonlocal finish
            finish = True

    # ^ not particularly elegant but it works

    for idx, subreddit_name in enumerate(subreddit_names):
        print(f"\n--- Processing subreddit {idx + 1}/{len(subreddit_names)} ---")
        print(f"Fetching {subreddit_name} data...")

        subreddit = await get_subreddit_data(reddit_access,
                                 subreddit_name,
                                 subreddit_object_transformer,
                                 post_object_transformer,
                                 comment_object_transformer)

        print(f"{subreddit_name} data fetched")

        for staging_transformer, loader in zip(staging_transformers, loaders):
            data_tuple = staging_transformer.transform(subreddit)
            loader.load(data_tuple)

        print(f"{subreddit_name} data loaded into the database")

        keyboard.on_press(lambda e: finish_program(e))

        if finish:
            print("Process interrupted by user.")
            break


if __name__ == "__main__":
    asyncio.run(main())