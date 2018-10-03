from django_news.utils import constants
from users.models import User


def user_to_dict(self):
    resp_dict = {
        "id": self.id,
        "nick_name": self.nick_name,
        "avatar_url": constants.QINIU_DOMIN_PREFIX + self.avatar_url if self.avatar_url else "",
        "mobile": self.mobile,
        "gender": self.gender if self.gender else "MAN",
        "signature": self.signature if self.signature else "",
        "followers_count": self.followers.count(),
        "news_count": self.news_list.count()
    }
    return resp_dict


def user_to_admin_dict(self):
    resp_dict = {
        "id": self.id,
        "nick_name": self.nick_name,
        "mobile": self.mobile,
        "register": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        "last_login": self.last_login.strftime("%Y-%m-%d %H:%M:%S"),
    }
    return resp_dict


def news_to_review_dict(self):
    resp_dict = {
        "id": self.id,
        "title": self.title,
        "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": self.status,
        "reason": self.reason if self.reason else ""
    }
    return resp_dict


def news_to_basic_dict(self):
    resp_dict = {
        "id": self.id,
        "title": self.title,
        "source": self.source,
        "digest": self.digest,
        "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        "index_image_url": self.index_image_url,
        "clicks": self.clicks,
    }
    return resp_dict


def news_to_dict(self):
    resp_dict = {
        "id": self.id,
        "title": self.title,
        "source": self.source,
        "digest": self.digest,
        "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        "content": self.content,
        "comments_count": self.comments.count(),
        "clicks": self.clicks,
        "category": self.category.to_dict(),
        "index_image_url": self.index_image_url,
        "author": self.user.to_dict() if self.user else None
    }
    return resp_dict


def comment_to_dict(self):
    resp_dict = {
        "id": self.id,
        "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        "content": self.content,
        "parent": self.parent.to_dict() if self.parent else None,
        "user": User.query.get(self.user_id).to_dict(),
        "news_id": self.news_id,
        "like_count": self.like_count
    }
    return resp_dict


def category_to_dict(self):
    resp_dict = {
        "id": self.id,
        "name": self.name
    }
    return resp_dict
