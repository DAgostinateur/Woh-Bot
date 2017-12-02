class UserBD(list):
    """A UserBD is made of a user and their birthday date."""

    def __init__(self, user_id, bd):
        """Keyword arguments:
        user_id -- user ID, Format: 000000000000000000
        bd      -- birthday date, Format: mm-dd"""
        super().__init__()
        self.bd = bd
        self.userId = user_id


class ChannelBD(list):
    """A ChannelBD is made of a channel id and a server id."""

    def __init__(self, channel_id, server_id):
        """Keyword arguments:
        channel_id -- channel ID, Format: 000000000000000000
        server_id  -- server ID,  Format: 000000000000000000"""
        super().__init__()
        self.serverId = server_id
        self.channelId = channel_id


class AdminUser(list):  # Will be used in the future
    """An AdminUser is made of a user id and a server id."""

    def __init__(self, user_id, server_id):
        """Keyword arguments:
        user_id    -- user ID,   Format: 000000000000000000
        server_id  -- server ID, Format: 000000000000000000"""
        super().__init__()
        self.userId = user_id
        self.serverId = server_id
