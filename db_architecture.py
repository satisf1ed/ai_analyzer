from sqlalchemy import (
    BigInteger, Column, ForeignKey, Boolean, String, Time, JSON, create_engine
)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Channel(Base):
    __tablename__ = 'channels'

    id = Column(BigInteger, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    publishedAt = Column(Time)
    defaultLan = Column(String)

    # Relationships
    videos = relationship('Video', back_populates='channel')
    authored_comments = relationship('Comment', back_populates='author_channel', foreign_keys='Comment.authorChannelId')
    received_comments = relationship('Comment', back_populates='target_channel', foreign_keys='Comment.channelId')

    def __repr__(self):
        return (f"<Channel(id={self.id}, title='{self.title}', description='{self.description}', "
                f"publishedAt='{self.publishedAt}', defaultLan='{self.defaultLan}')>")


class Video(Base):
    __tablename__ = 'videos'

    id = Column(BigInteger, primary_key=True)
    publishedAt = Column(Time)
    channelId = Column(BigInteger, ForeignKey('channels.id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    channelTitle = Column(String)
    tags = Column(JSON)
    categoryId = Column(BigInteger)
    defaultLanguage = Column(String)
    duration = Column(String)

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
    __tablename__ = 'subtitles'

    id = Column(BigInteger, primary_key=True)
    videoId = Column(BigInteger, ForeignKey('videos.id'), nullable=False)
    text = Column(String)

    # Relationships
    video = relationship('Video', back_populates='subtitles')

    def __repr__(self):
        return f"<Subtitle(id={self.id}, videoId={self.videoId}, text='{self.text}')>"


class Comment(Base):
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
    publishedAt = Column(Time)
    updatedAt = Column(Time)

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
