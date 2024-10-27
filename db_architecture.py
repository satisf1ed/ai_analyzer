from sqlalchemy import (
    BigInteger, Column, ForeignKey, Boolean, String, Time, JSON, create_engine, Double, DateTime, ARRAY
)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Channel(Base):
    """
        Represents a YouTube channel with metadata such as title, description, and language.

        Attributes:
            id (BigInteger): Primary key identifier for the channel.
            title (str): Title of the channel.
            description (str): Description of the channel content.
            publishedAt (Time): Time when the channel was published.
            defaultLan (str): Default language for the channel.

        Relationships:
            videos (Video): Relationship with the `Video` class.
            authored_comments (Comment): Relationship with comments authored by this channel.
            received_comments (Comment): Relationship with comments received by this channel.
        """

    __tablename__ = 'channels'

    id = Column(BigInteger, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    customUrl = Column(String)
    publishedAt = Column(DateTime)
    thumbnail = Column(String)
    localizedTitle = Column(String)
    localizedDescription = Column(String)
    county = Column(String)
    relatedPlaylistsLikes = Column(String)
    relatedPlaylistsUploads = Column(String)
    viewCount = Column(BigInteger)
    subscribersCount = Column(BigInteger)
    hiddenSubscriberCount = Column(Boolean)
    videoCount = Column(BigInteger)
    topicCategories = Column(ARRAY(String))
    privacyStatus = Column(String)
    isLinked = Column(Boolean)
    longUploadsStatus = Column(String)
    madeForKids = Column(Boolean)
    brandingSettingsChannelTitle = Column(String)
    brandingSettingsChannelDescription = Column(String)
    brandingSettingsChannelKeywords = Column(String)
    brandingSettingsChannelUnsubscribedTrailer = Column(String)


    # Relationships
    videos = relationship('Video', back_populates='channel')
    authored_comments = relationship('Comment', back_populates='author_channel', foreign_keys='Comment.authorChannelId')
    received_comments = relationship('Comment', back_populates='target_channel', foreign_keys='Comment.channelId')

    def __repr__(self):
        return (f"<Channel(id={self.id}, title='{self.title}', description='{self.description}', "
                f"publishedAt='{self.publishedAt}'>")


class Video(Base):
    """
        Represents a video uploaded to a YouTube channel.

        Attributes:
            id (BigInteger): Primary key identifier for the video.
            publishedAt (Time): Timestamp for when the video was published.
            channelId (BigInteger): Foreign key reference to the channel's ID.
            title (str): Title of the video.
            description (str): Description of the video content.
            channelTitle (str): Name of the channel that published the video.
            tags (JSON): JSON field containing tags associated with the video.
            categoryId (BigInteger): ID of the video category.
            defaultLanguage (str): Default language for the video.
            duration (str): Duration of the video.

        Relationships:
            channel (Channel): Relationship with the `Channel` class.
            subtitles (Subtitle): Relationship with subtitles associated with the video.
            comments (Comment): Relationship with comments associated with the video.
        """

    __tablename__ = 'videos'

    id = Column(BigInteger, primary_key=True)
    publishedAt = Column(DateTime)
    channelId = Column(BigInteger, ForeignKey('channels.id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    thumbnail = Column(String)
    channelTitle = Column(String)
    tags = Column(ARRAY(String))
    liveBroadcastContent = Column(String)
    defaultLanguage = Column(String)
    defaultAudioLanguage = Column(String)
    categoryId = Column(String)
    duration = Column(String)
    dimension = Column(String)
    definition = Column(String)
    caption = Column(String)
    licensedContent = Column(Boolean)
    uploadStatus = Column(String)
    privacyStatus = Column(String)
    license = Column(String)
    embeddable = Column(Boolean)
    publicStatsViewable = Column(Boolean)
    madeForKids = Column(Boolean)
    viewsCount = Column(BigInteger)
    likesCount = Column(BigInteger)
    favoriteCount = Column(BigInteger)
    comment_count = Column(BigInteger)


    # Relationships
    channel = relationship('Channel', back_populates='videos')
    subtitles = relationship('Subtitle', back_populates='video')
    comments = relationship('Comment', back_populates='video')

    def __repr__(self):
        return (f"<Video(id={self.id}, publishedAt='{self.publishedAt}', channelId={self.channelId}, "
                f"title='{self.title}', description='{self.description}', channelTitle='{self.channelTitle}', "
                f"tags={self.tags}, categoryId={self.categoryId}, defaultLanguage='{self.defaultLanguage}', "
                f"duration='{self.duration}')>")


class Subtitle(Base):
    """
        Represents subtitles associated with a specific video.

        Attributes:
            id (BigInteger): Primary key identifier for the subtitle.
            videoId (BigInteger): Foreign key reference to the associated video's ID.
            text (str): The subtitle text.

        Relationships:
            video (Video): Relationship with the `Video` class.
        """

    __tablename__ = 'subtitles'

    id = Column(BigInteger, primary_key=True)
    videoId = Column(BigInteger, ForeignKey('videos.id'), nullable=False)
    text = Column(String)
    start = Column(Double)
    duration = Column(Double)

    # Relationships
    video = relationship('Video', back_populates='subtitles')

    def __repr__(self):
        return f"<Subtitle(id={self.id}, videoId={self.videoId}, text='{self.text}')>"


class Comment(Base):
    """
       Represents a comment on a video, including author information and comment metadata.

       Attributes:
           id (BigInteger): Primary key identifier for the comment.
           videoId (BigInteger): Foreign key reference to the video's ID the comment is associated with.
           authorDisplayName (str): Display name of the comment's author.
           authorChannelUrl (str): URL of the author's channel.
           authorChannelId (BigInteger): Foreign key reference to the author's channel ID.
           channelId (BigInteger): Foreign key reference to the channel receiving the comment.
           textDisplay (str): Display text of the comment.
           textOriginal (str): Original text of the comment.
           parentId (BigInteger): Foreign key reference to the parent comment ID, if it is a reply.
           canRate (bool): Indicates if the comment can be rated.
           viewerRating (str): The viewer's rating on the comment.
           likeCount (BigInteger): Number of likes on the comment.
           moderationStatus (str): Moderation status of the comment.
           publishedAt (Time): Timestamp for when the comment was published.
           updatedAt (Time): Timestamp for when the comment was last updated.

       Relationships:
           video (Video): Relationship with the `Video` class.
           author_channel (Channel): Relationship with the channel authoring the comment.
           target_channel (Channel): Relationship with the channel receiving the comment.
           parent_comment (Comment): Self-referential relationship for nested comments.
       """

    __tablename__ = 'comments'

    id = Column(BigInteger, primary_key=True)
    videoId = Column(BigInteger, ForeignKey('videos.id'), nullable=False)
    authorDisplayName = Column(String)
    authorChannelUrl = Column(String)
    authorChannelId = Column(BigInteger, ForeignKey('channels.id'))
    channelId = Column(BigInteger, ForeignKey('channels.id'))
    textDisplay = Column(String)
    textOriginal = Column(String)
    parentId = Column(BigInteger, ForeignKey('comments.id'), nullable=True)
    canRate = Column(Boolean)
    viewerRating = Column(String)
    likeCount = Column(BigInteger)
    moderationStatus = Column(String)
    publishedAt = Column(DateTime)
    updatedAt = Column(DateTime)

    # Relationships
    video = relationship('Video', back_populates='comments')
    author_channel = relationship('Channel', back_populates='authored_comments', foreign_keys=[authorChannelId])
    target_channel = relationship('Channel', back_populates='received_comments', foreign_keys=[channelId])
    parent_comment = relationship('Comment', remote_side=[id], uselist=False)

    def __repr__(self):
        return (f"<Comment(id={self.id}, videoId={self.videoId}, authorDisplayName='{self.authorDisplayName}', "
                f"authorChannelUrl='{self.authorChannelUrl}', authorChannelId={self.authorChannelId}, "
                f"channelId={self.channelId}, textDisplay='{self.textDisplay}', textOriginal='{self.textOriginal}', "
                f"parentId={self.parentId}, canRate={self.canRate}, viewerRating='{self.viewerRating}', "
                f"likeCount={self.likeCount}, moderationStatus='{self.moderationStatus}', "
                f"publishedAt='{self.publishedAt}', updatedAt='{self.updatedAt}')>")


engine = create_engine('sqlite:///youtube.db')

Base.metadata.create_all(engine)
