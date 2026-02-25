from enum import Enum


class Enums(str, Enum):
    def __str__(self):
        return self.value

    def __repr__(self):
        return repr(self.value)


class likePostAction(Enums):
    Like = "Like"
    Unlike = "Unlike"
    Explore_two_tower = "Explore:two_tower"
    Profile = "Profile"
    Feed = "Feed"


class postBookmarkAction(Enums):
    Bookmark = "Bookmark"
    Unbookmark = "Unbookmark"
    Explore = "Explore"
    Feed = "Feed"


class requestFollow(Enums):
    Follower = "Follower"
    Following = "Following"
    Related_two_tower = "Related:two_tower"
    Feed = "Feed"


class likeCommentAction(Enums):
    Unlike = "Unlike"
    Like = "Like"
    Explore_two_tower = "Explore:two_tower"
    Feed = "Feed"


class setReportRecord(Enums):
    Post = "Post"
    Profile = "Profile"
    reason_1 = 1
    reason_2 = 2


class getFollowers(Enums):
    Follower = "Follower"
    Following = "Following"


class getRelatedExplorePost(Enums):
    start_id = "AI_RE_2"
    Explore_two_tower = "Explore:two_tower"
    Feed = "Feed"
    Explore = "Explore"


class updateProfile(Enums):
    Everyone = "Everyone"
    NoOne = "NoOne"
    Following = "Following"
    Private = "Private"
    Public = "Public"


class updateProfile(Enums):
    Search = "Search"
