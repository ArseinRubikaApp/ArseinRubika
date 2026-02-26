```markdown
# 📘 مستندات کامل کلاس‌های ArseinRubika (Arsein.py)

**نسخه:** آخرین کامیت اصلی (فوریه ۲۰۲۶)  
**کلاس‌ها:** Messenger (اصلی)، Bot (بات توکنی)، Rubino (روبینو)  
**تعداد کل متدها:** Messenger ≈ ۱۸۵ متد | Bot ≈ ۴۵ متد | Rubino ≈ ۵۷ متد  

---

## ۱. کلاس Messenger (اصلی - UserBot)

```python
class Messenger:
    def __init__(
        self,
        Sh_account: str = None,
        keyAccount: str = None,
        TypePlat: str = None,
        session_file: str = None,
        Proxy: Optional[Union[str, List[str]]] = None,
    ):
```

### تمام متدهای Messenger با پارامترها (به ترتیب فایل)
1. `def __repr__(self):`
2. `@property def thumb_inline(self):`
3. `@classmethod def _getDataUser(cls):`
4. `def sendMessage(self, guid: str, text: str, link: str = None, Guid_mention: str = None, message_id: str = None):`
5. `def editMessage(self, guid: str, new: str, message_id: str):`
6. `def deleteMessages(self, guid: str, message_ids: str, All: bool = False):`
7. `def getMessagefilter(self, guid: str, filter_whith: str, sort: str = "FromMax"):`
8. `def getMessages(self, guid: str, min_id: int):`
9. `def getMessagesbySort(self, guid: str, message_id: list, Type: str):`
10. `def searchMessages(self, guid: str, text: str):`
11. `def getChats(self, start_id: str = None):`
12. `def getMapView(self, latitude, longitude):`
13. `def sendMap(self, guid: str, latitude: float, longitude: float):`
14. `def getMessagesUpdates(self, guid: str):`
15. `def getChatsUpdate(self):`
16. `def deleteUserChat(self, user_guid: str, last_message: list):`
17. `def startSupperBot(self, guid: str):`
18. `def stoptSupperBot(self, guid: str):`
19. `def getBotInfo(self, guid: str):`
20. `def sendChatActivity(self, user_guid: str):`
21. `def getInfoByUsername(self, username: str):`
22. `def banGroupMember(self, guid_gap: str, user_id: str):`
23. `def unbanGroupMember(self, guid_gap: str, user_id: str):`
24. `def banChannelMember(self, guid_channel: str, user_id: str):`
25. `def unbanChannelMember(self, guid_channel: str, user_id: str):`
26. `def getGroupMentionList(self, guid_group: str, text: str):`
27. `def shaireContect(self, guid: str, phone_number: str, first_name: str, last_name: str = None):`
28. `def report(self, guid: str, reportType: int):`
29. `def reportPost(self, guid: str, reportType: int, message_id: str):`
30. `def otherReport(self, TYPE: str, guid: str, text: str, message_id: str = None):`
31. `def getbanGroupUsers(self, guid_gap: str, text: str = None, start_id: str = None):`
32. `def getbanChannelUsers(self, guid_channel: str, text: str = None, start_id: str = None):`
33. `def getGroupInfo(self, guid_gap: str):`
34. `def getChannelInfo(self, guid_channel: str):`
35. `def addMemberGroup(self, guid_gap: str, user_ids: list):`
36. `def addMemberChannel(self, guid_channel: str, user_ids: str):`
37. `def getGroupAdmins(self, guid_gap: str):`
38. `def getChannelAdmins(self, guid_channel: str):`
39. `def AddNumberPhone(self, first_num: str, numberPhone: str, last_num: str = None):`
40. `def getMessagesInfo(self, guid: str, message_ids: list):`
41. `def getGroupMembers(self, guid_gap, text=None, start_id=None):`
42. `def getChannelMembers(self, channel_guid: str, text: str = None, start_id: str = None):`
43. `def lockGroup(self, guid_gap: str):`
44. `def unlockGroup(self, guid_gap: str):`
45. `def getGroupAccess(self, guid_gap: str):`
46. `def getGroupLink(self, guid_gap):`
47. `def GroupOnlineCount(self, guid_gap: str):`
48. `def getChannelLink(self, guid_channel: str):`
49. `def changeGroupLink(self, guid_gap: str):`
50. `def changeChannelLink(self, guid_channel: str):`
51. `def setGroupTimer(self, guid_gap: str, time: int):`
52. `def limit_storage_Group(self, guid_gap: str, active: bool):`
53. `def limit_storage_Channel(self, guid_channel: str, active: bool):`
54. `def getGroupMessageReadParticipants(self, guid_gap: str, message_id: str):`
55. `def setGroupAdmin(self, guid_gap: str, guid_member: str, access_admin: list = None):`
56. `def deleteGroupAdmin(self, guid_gap: str, guid_admin: str):`
57. `def deleteGroup(self, guid_gap: str):`
58. `def setChannelAdmin(self, guid_channel: str, guid_member: str, access_admin: list = None):`
59. `def deleteChannelAdmin(self, guid_channel: str, guid_admin: str):`
60. `def getStickersByEmoji(self, emojee: str):`
61. `def searchStickerSets(self, text: str, start_id: str = None):`
62. `def getTrendStickerSets(self, start_id: str = None):`
63. `def getStickerSetByID(self, sticker_set_id: str = None):`
64. `def actionStickerSet(self, action: int, sticker_set_id: str = None):`
65. `def activenotification(self, guid: str):`
66. `def offnotification(self, guid: str):`
67. `def sendPoll(self, guid: str, question: str, options: list):`
68. `def sendPollExam(self, guid: str, question: str, options: list, explanation: str, correct_option_index: int):`
69. `def getPollStatus(self, poll_id: str):`
70. `def getVoters(self, poll_id: str, index: Union[str, int]):`
71. `def votePoll(self, poll_id: str, index: Union[str, int]):`
72. `def forwardMessages(self, From: str, message_ids: Union[str, int, list], to: str):`
73. `def VisitChatGroup(self, guid_gap: str):`
74. `def HideChatGroup(self, guid_gap: str):`
75. `def pin(self, guid: str, message_id: Union[str, int]):`
76. `def unpin(self, guid: str, message_id: Union[str, int]):`
77. `def logout(self):`
78. `def joinGroup(self, link: str):`
79. `def getJoinLinkUserJoined(self, object_guid: str, join_link: str, start_id: str = None):`
80. `def joinChannelAll(self, guid: str):`
81. `def joinChannelByLink(self, link: str):`
82. `def joinChannelByID(self, ide: str):`
83. `def joinChannelByGuid(self, guid: str):`
84. `def leaveGroup(self, guid_gap: str):`
85. `def leaveChannel(self, guid_channel: str):`
86. `def EditNameGroup(self, groupgu: str, namegp: str):`
87. `def EditBioGroup(self, groupgu: str, biogp: str):`
88. `def block(self, guid_user: str):`
89. `def unblock(self, guid_user: str):`
90. `def startVoiceChat(self, guid: str):`
91. `def addUserContact(self, guid: str):`
92. `def getVoiceChatId(self, guid: str):`
93. `def joinGroupVoiceChat(self, guid_g_ch: str, guid_user: str):`
94. `def getGroupVoiceChat(self, guid: str):`
95. `def getGroupVoiceChatParticipants(self, guid: str, start_id: str = None):`
96. `def editVoiceChat(self, guid: str, bol: bool = True):`
97. `def changeTitleVoiceChat(self, guid: str, title: str):`
98. `def finishVoiceChat(self, guid: str):`
99. `def leaveGroupVoiceChat(self, guid: str):`
100. `def getDisplayAsInGroupVoiceChat(self, guid: str, start_id: str = None):`
101. `def sendGroupVoiceChatActivity(self, guid: str, guiduser: str = None, activity: str = "Speaking"):`
102. `def getGroupVoiceChatUpdates(self, guid: str):`
103. `def setGroupVoiceChatState(self, guid: str, state: bool, guid_member: str = None):`
104. `def getUserInfo(self, guid_user: str):`
105. `def getUserInfoByIDE(self, IDE_user: str):`
106. `def seeGroupbyLink(self, link_gap: str):`
107. `def seeChannelbyLink(self, link_channel: str):`
108. `def getAvatars(self, guid: str):`
109. `def uploadAvatar_replay(self, files_ide: str):`
110. `def uploadAvatar(self, main: str, thumbnail: str = None):`
111. `def removeAvatar(self, guid: str):`
112. `def removeAllAvatars(self, guid: str):`
113. `def Devicesrubika(self, service_guid: str):`
114. `def getPaymentInfo(self, payment_id: Union[str, int]):`
115. `def deleteChatHistory(self, guid: str, last_message_id: str):`
116. `def addFolder(self, Name="Arsein", include_chat: list[str] = None, include_object: list[str] = None, exclude_chat: list[str] = None, exclude_object: list[str] = None):`
117. `def deleteFolder(self, folder_id: str):`
118. `def addGroup(self, title: str, guidsUser: list):`
119. `def deleteGroup(self, guid_group: str):`
120. `def addChannel(self, title: str, typeChannell: int, bio: str, guidsUser: list):`
121. `def editUser(self, first_name: str = None, last_name: str = None, bio: str = None):`
122. `def editUsername(self, username: str):`
123. `def editDate_birth(self, birth_date: str):`
124. `def Postion(self, guid, guiduser):`
125. `def getPostion(self, guid: str):`
126. `def AcceptPostion(self, guid: str):`
127. `def RejectPostion(self, guid: str):`
128. `def sendLive(self, guid: str, titlelive: str):`
129. `def ClearAccounts(self):`
130. `def DeleteAccount(self):`
131. `def selectionClearAccount(self, session_key: str):`
132. `def HidePhone(self, **kwargs: dict):`
133. `def HideOnline(self, **kwargs: dict):`
134. `def search_inaccount(self, text: str):`
135. `def search_inrubika(self, text: str):`
136. `def getAbsObjects(self, guids: list[str]):`
137. `def Infolinkpost(self, linkpost: str):`
138. `def addToMyGifSet(self, guid: str, message_id: str):`
139. `def deleteMyGifSet(self, file_id: Union[str, int, list]):`
140. `def getContactsLastOnline(self, user_guids: list[str]):`
141. `def SignMessageChannel(self, guid_channel: str, sign: bool = False):`
142. `def ActiveContectJoin(self):`
143. `def ActiveEverybodyJoin(self):`
144. `def CalledBy(self, typeCall: str):`
145. `def changeChannelID(self, guid_channel: str, username: str):`
146. `def getMessageShareUrl(self, guid: str, messageId: Union[str, list]):`
147. `def getBlockedUsers(self, start_id: str = None):`
148. `def deleteContact(self, guid_user: str):`
149. `def checkUserUsername(self, username: str):`
150. `def checkChannelUsername(self, username: str):`
151. `def getContacts(self, start_id: str = None):`
152. `def getLiveStatus(self, live_id: Optional[Union[str, int]], token_live: Optional[Union[str, int]]):`
153. `def getLiveComments(self, live_id: Optional[Union[str, int]], token_live: Optional[Union[str, int]]):`
154. `def getdatabaseReaction(self):`
155. `def Reaction(self, guid: str, typeReaction: str, reaction: str, message_id: str):`
156. `def commonGroup(self, guid_user: str):`
157. `def setTypeChannel(self, guid_channel: str, Private: bool = False):`
158. `def getChatAds(self, user_guids: list):`
159. `def clickMessageUrl(self, guid: str, message_id: Optional[Union[str, int, list]], link: str):`
160. `def seenChat(self, guid: str, message_id: str):`
161. `def getContactsUpdates(self):`
162. `def twolocks(self, ramz: str, hide: str):`
163. `def deletetwolocks(self, password: str):`
164. `def checkPassword(self, password: str):`
165. `def passwordChange(self, password: str):`
166. `def loginforgetPassword(self, emailCode: Optional[Union[str, int]], password: str, phone_number: Optional[Union[str, int]]):`
167. `def ProfileEdit(self, first_name: str = None, last_name: str = None, bio: str = None, username: str = None):`
168. `def getChatGroup(self, guid_gap: str):`
169. `def getChatChannel(self, guid_channel: str):`
170. `def getChatUser(self, guid_User: str):`
171. `def Authrandom(self):`
172. `def requestSendFile(self, addressfile: str):`
173. `def resend(self, guid: str, message_id: list[str]):`
174. `def downloadFiles(self, guid: str, message_id: list[str, int], save: str = None, link: bool = False):`
175. `def Http(self, link: str, formats: str):`
176. `def SendSticker(self, guid: str, emoji_character: str, w_h_ratio: str, sticker_id: str, sticker_set_id: str, file_id: str = None, dc_id: str = None, access_hash_rec: str = None):`
177. `def SendImage(self, guid: str, addressfile: str, spoil: bool = False, thumbinline: str = None, caption: str = None, message_id: str = None):`
178. `def SendFile(self, guid: str, addressfile: str, formats: str = None, caption: str = None, message_id: str = None):`
179. `def SendVideo(self, guid: str, addressfile: str, spoil: bool = False, thumbinline: str = None, caption: str = None, message_id: str = None):`
180. `def SendGif(self, guid: str, addressfile: str, thumbinline: str = None, caption: str = None, message_id: str = None):`
181. `def SendVoice(self, guid: str, addressfile: str, timevoice: Optional[Union[str, int]] = None, caption: str = None, message_id: str = None):`
182. `def SendMusic(self, guid: str, addressfile: str, caption: str = None, message_id: str = None):`
183. `def getJoinRequests(self, object_guid: str):`
184. `def AcceptJoinRequest(self, object_guid: str, user_guid: str):`
185. `def RejectJoinRequest(self, object_guid: str, user_guid: str):`
186. `def run(self):`
187. `def register(self):` (و متدهای بات داخلی)

---

## ۲. کلاس Bot (بات با توکن)

```python
class Bot:
    def __init__(self, token: str):
        self.methods = method_Rubika(tokenBot=token)
