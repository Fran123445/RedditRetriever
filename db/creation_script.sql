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
	subreddit_id INTEGER,
	text NVARCHAR(512)
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
	creation_date DATETIME
)
GO

-- Staging -> Schema stored procedures

ALTER PROCEDURE usp_LoadSubredditsFromStaging AS
BEGIN
	WITH Subreddit_CTE AS (
		SELECT 
			internal_reddit_id,
			name,
			subscribers,
			nsfw
		FROM Staging_Subreddit
	)
	MERGE Subreddit AS S
	USING Subreddit_CTE AS SCTE
	ON S.internal_reddit_id = SCTE.internal_reddit_id
	WHEN MATCHED THEN
		UPDATE SET
			S.name = SCTE.name,
			S.subscribers = SCTE.subscribers,
			S.nsfw = SCTE.nsfw
	WHEN NOT MATCHED BY TARGET THEN
		INSERT (
			internal_reddit_id,
			name,
			subscribers,
			nsfw
		) VALUES (
			SCTE.internal_reddit_id,
			SCTE.name,
			SCTE.subscribers,
			SCTE.nsfw
		);	
END
GO

ALTER PROCEDURE usp_LoadFlairsFromStaging AS
BEGIN
	INSERT INTO Flair(
		subreddit_id,
		text
	)
	SELECT DISTINCT
		S.id,
		text
	FROM Staging_Flair SF JOIN Subreddit S ON
		SF.internal_subreddit_id = S.internal_reddit_id
	WHERE NOT EXISTS(
		SELECT 1 FROM Flair F2 WHERE F2.subreddit_id = S.id AND F2.text IS NOT DISTINCT FROM SF.text
	)
END
GO

ALTER PROCEDURE usp_LoadUsersFromStaging AS
BEGIN
	INSERT INTO [User](
		internal_reddit_id,
		username
	)
	SELECT DISTINCT
		internal_reddit_id,
		username
	FROM Staging_Author SA
	WHERE NOT EXISTS(
		SELECT 1 FROM [User] U WHERE U.internal_reddit_id = SA.internal_reddit_id
	)
END
GO

ALTER PROCEDURE usp_LoadAuthorsFromStaging AS
BEGIN
	WITH Author_CTE AS(
	SELECT DISTINCT
		U.id AS id,
		s.id AS Subreddit_id,
		f.id AS Flair_id
	FROM Staging_Author SA JOIN [User] U ON
		SA.internal_reddit_id = U.internal_reddit_id
	JOIN Subreddit S ON
		SA.internal_subreddit_id = S.internal_reddit_id
	LEFT JOIN Flair F ON -- left join because the flair can be null
		F.subreddit_id = S.id AND
		SA.flair IS NOT DISTINCT FROM F.text
	)
	MERGE Author AS A
	USING Author_CTE AS ACTE
	ON A.id = ACTE.id AND
		A.subreddit_id = ACTE.subreddit_id
	WHEN MATCHED THEN
		UPDATE SET
			A.flair_id = ACTE.flair_id
	WHEN NOT MATCHED BY TARGET THEN
		INSERT (
			id,
			subreddit_id,
			flair_id
		) VALUES (
			ACTE.id,
			ACTE.subreddit_id,
			ACTE.flair_id
		);
END
GO

ALTER PROCEDURE usp_LoadPostsFromStaging AS
BEGIN
	WITH Post_CTE AS(
		SELECT 
		SP.internal_reddit_id AS internal_reddit_id,
		S.id AS subreddit_id,
		A.id AS author_id,
		F.id AS flair_id,
		SP.title,
		SP.body,
		SP.edited_date,
		SP.upvotes,
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
		LEFT JOIN Flair F ON
			S.id = F.subreddit_id AND
			F.text IS NOT DISTINCT FROM SP.flair
	)
	MERGE Post AS P
	USING Post_CTE AS PCTE
	ON P.internal_reddit_id = PCTE.internal_reddit_id
	WHEN MATCHED THEN
		UPDATE SET
			P.flair_id = PCTE.flair_id,
			P.body = PCTE.body,
			P.edited_date = PCTE.edited_date,
			P.upvotes = PCTE.upvotes,
			P.nsfw = PCTE.nsfw,
			P.spoiler = PCTE.spoiler
	WHEN NOT MATCHED BY TARGET THEN
		INSERT (
			internal_reddit_id,
			subreddit_id,
			author_id,
			flair_id,
			title,
			body,
			edited_date,
			upvotes,
			nsfw,
			spoiler,
			creation_date
		) VALUES (
			PCTE.internal_reddit_id,
			PCTE.subreddit_id,
			PCTE.author_id,
			PCTE.flair_id,
			PCTE.title,
			PCTE.body,
			PCTE.edited_date,
			PCTE.upvotes,
			PCTE.nsfw,
			PCTE.spoiler,
			PCTE.creation_date
		);
