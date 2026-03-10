class AntiSpamState:
    def __init__(self):
        self.enabled = True
        self.whitelist_users = set()
        self.whitelist_roles = set()
        self.whitelist_channels = set()

    def is_whitelisted(self, message):
        if message.author.id in self.whitelist_users:
            return True

        if message.channel.id in self.whitelist_channels:
            return True

        if any(role.id in self.whitelist_roles for role in message.author.roles):
            return True

        return False


antispam_state = AntiSpamState()