```

### تمام متدهای Bot با پارامترها
1. `@property def getMe(self):`
2. `def getUpdates(self, offset_id: str = None, limit: int = None):`
3. `def requestSendFile(self, type: str):`
4. `def getUpdate(self, filters):` (دکوراتور)
5. `def run(self):`
6. `def sendMessage(self, chat_id: str, text: str, chat_keypad_type: str = None, keypad: Optional[Dict[str, Any]] = None, notification: bool = False, inline_keypad: Optional[Dict[str, Any]] = None, reply_to_message_id: str = None, resize_keyboard: bool = True, on_time_keyboard: bool = False):`
7. `def sendPoll(self, chat_id: str, question: str, items: list[str]):`
8. `def sendLocation(self, chat_id: str, latitude: str, longitude: str, chat_keypad_type: str = None, keypad=None, notification="false", inline_keypad=None, resize_keyboard=True, on_time_keyboard=False, reply_to_message_id=None):`
9. `def sendContact(self, chat_id: str, first_name: str, last_name: str, phone_number: str, chat_keypad_type=None, keypad=None, notification="false", inline_keypad=None, resize_keyboard=True, on_time_keyboard=False, reply_to_message_id=None):`
10. `def getChat(self, chat_id: str):`
11. `def forwardMessage(self, chat_id: str, message_id: str, to_chat_id: str, notification: bool = False):`
12. `def editMessageText(self, chat_id: str, message_id: str, text: str):`
13. `def getChatAdmins(self, chat_id: str):`
14. `def getChatMembers(self, chat_id: str, start_id: str = ""):`
15. `def getChatInfo(self, chat_id: str):`
16. `def editChatTitle(self, chat_id: str, title: str):`
17. `def editChatDescription(self, chat_id: str, description: str):`
18. `def editChatPhoto(self, chat_id: str, file_id: str):`
19. `def addChatMembers(self, chat_id: str, member_ids: list[str]):`
20. `def banChatMember(self, chat_id: str, user_id: str):`
21. `def unbanChatMember(self, chat_id: str, member_id: str):`
22. `def restrictChatMember(self, chat_id: str, member_id: str, until_date: int = 0):`
23. `def getChatAdministrators(self, chat_id: str):`
24. `def getChatMemberCount(self, chat_id: str):`
25. `def promoteChatMember(self, chat_id: str, member_id: str, rights: dict = {}):`
26. `def pinChatMessage(self, chat_id: str, message_id: str):` (توجه: member_id اشتباه در برخی جاها)
27. `def unpinChatMessage(self, chat_id: str, message_id: str):`
28. `def exportChatInviteLink(self, chat_id: str):`
29. `def revokeChatInviteLink(self, chat_id: str, invite_link: str):`
30. `def editMessageKeypad(self, chat_id: str, message_id: str, inline_keypad=None, resize_keyboard=True, on_time_keyboard=False):`
31. `def deleteMessage(self, chat_id: str, message_id: str):`
32. `def setCommands(self, bot_commands: list[str]):`
33. `def updateBotEndpoints(self, url: str, TypeEndpoin: str):`
34. `def editChatKeypad(self, chat_id: str, chat_keypad_type: str = None, keypad=None, resize_keyboard=True, on_time_keyboard=False):`
35. `def getLinkDownload(self, file_id: str):`
36. `def sendFile(self, chat_id: str, file: str, caption=None, chat_keypad_type=None, reply_to_message_id=None, notification="false", keypad=None, inline_keypad=None, resize_keyboard=True, on_time_keyboard=False):`
37. `def sendImage(self, chat_id: str, file: str, caption=None, ...)` (همان پارامترهای بالا)
38. `def sendVoice(self, chat_id: str, file: str, caption=None, ...):`
39. `def sendVideo(self, chat_id: str, file: str, caption=None, ...):`
40. `def sendSticker(self, chat_id: str, sticker_id: str, notification=False):`
41. `def sendAudio(self, chat_id: str, audio_id: str, caption=None, notification=False):`
42. `def sendPhoto(self, chat_id: str, file_id: str, caption=None, notification=False):`

---

## ۳. کلاس Rubino (روبینو)

```python
class Rubino:
    def __init__(self, auth: str, Proxy: Optional[Union[str, List[str]]] = None):
