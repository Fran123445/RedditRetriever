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
	id BIGINT PRIMARY KEY IDENTITY(1,1),
	text NVARCHAR(512)
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
	FOREIGN KEY (flair_id) REFERENCES Flair(id)
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
	FOREIGN KEY (flair_id) REFERENCES Flair(id)
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

-- Data loading SPs

CREATE PROCEDURE spLoadSubreddit(
	@internal_reddit_id NVARCHAR(16),
	@name NVARCHAR(512),
	@subscribers INTEGER,
	@nsfw INT
) AS
BEGIN
	INSERT INTO Subreddit(
		internal_reddit_id,
		name,
		subscribers,
		nsfw
	) VALUES (
		@internal_reddit_id,
		@name,
		@subscribers,
		@nsfw
	)
END
GO

CREATE PROCEDURE spLoadFlair(
	@text NVARCHAR(512)
) AS
BEGIN
	INSERT INTO Flair(
		text
	) VALUES (
		@text
	)
END
GO

CREATE PROCEDURE spLoadUser(
	@internal_reddit_id NVARCHAR(16),
	@username NVARCHAR(512)
) AS
BEGIN
	INSERT INTO [User](
		internal_reddit_id,
		username
	) VALUES (
		@internal_reddit_id,
		@username
	)
END
GO

CREATE PROCEDURE spLoadAuthor(
	@user_id BIGINT,
	@subreddit_id INTEGER,
	@flair_id BIGINT
) AS
BEGIN
	INSERT INTO Author(
		id,
		subreddit_id,
		flair_id
	) VALUES (
		@user_id,
		@subreddit_id,
		@flair_id
	)
END
GO

CREATE PROCEDURE spLoadPost(
	@internal_reddit_id NVARCHAR(16),
	@subreddit_id INTEGER,
	@author_id BIGINT,
	@flaird_id BIGINT,
	@title NVARCHAR(512),
	@body NVARCHAR(MAX),
	@edited_date DATETIME,
	@upvotes INTEGER,
	@downvotes INTEGER,
	@nsfw BIT,
	@spoiler BIT,
	@creation_date DATETIME
) AS
BEGIN
	INSERT INTO Post(
		internal_reddit_id,
		subreddit_id,
		author_id,
		flair_id,
		title,
		body,
		edited_date,
		upvotes,
		downvotes,
		nsfw,
		spoiler,
		creation_date
	) VALUES (
		@internal_reddit_id,
		@subreddit_id,
		@author_id,
		@flaird_id,
		@title,
		@body,
		@edited_date,
		@upvotes,
		@downvotes,
		@nsfw,
		@spoiler,
		@creation_date
	)
END
GO

CREATE PROCEDURE spLoadComment(
	@internal_reddit_id NVARCHAR(16),
	@post_id BIGINT,
	@author_id BIGINT,
	@parent_comment_id BIGINT,
	@body NVARCHAR(MAX),
	@edited_date DATETIME,
	@upvotes INTEGER,
	@downvotes INTEGER,
	@creation_date DATETIME
) AS
BEGIN
	INSERT INTO Comment(
		internal_reddit_id,
		post_id,
		author_id,
		parent_comment_id,
		body,
		edited_date,
		upvotes,
		downvotes,
		creation_date
	) VALUES (
		@internal_reddit_id,
		@post_id,
		@author_id,
		@parent_comment_id,
		@body,
		@edited_date,
		@upvotes,
		@downvotes,
		@creation_date
	)
END
GO