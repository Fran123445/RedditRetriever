-- DB Creation

CREATE DATABASE RedditRetriever
GO

USE RedditRetriever
GO

CREATE TABLE Subreddit(
	id INTEGER PRIMARY KEY IDENTITY(1,1),
	internal_reddit_id NVARCHAR(16) UNIQUE NOT NULL,
	name NVARCHAR(512) NOT NULL,
	subscribers INTEGER NOT NULL,
	nsfw BIT NOT NULL
)

CREATE TABLE Flair(
	id BIGINT IDENTITY(1,1),
	subreddit_id INTEGER,
	text NVARCHAR(512)
	PRIMARY KEY (id, subreddit_id)
	FOREIGN KEY (subreddit_id) REFERENCES subreddit(id)
)

CREATE TABLE [User](
	id BIGINT PRIMARY KEY IDENTITY(1,1),
	internal_reddit_id NVARCHAR(16) UNIQUE NOT NULL,
	username NVARCHAR(512) NOT NULL
)

CREATE TABLE Author(
	id BIGINT,
	subreddit_id INTEGER,
	flair_id BIGINT,
	PRIMARY KEY (id, subreddit_id),
	FOREIGN KEY (id) REFERENCES [User](id),
	FOREIGN KEY (subreddit_id) REFERENCES Subreddit(id),
	FOREIGN KEY (flair_id, subreddit_id) REFERENCES Flair(id, subreddit_id)
)

CREATE TABLE Post(
	id BIGINT PRIMARY KEY IDENTITY(1,1),
	internal_reddit_id NVARCHAR(16) UNIQUE NOT NULL,
	subreddit_id INTEGER NOT NULL,
	author_id BIGINT NOT NULL,
	flair_id BIGINT,
	title NVARCHAR(MAX) NOT NULL,
	body NVARCHAR(MAX),
	edited_date DATETIME, -- if this one's null, then the post was never edited
	upvotes INTEGER NOT NULL,
	downvotes INTEGER NOT NULL,
	nsfw BIT NOT NULL,
	spoiler BIT NOT NULL,
	creation_date DATETIME NOT NULL,
	FOREIGN KEY (subreddit_id) REFERENCES Subreddit(id),
	FOREIGN KEY (author_id, subreddit_id) REFERENCES Author(id, subreddit_id),
	FOREIGN KEY (flair_id, subreddit_id) REFERENCES Flair(id, subreddit_id)
)

CREATE TABLE Comment(
	id BIGINT PRIMARY KEY IDENTITY(1,1),
	internal_reddit_id NVARCHAR(16) UNIQUE NOT NULL,
	post_id BIGINT NOT NULL,
	author_id BIGINT NOT NULL,
	subreddit_id INTEGER NOT NULL,
	parent_comment_id BIGINT, -- if this one's null then it's a comment to the op
	body NVARCHAR(MAX) NOT NULL,
	edited_date DATETIME,
	upvotes INTEGER NOT NULL,
	downvotes INTEGER NOT NULL,
	creation_date DATETIME NOT NULL,
	FOREIGN KEY (post_id) REFERENCES Post(id),
	FOREIGN KEY (author_id, subreddit_id) REFERENCES Author(id, subreddit_id),
	FOREIGN KEY (parent_comment_id) REFERENCES Comment(id)
)
GO

-- Staging tables

CREATE TABLE Staging_Subreddit(
	internal_reddit_id NVARCHAR(16) UNIQUE,
	name NVARCHAR(512),
	subscribers INTEGER,
	nsfw BIT
)

CREATE TABLE Staging_Flair(
	internal_subreddit_id NVARCHAR(16),
	text NVARCHAR(512)
)

CREATE TABLE Staging_Author(
	internal_reddit_id NVARCHAR(16),
	internal_subreddit_id NVARCHAR(16),
	username NVARCHAR(512),
	flair NVARCHAR(512)
)

CREATE TABLE Staging_Post(
	internal_reddit_id NVARCHAR(16) UNIQUE,
	internal_subreddit_id NVARCHAR(16),
	internal_author_id NVARCHAR(16),
	flair NVARCHAR(512),
	title NVARCHAR(MAX),
	body NVARCHAR(MAX),
	edited_date DATETIME,
	upvotes INTEGER,
	downvotes INTEGER,
	nsfw BIT,
	spoiler BIT,
	creation_date DATETIME,
)

CREATE TABLE Staging_Comment(
	internal_reddit_id NVARCHAR(16) UNIQUE,
	internal_post_id NVARCHAR(16),
	internal_author_id NVARCHAR(16),
	internal_subreddit_id NVARCHAR(16),
	internal_parent_comment_id NVARCHAR(16),
	body NVARCHAR(MAX),
	edited_date DATETIME,
	upvotes INTEGER,
	downvotes INTEGER,
	creation_date DATETIME
)
GO