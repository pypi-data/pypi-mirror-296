from __future__ import annotations

from abc import ABC

from pydantic import BaseModel, ConfigDict, Field, SkipValidation

from botops.telegram.enums import ChatTypeEnum, EntityTypeEnum, PollTypeEnum

__all__ = [
    "Update",
    "User",
    "Message",
    "CallbackQuery",
    "InlineQuery",
    "ReplyKeyboardRemove",
    "InlineKeyboardMarkup",
    "ForceReply",
    "MessageEntity",
    "ReplyKeyboardMarkup",
    "ChosenInlineResult",
    "ShippingQuery",
    "PreCheckoutQuery",
    "Poll",
    "PollAnswer",
    "ChatJoinRequest",
    "ChatMemberUpdated",
    "TelegramType",
    "TelegramResponse",
]


class TelegramType(BaseModel, ABC):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, use_enum_values=True, revalidate_instances="never"
    )


class TelegramResponse[R](TelegramType):
    ok: SkipValidation[bool] = Field()
    result: R | None = Field(None)
    error_code: SkipValidation[int] | None = Field(None)
    description: SkipValidation[str] | None = Field(None)
    parameters: SkipValidation[dict] | None = Field(None)


class User(TelegramType):
    id: int = Field()
    is_bot: bool = Field()
    first_name: str = Field()
    last_name: str | None = Field(None)
    username: str | None = Field(None)
    language_code: str | None = Field(None)
    is_premium: bool | None = Field(None)
    added_to_attachment_menu: bool | None = Field(None)
    can_join_groups: bool | None = Field(None)
    can_read_all_group_messages: bool | None = Field(None)
    supports_inline_queries: bool | None = Field(None)


class Chat(TelegramType):
    id: int = Field()
    type: ChatTypeEnum = Field()
    title: str | None = Field(None)
    username: str | None = Field(None)
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    is_forum: bool | None = Field(None)
    photo: ChatPhoto | None = Field(None)
    active_usernames: list[str] | None = Field(None)
    emoji_status_custom_emoji_id: str | None = Field(None)
    emoji_status_expiration_date: int | None = Field(None)
    bio: str | None = Field(None)
    has_private_forwards: bool | None = Field(None)
    has_restricted_voice_and_video_messages: bool | None = Field(None)
    join_to_send_messages: bool | None = Field(None)
    join_by_request: bool | None = Field(None)
    description: str | None = Field(None)
    invite_link: str | None = Field(None)
    pinned_message: Message | None = Field(None)
    permissions: ChatPermissions | None = Field(None)
    slow_mode_delay: int | None = Field(None)
    message_auto_delete_time: int | None = Field(None)
    has_aggressive_anti_spam_enabled: bool | None = Field(None)
    has_hidden_members: bool | None = Field(None)
    has_protected_content: bool | None = Field(None)
    sticker_set_name: str | None = Field(None)
    can_set_sticker_set: bool | None = Field(None)
    linked_chat_id: int | None = Field(None)
    location: ChatLocation | None = Field(None)


