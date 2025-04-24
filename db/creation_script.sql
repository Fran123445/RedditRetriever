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

-- Staging -> Schema stored procedures

CREATE PROCEDURE usp_LoadSubredditsFromStaging AS
BEGIN
	INSERT INTO Subreddit(
		internal_reddit_id,
		name,
		subscribers,
		nsfw
	)
	SELECT 
		internal_reddit_id,
		name,
		subscribers,
		nsfw
	FROM Staging_Subreddit
END
GO

CREATE PROCEDURE usp_LoadFlairsFromStaging AS
BEGIN
	INSERT INTO Flair(
		subreddit_id,
		text
	)
	SELECT
		internal_subreddit_id,
		text
	FROM Staging_Flair
		
END
GO

CREATE PROCEDURE usp_LoadUsersFromStaging AS
BEGIN
	INSERT INTO [User](
		internal_reddit_id,
		username
	)
	SELECT
		internal_reddit_id,
		username
	FROM Staging_Author
END
GO

CREATE PROCEDURE usp_LoadAuthorsFromStaging AS
BEGIN
	INSERT INTO Author(
		id,
		subreddit_id,
		flair_id
	)
	SELECT
		U.id,
		s.id,
		f.id
	FROM Staging_Author SA JOIN [User] U ON
		SA.internal_reddit_id = U.internal_reddit_id
	JOIN Subreddit S ON
		SA.internal_subreddit_id = S.internal_reddit_id
	JOIN Flair F ON
		SA.flair = F.text
END
GO

CREATE PROCEDURE usp_LoadPostsFromStaging AS
BEGIN
	INSERT INTO POST (
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
	)
	SELECT 
		SP.internal_reddit_id,
		S.id,
		A.id,
		F.id,
		SP.title,
		SP.body,
		SP.edited_date,
		SP.upvotes,
		SP.downvotes,
		SP.nsfw,
		SP.spoiler,
		SP.creation_date
	FROM Staging_Post SP JOIN Subreddit S ON
		SP.internal_subreddit_id = S.internal_reddit_id
	JOIN [User] U ON
		SP.internal_author_id = U.internal_reddit_id
	JOIN Author A ON
		S.id = A.subreddit_id AND
		U.id = A.id
	JOIN Flair F ON
		S.id = F.subreddit_id AND
		F.text = SP.flair
END
GO

CREATE PROCEDURE usp_LoadCommentsFromStaging AS
BEGIN
	INSERT INTO Comment (
		internal_reddit_id,
		post_id,
		author_id,
		subreddit_id,
		parent_comment_id,
		body,
		edited_date,
		upvotes,
		downvotes,
		creation_date
	)
	SELECT
		SC.internal_reddit_id,
		P.id,
		A.id,
		S.id,
		ParentC.id,
		SC.body,
		SC.edited_date,
		SC.upvotes,
		SC.downvotes,
		SC.creation_date
	FROM Staging_Comment SC
	JOIN Subreddit S ON
		SC.internal_subreddit_id = S.internal_reddit_id
	JOIN Post P ON
		SC.internal_post_id = P.internal_reddit_id
	JOIN [User] U ON
		SC.internal_author_id = U.internal_reddit_id
	JOIN Author A ON
		U.id = A.id AND S.id = A.subreddit_id
	LEFT JOIN Comment ParentC ON
		S.id = ParentC.subreddit_id AND
		SC.internal_parent_comment_id = ParentC.internal_reddit_id
END
GO