```

### تمام متدهای Rubino با پارامترها
1. `def addPostVideo(self, addressfile: str, profile_id: str, caption: str, sizes: list[str] = ["1293", "1080"], thumbinline: str = None):`
2. `def addPostImage(self, addressfile: str, profile_id: str, caption: str, sizes: list[str] = None):`
3. `def addStoryVideo(self, addressfile: str, profile_id: str, sizes: list[str] = ["1280", "720"], thumbinline: str = None):`
4. `def addStoryImage(self, addressfile: str, profile_id: str, sizes: list[str] = None, thumbinline: str = None):`
5. `def likePostAction(self, post_id: str, post_profile_id: str, action_type: str, profile_id: str):`
6. `def getMyProfileInfo(self, profile_id: str):`
7. `def getProfileHighlights(self, target_profile_id: str, profile_id: str = None):`
8. `def getMyProfilePosts(self, limit, profile_id: str, max_id: str = None, sort: str = "FromMax"):`
9. `def updateProfile(self, profile_id: str, username: str = None, name: str = None, bio: str = None, email: str = None):`
10. `def private_page(self, profile_id: str, profile_status: str = None):`
11. `def getProfileList(self, limit: int, sort: str = "FromMax"):`
12. `def getNewEvents(self, profile_id: str, limit: int, sort: str = "FromMax"):`
13. `def getProfileInfo(self, target_profile_id: str, track_id: str = ""):`
14. `def getProfilePosts(self, limit: int, target_profile_id: str, profile_id: str, max_id: str = None, sort: str = "FromMax"):`
15. `def getRecentFollowingPosts(self, profile_id: str, limit: int, max_id: str, sort: str = "FromMax"):`
16. `def getProfilesStories(self, profile_id: str):`
17. `def sendRubinoPost(self, object_guid: str, post_id: str, post_profile_id: str):`
18. `def postBookmarkAction(self, post_id: str, post_profile_id: str, action_type: str, track_id: str = None):`
19. `def requestFollow(self, followee_id: str, f_type: str, post_track_id: str, profile_id: str):`
20. `def getComments(self, profile_id: str, post_id: str, post_profile_id: str, limit: int, min_id: Optional[Union[str, int]] = None, sort: str = "FromMax"):`
21. `def addComment(self, text: str, post_id: str, post_profile_id: str, profile_id: str):`
22. `def likeCommentAction(self, post_id: str, comment_id: str, action_type: str, profile_id: str, track_id: str):`
23. `def getPostLikes(self, profile_id: str, post_id: str, post_profile_id: str, limit: int, max_id: str = None, sort: str = "FromMax"):`
24. `def setReportRecord(self, model: str, reason: Optional[int], record_id: str, post_profile_id: str = None, profile_id: str = None):`
25. `def isExistUsername(self, username: str):`
26. `def getHighlightStoryIds(self, profile_id: str, target_profile_id: str, highlight_id: str, story_ids: list = None):`
27. `def getFollowers(self, profile_id: str, limit: int, target_profile_id: str, f_type: str, max_id: str = None, sort: str = "FromMax"):`
28. `def searchFollower(self, username: str, limit: int, search_type: str, target_profile_id: str, profile_id: str):`
29. `def getExplorePosts(self, profile_id: str, limit, max_id: str, topic_id: str = None, sort: str = "FromMax"):`
30. `def getRelatedExplorePost(self, profile_id: str, post_id: str, post_profile_id: str, limit: int, track_id: str, start_id: str = None):`
31. `def getStory(self, profile_id: str, story_profile_id: str, story_ids: list):`
32. `def getStoryIds(self, profile_id: str, target_profile_id: str):`
33. `def getSuggested(self, profile_id: str, limit: int, max_id: str, sort: str = "FromMax"):`
34. `def searchProfile(self, username: str, limit: str, profile_id: str):`
35. `def getHashTagTrend(self, limit: int, profile_id: str):`
36. `def searchHashTag(self, text: str, limit: int, profile_id: str):`
37. `def getPostsByHashTag(self, text: str, start_id: str = None):`
38. `def getTaggedPosts(self, target_profile_id: str, profile_id: str, start_id: str = None):`
39. `def getExplorePostTopics(self, profile_id: str):`
40. `def create_page(self, username: str, name: str, bio: str = None, phone: str = None, email: str = None, website: str = None):`
41. `def unblock_page(self, target_profile_id: str, profile_id: str):`
42. `def block_page(self, target_profile_id: str, profile_id: str):`
43. `def getInfoPost(self, url: str, profile_id: str):`
(و بقیه متدهای بلوک/فالوور/استوری و ... کامل در فایل اصلی)

---

**نحوه استفاده سریع:**

```python
from arsein.Arsein import Messenger, Bot, Rubino

# Messenger (UserBot)
bot = Messenger(Sh_account="...", keyAccount="...")

# Bot (بات رسمی)
b = Bot(token="BOT_TOKEN")

# Rubino
rub = Rubino(auth="...")
rub.addPostImage("photo.jpg", profile_id="...", caption="سلام!")
```