class Message(TelegramType):
    message_id: int = Field()
    message_thread_id: int | None = Field(None)
    from_user: User = Field(..., alias="from")
    sender_chat: Chat | None = Field(None)
    date: int = Field()
    chat: Chat = Field()
    forward_from: User | None = Field(None)
    forward_from_chat: Chat | None = Field(None)
    forward_from_message_id: int | None = Field(None)
    forward_signature: str | None = Field(None)
    forward_sender_name: str | None = Field(None)
    forward_date: int | None = Field(None)
    is_topic_message: bool | None = Field(None)
    is_automatic_forward: bool | None = Field(None)
    reply_to_message: Message | None = Field(None)
    via_bot: User | None = Field(None)
    edit_date: int | None = Field(None)
    has_protected_content: bool | None = Field(None)
    media_group_id: str | None = Field(None)
    author_signature: str | None = Field(None)
    text: str | None = Field(None)
    entities: list[MessageEntity] | None = Field(None)
    animation: Animation | None = Field(None)
    audio: Audio | None = Field(None)
    document: Document | None = Field(None)
    photo: list[PhotoSize] | None = Field(None)
    sticker: Sticker | None = Field(None)
    story: Story | None = Field(None)
    video: Video | None = Field(None)
    video_note: VideoNote | None = Field(None)
    voice: Voice | None = Field(None)
    caption: str | None = Field(None)
    caption_entities: list[MessageEntity] | None = Field(None)
    has_media_spoiler: bool | None = Field(None)
    contact: Contact | None = Field(None)
    dice: Dice | None = Field(None)
    game: Game | None = Field(None)
    poll: Poll | None = Field(None)
    venue: Venue | None = Field(None)
    location: Location | None = Field(None)
    new_chat_members: list[User] | None = Field(None)
    left_chat_member: User | None = Field(None)
    new_chat_title: str | None = Field(None)
    new_chat_photo: list[PhotoSize] | None = Field(None)
    delete_chat_photo: bool | None = Field(None)
    group_chat_created: bool | None = Field(None)
    supergroup_chat_created: bool | None = Field(None)
    channel_chat_created: bool | None = Field(None)
    message_auto_delete_timer_changed: MessageAutoDeleteTimerChanged | None = Field(None)
    migrate_to_chat_id: int | None = Field(None)
    migrate_from_chat_id: int | None = Field(None)
    pinned_message: Message | None = Field(None)
    invoice: Invoice | None = Field(None)
    successful_payment: SuccessfulPayment | None = Field(None)
    user_shared: UserShared | None = Field(None)
    chat_shared: ChatShared | None = Field(None)
    connected_website: str | None = Field(None)
    write_access_allowed: WriteAccessAllowed | None = Field(None)
    passport_data: PassportData | None = Field(None)
    proximity_alert_triggered: ProximityAlertTriggered | None = Field(None)
    forum_topic_created: ForumTopicCreated | None = Field(None)
    forum_topic_edited: ForumTopicEdited | None = Field(None)
    forum_topic_closed: ForumTopicClosed | None = Field(None)
    forum_topic_reopened: ForumTopicReopened | None = Field(None)
    general_forum_topic_hidden: GeneralForumTopicHidden | None = Field(None)
    general_forum_topic_unhidden: GeneralForumTopicUnhidden | None = Field(None)
    video_chat_scheduled: VideoChatScheduled | None = Field(None)
    video_chat_started: VideoChatStarted | None = Field(None)
    video_chat_ended: VideoChatEnded | None = Field(None)
    video_chat_participants_invited: VideoChatParticipantsInvited | None = Field(None)
    web_app_data: WebAppData | None = Field(None)
    reply_markup: InlineKeyboardMarkup | None = Field(None)


class MessageId(TelegramType):
    message_id: int = Field()


class MessageEntity(TelegramType):
    type: EntityTypeEnum = Field()
    offset: int = Field()
    length: int = Field()
    url: str | None = Field(None)
    user: User | None = Field(None)
    language: str | None = Field(None)
    custom_emoji_id: str | None = Field(None)


class PhotoSize(TelegramType):
    file_id: str = Field()
    file_unique_id: str = Field()
    width: int = Field()
    height: int = Field()
    file_size: int | None = Field(None)


class Animation(TelegramType):
    file_id: str = Field()
    file_unique_id: str = Field()
    width: int = Field()
    height: int = Field()
    duration: int = Field()
    thumbnail: PhotoSize | None = Field(None)
    file_name: str | None = Field(None)
    mime_type: str | None = Field(None)
    file_size: int | None = Field(None)


class Audio(TelegramType):
    file_id: str = Field()
    file_unique_id: str = Field()
    duration: int = Field()
    performer: str | None = Field(None)
    title: str | None = Field(None)
    file_name: str | None = Field(None)
    mime_type: str | None = Field(None)
    file_size: int | None = Field(None)
    thumbnail: PhotoSize | None = Field(None)


class Document(TelegramType):
    file_id: str = Field()
    file_unique_id: str = Field()
    thumbnail: PhotoSize | None = Field(None)
    file_name: str | None = Field(None)
    mime_type: str | None = Field(None)
    file_size: int | None = Field(None)


class Story(TelegramType): ...


class Video(TelegramType):
    file_id: str = Field()
    file_unique_id: str = Field()
    width: int = Field()
    height: int = Field()
    duration: int = Field()
    thumbnail: PhotoSize | None = Field(None)
    file_name: str | None = Field(None)
    mime_type: str | None = Field(None)
    file_size: int | None = Field(None)


class VideoNote(TelegramType):
    file_id: str = Field()
    file_unique_id: str = Field()
    length: int = Field()
    duration: int = Field()
    thumbnail: PhotoSize | None = Field(None)
    file_size: int | None = Field(None)


class Voice(TelegramType):
    file_id: str = Field()
    file_unique_id: str = Field()
    duration: int = Field()
    mime_type: str | None = Field(None)
    file_size: int | None = Field(None)


class Contact(TelegramType):
    phone_number: str = Field()
    first_name: str = Field()
    last_name: str | None = Field(None)
    user_id: int | None = Field(None)
    vcard: str | None = Field(None)


class Dice(TelegramType):
    emoji: str = Field()
    value: int = Field()


class PollOption(TelegramType):
    text: str = Field()
    voter_count: int = Field()


class PollAnswer(TelegramType):
    poll_id: str = Field()
    voter_chat: Chat | None = Field(None)
    user: User | None = Field(None)
    option_ids: list[int] = Field()


