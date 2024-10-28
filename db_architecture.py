from sqlalchemy import (
    BigInteger, Column, ForeignKey, Boolean, String, Time, create_engine, Double, DateTime, ARRAY
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Channel(Base):
    """
    Represents a YouTube channel with metadata including title, description, and various settings.

    Attributes:
        id (BigInteger): Unique identifier for the channel.
        title (str): The title of the YouTube channel.
        description (str): Detailed description of the channel's content.
        customUrl (str): Custom URL for the channel.
        publishedAt (DateTime): Date and time of the channel's publication.
        thumbnail (str): URL to the channel's thumbnail image.
        localizedTitle (str): Localized version of the channel's title.
        localizedDescription (str): Localized version of the channel's description.
        county (str): Country associated with the channel.
        relatedPlaylistsLikes (str): Playlist ID for videos liked by the channel.
        relatedPlaylistsUploads (str): Playlist ID for videos uploaded by the channel.
        viewCount (BigInteger): Total view count of the channel.
        subscribersCount (BigInteger): Total subscriber count of the channel.
        hiddenSubscriberCount (bool): Indicates if subscriber count is hidden.
        videoCount (BigInteger): Total number of videos on the channel.
        topicCategories (ARRAY of str): List of topic categories associated with the channel.
        privacyStatus (str): Privacy status of the channel.
        isLinked (bool): Indicates if the channel is linked to a Google account.
        longUploadsStatus (str): Status of long uploads for the channel.
        madeForKids (bool): Indicates if the channel is designated for kids.
        brandingSettingsChannelTitle (str): Custom title in branding settings.
        brandingSettingsChannelDescription (str): Custom description in branding settings.
        brandingSettingsChannelKeywords (str): Custom keywords in branding settings.
        brandingSettingsChannelUnsubscribedTrailer (str): Trailer URL shown to unsubscribed viewers.

    Relationships:
        videos (Video): List of `Video` objects related to the channel.
        authored_comments (Comment): List of `Comment` objects authored by this channel.
        received_comments (Comment): List of `Comment` objects directed to this channel.
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
    Represents a video on a YouTube channel, with metadata about publication, content, and categorization.

    Attributes:
        id (BigInteger): Unique identifier for the video.
        publishedAt (DateTime): Publication timestamp for the video.
        channelId (BigInteger): Foreign key reference to the associated channel's ID.
        title (str): Title of the video.
        description (str): Detailed description of the video's content.
        thumbnail (str): URL to the video's thumbnail image.
        channelTitle (str): Name of the channel that uploaded the video.
        tags (ARRAY of str): Tags associated with the video.
        liveBroadcastContent (str): Indicates if the video is a live broadcast.
        defaultLanguage (str): Default language of the video's content.
        defaultAudioLanguage (str): Default audio language of the video's content.
        categoryId (str): ID of the video's category.
        duration (str): Duration of the video in ISO 8601 format.
        dimension (str): Dimension of the video (e.g., 2D, 3D).
        definition (str): Quality definition (e.g., HD, SD).
        caption (str): Indicates if captions are available.
        licensedContent (bool): Indicates if the video is licensed content.
        uploadStatus (str): Upload status of the video.
        privacyStatus (str): Privacy status of the video.
        license (str): License type for the video.
        embeddable (bool): Indicates if the video is embeddable on other sites.
        publicStatsViewable (bool): Indicates if public statistics are viewable.
        madeForKids (bool): Indicates if the video is designated for kids.
        viewsCount (BigInteger): View count of the video.
        likesCount (BigInteger): Like count for the video.
        favoriteCount (BigInteger): Favorite count for the video.
        comment_count (BigInteger): Comment count for the video.

    Relationships:
        channel (Channel): The `Channel` object associated with the video.
        subtitles (Subtitle): List of `Subtitle` objects associated with the video.
        comments (Comment): List of `Comment` objects associated with the video.
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
    Represents subtitles linked to a YouTube video, containing textual content and timing information.

    Attributes:
        id (BigInteger): Unique identifier for the subtitle.
        videoId (BigInteger): Foreign key reference to the associated video's ID.
        text (str): Subtitle text.
        start (Double): Start time of the subtitle in seconds.
        duration (Double): Duration of the subtitle in seconds.

    Relationships:
        video (Video): The `Video` object associated with the subtitle.
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


engine = create_engine('postgresql://admin:admin@localhost:5432/postgres')

Base.metadata.create_all(engine)
