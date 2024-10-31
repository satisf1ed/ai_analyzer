from sqlalchemy import exists

from db_architecture import Channel, Video, Comment
from db_sessions import session


def save_channel_info(channel_info: dict, channel_id: str):
    if not check_exists_channel_by_id(channel_id):
        channel_imp = Channel(
            channelId=channel_id,
            title=channel_info.get('snippet', {}).get('title'),
            description=channel_info.get('snippet', {}).get('description', None),
            customUrl=channel_info.get('snippet', {}).get('customUrl', None),
            publishedAt=channel_info.get('snippet', {}).get('publishedAt', None),
            thumbnail=channel_info.get('snippet', {}).get('thumbnails', {}).get('default', {}).get('url', None),
            localizedTitle=channel_info.get('snippet', {}).get('localized', {}).get('title', None),
            localizedDescription=channel_info.get('snippet', {}).get('localized', {}).get('description', None),
            country=channel_info.get('snippet', {}).get('country', None),
            relatedPlaylistsLikes=channel_info.get('contentDetails', {}).get('relatedPlaylists', {}).get('likes', None),
            relatedPlaylistsUploads=channel_info.get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads',
                                                                                                             None),
            viewCount=channel_info.get('statistics', {}).get('viewCount', None),
            subscribersCount=channel_info.get('statistics', {}).get('subscriberCount', None),
            hiddenSubscriberCount=channel_info.get('statistics', {}).get('hiddenSubscriberCount', None),
            videoCount=channel_info.get('statistics', {}).get('videoCount', None),
            topicCategories=channel_info.get('topicDetails', {}).get('topicCategories', None),
            privacyStatus=channel_info.get('status', {}).get('privacyStatus', None),
            isLinked=channel_info.get('status', {}).get('isLinked', None),
            longUploadsStatus=channel_info.get('status', {}).get('longUploadsStatus', None),
            madeForKids=channel_info.get('status', {}).get('madeForKids', None),
            brandingSettingsChannelTitle=channel_info.get('brandingSettings', {}).get('channel', {}).get('title', None),
            brandingSettingsChannelDescription=channel_info.get('brandingSettings', {}).get('channel', {}).get(
                'description', None),
            brandingSettingsChannelKeywords=channel_info.get('brandingSettings', {}).get('channel', {}).get('keywords',
                                                                                                               None),
            brandingSettingsChannelUnsubscribedTrailer=channel_info.get('brandingSettings', {}).get('channel', {}).get(
                'unsubscribedTrailer', None))
        session.add(channel_imp)
        session.commit()


def save_video_info(video_info: dict, channel_id: str, video_id: str):
    if not check_exists_video_by_id(video_id):
        video_imp = Video(
            channelId=channel_id,
            videoId=video_id,
            publishedAt=video_info.get('snippet', {}).get('publishedAt'),
            title=video_info.get('snippet', {}).get('title'),
            description=video_info.get('snippet', {}).get('description'),
            thumbnail=video_info.get('snippet', {}).get('thumbnails', {}).get('default', {}).get('url', None),
            channelTitle=video_info.get('snippet', {}).get('channelTitle', None),
            tags=video_info.get('snippet', {}).get('tags', None),
            liveBroadcastContent=video_info.get('snippet', {}).get('liveBroadcastContent', None),
            defaultLanguage=video_info.get('snippet', {}).get('defaultLanguage', None),
            defaultAudioLanguage=video_info.get('snippet', {}).get('defaultAudioLanguage', None),
            categoryId=video_info.get('snippet', {}).get('categoryId', None),
            duration=video_info.get('contentDetails', {}).get('duration', None),
            dimension=video_info.get('contentDetails', {}).get('dimension', None),
            definition=video_info.get('contentDetails', {}).get('definition', None),
            caption=video_info.get('contentDetails', {}).get('caption', None),
            licensedContent=video_info.get('contentDetails', {}).get('licensedContent', None),
            uploadStatus=video_info.get('status', {}).get('uploadStatus', None),
            privacyStatus=video_info.get('status', {}).get('privacyStatus', None),
            license=video_info.get('status', {}).get('license', None),
            embeddable=video_info.get('status', {}).get('embeddable', None),
            publicStatsViewable=video_info.get('status', {}).get('publicStatsViewable', None),
            madeForKids=video_info.get('status', {}).get('madeForKids', None),
            viewsCount=video_info.get('statistics', {}).get('viewCount', None),
            likesCount=video_info.get('statistics', {}).get('likeCount', None),
            favoriteCount=video_info.get('statistics', {}).get('favoriteCount', None),
            comment_count=video_info.get('statistics', {}).get('commentCount', None))
        session.add(video_imp)
        session.commit()

def save_comments(comment: dict, comment_id: str):
    if not check_exists_comment_by_id(comment_id):
        comment_imp = Comment(
            commentId=comment_id,
            videoId=comment.get('videoId', None),
            authorDisplayName=comment.get('authorDisplayName', None),
            authorProfileImageUrl=comment.get('authorProfileImageUrl', None),
            authorChannelUrl=comment.get('authorChannelUrl', None),
            authorChannelId=comment.get('authorChannelId', {}).get('value', None),
            textDisplay=comment.get('textDisplay', None),
            textOriginal=comment.get('textOriginal', None),
            parentId=comment.get('parentId', None),
            canRate=comment.get('canRate', None),
            viewerRating=comment.get('viewerRating', None),
            likeCount=comment.get('likeCount', None),
            publishedAt=comment.get('publishedAt', None),
            updatedAt=comment.get('updatedAt', None))
        session.add(comment_imp)
        session.commit()



def check_exists_video_by_id(video_id: str):
    exists_query = session.query(exists().where(Video.videoId == video_id)).scalar()

    if exists_query:
        return True
    else:
        return False


def check_exists_channel_by_id(channel_id: str):
    exists_query = session.query(exists().where(Channel.channelId == channel_id)).scalar()

    if exists_query:
        return True
    else:
        return False


def check_exists_comment_by_id(comment_id: str):
    exists_query = session.query(exists().where(Comment.commentId == comment_id)).scalar()

    if exists_query:
        return True
    else:
        return False