class Poll(TelegramType):
    id: str = Field()
    question: str = Field()
    options: list[PollOption] = Field()
    total_voter_count: int = Field()
    is_closed: bool = Field()
    is_anonymous: bool = Field()
    type: PollTypeEnum = Field()
    allows_multiple_answers: bool = Field()
    correct_option_id: int | None = Field(None)
    explanation: str | None = Field(None)
    explanation_entities: list[MessageEntity] | None = Field(None)
    open_period: int | None = Field(None)
    close_date: int | None = Field(None)


class Location(TelegramType):
    longitude: float = Field()
    latitude: float = Field()
    horizontal_accuracy: float | None = Field(None)
    live_period: int | None = Field(None)
    heading: int | None = Field(None)
    proximity_alert_radius: int | None = Field(None)


class Venue(TelegramType):
    location: Location = Field()
    title: str = Field()
    address: str = Field()
    foursquare_id: str | None = Field(None)
    foursquare_type: str | None = Field(None)
    google_place_id: str | None = Field(None)
    google_place_type: str | None = Field(None)


class WebAppData(TelegramType):
    data: str = Field()
    button_text: str = Field()


class ProximityAlertTriggered(TelegramType): ...


class MessageAutoDeleteTimerChanged(TelegramType): ...


class ForumTopicCreated(TelegramType): ...


class ForumTopicClosed(TelegramType): ...


class ForumTopicReopened(TelegramType): ...


class GeneralForumTopicHidden(TelegramType): ...


class UserShared(TelegramType): ...


class ChatShared(TelegramType): ...


class WriteAccessAllowed(TelegramType): ...


class VideoChatScheduled(TelegramType): ...


class VideoChatStarted(TelegramType): ...


class VideoChatEnded(TelegramType): ...


class VideoChatParticipantsInvited(TelegramType): ...


class UserProfilePhotos(TelegramType): ...


class File(TelegramType): ...


class ChatPhoto(TelegramType):
    small_file_id: str = Field()
    small_file_unique_id: str = Field()
    big_file_id: str = Field()
    big_file_unique_id: str = Field()


class ChatPermissions(TelegramType):
    can_send_messages: bool | None = Field(None)
    can_send_audios: bool | None = Field(None)
    can_send_documents: bool | None = Field(None)
    can_send_photos: bool | None = Field(None)
    can_send_videos: bool | None = Field(None)
    can_send_video_notes: bool | None = Field(None)
    can_send_voice_notes: bool | None = Field(None)
    can_send_polls: bool | None = Field(None)
    can_send_other_messages: bool | None = Field(None)
    can_add_web_page_previews: bool | None = Field(None)
    can_change_info: bool | None = Field(None)
    can_invite_users: bool | None = Field(None)
    can_pin_messages: bool | None = Field(None)
    can_manage_topics: bool | None = Field(None)


class ChatLocation(TelegramType):
    location: Location = Field()
    address: str = Field()


class Sticker(TelegramType): ...


class Game(TelegramType): ...


class SuccessfulPayment(TelegramType): ...


class PassportData(TelegramType): ...


class ForumTopicEdited(TelegramType): ...


class GeneralForumTopicUnhidden(TelegramType): ...


class InlineKeyboardMarkup(TelegramType): ...


class ReplyKeyboardMarkup(TelegramType): ...


class ReplyKeyboardRemove(TelegramType): ...


class ForceReply(TelegramType): ...


class InlineQuery(TelegramType): ...


class ChosenInlineResult(TelegramType): ...


class CallbackQuery(TelegramType): ...


class ShippingQuery(TelegramType): ...


class PreCheckoutQuery(TelegramType): ...


class ChatMemberUpdated(TelegramType): ...


class ChatJoinRequest(TelegramType): ...


class Invoice(TelegramType):
    title: str = Field()
    description: str = Field()
    start_parameter: str = Field()
    currency: str = Field()
    total_amount: float = Field()


class Update(TelegramType):
    update_id: int = Field()
    message: Message | None = Field(None)
    edited_message: Message | None = Field(None)
    channel_post: Message | None = Field(None)
    edited_channel_post: Message | None = Field(None)
    inline_query: InlineQuery | None = Field(None)
    chosen_inline_result: ChosenInlineResult | None = Field(None)
    callback_query: CallbackQuery | None = Field(None)
    shipping_query: ShippingQuery | None = Field(None)
    pre_checkout_query: PreCheckoutQuery | None = Field(None)
    poll: Poll | None = Field(None)
    poll_answer: PollAnswer | None = Field(None)
    my_chat_member: ChatMemberUpdated | None = Field(None)
    chat_member: ChatMemberUpdated | None = Field(None)
    chat_join_request: ChatJoinRequest | None = Field(None)

    @property
    def offset(self) -> int:
        return self.update_id + 1