END
GO

ALTER PROCEDURE usp_LoadCommentsFromStaging AS
BEGIN
	WITH Comment_CTE AS(
		SELECT
		SC.internal_reddit_id,
		P.id AS post_id,
		A.id AS author_id,
		S.id AS subreddit_id,
		ParentC.id AS parent_comment_id,
		SC.body,
		SC.edited_date,
		SC.upvotes,
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
	)
	MERGE Comment AS C
	USING Comment_CTE AS CCTE
	ON C.internal_reddit_id = CCTE.internal_reddit_id
	WHEN MATCHED THEN
		UPDATE SET
			C.body = CCTE.body,
			C.edited_date = CCTE.edited_date,
			C.upvotes = CCTE.upvotes
	WHEN NOT MATCHED BY TARGET THEN
		INSERT (
			internal_reddit_id,
			post_id,
			author_id,
			subreddit_id,
			parent_comment_id,
			body,
			edited_date,
			upvotes,
			creation_date
		) VALUES (
			CCTE.internal_reddit_id,
			CCTE.post_id,
			CCTE.author_id,
			CCTE.subreddit_id,
			CCTE.parent_comment_id,
			CCTE.body,
			CCTE.edited_date,
			CCTE.upvotes,
			CCTE.creation_date
		);

	-- This is because children might not get assigned their parent comment on the above merge
	UPDATE ChildComment
	SET
		ChildComment.parent_comment_id = ParentComment.id
	FROM Comment ChildComment JOIN Staging_Comment SC ON
		ChildComment.internal_reddit_id = SC.internal_reddit_id
	JOIN Comment ParentComment ON
		SC.internal_parent_comment_id = ParentComment.internal_reddit_id
	WHERE 
		SC.internal_parent_comment_id IS NOT NULL AND
		ChildComment.parent_comment_id IS NULL
END
GO

CREATE PROCEDURE usp_LoadTablesFromStaging AS
BEGIN
	EXEC usp_LoadSubredditsFromStaging
	EXEC usp_LoadFlairsFromStaging
	EXEC usp_LoadUsersFromStaging
	EXEC usp_LoadAuthorsFromStaging
	EXEC usp_LoadPostsFromStaging
	EXEC usp_LoadCommentsFromStaging
END

EXEC usp_LoadTablesFromStaging


SELECT
	S.name,
	S.subscribers,
	AVG(P.upvotes)/CAST(subscribers AS FLOAT) AS average_upvotes,
	COUNT(*)/CAST(subscribers AS FLOAT) as comments_per_subscriber
FROM Post P JOIN Subreddit S ON
	P.subreddit_id = S.id
JOIN Comment C ON
	C.post_id = P.id AND
	C.subreddit_id = S.id
GROUP BY 
	S.name, S.subscribers
ORDER BY 4 DESC

SELECT
	S.name,
	AVG((CAST(C.upvotes AS FLOAT)/CAST(S.subscribers AS FLOAT))/(LEN(C.body))) AS average_comment_length
FROM Comment C JOIN Subreddit S ON
	C.subreddit_id =S.id
GROUP BY S.name
ORDER BY 2 DESC

SELECT
	S.name,
	COUNT(*) AS ammount_of_comments,
	S.subscribers,
	COUNT(*)/CAST(S.subscribers AS FLOAT) AS comment_count_per_subs
FROM Post P JOIN Comment C ON
	P.id = C.post_id
JOIN Subreddit S ON
	P.subreddit_id = S.id
GROUP BY
	S.name,
	S.subscribers
ORDER BY 2 DESC

SELECT
	S.name,
	P.title,
	P.id,
	AVG(DATEDIFF(minute, P.creation_date, C.creation_date)) AS avg_time_diff_between_p_and_c
FROM Comment C JOIN Post P ON
	C.post_id = P.id
JOIN Subreddit S ON
	P.subreddit_id = S.id
GROUP BY
	S.name,
	P.title,
	S.subscribers,
	P.id
ORDER BY 3 ASC

DELETE Comment
DELETE Post
DELETE Author
DELETE [User]
DELETE Flair
DELETE Subreddit

DELETE Staging_Author
DELETE Staging_Comment
DELETE Staging_Post
DELETE Staging_Flair
DELETE Staging_Subreddit

DROP TABLE Comment
DROP TABLE Post
DROP TABLE Author
DROP TABLE [User]
DROP TABLE Flair
DROP TABLE Subreddit