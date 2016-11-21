"""Settings for the bot."""

CRAIGSLIST_SITE = "washingtondc"

QUERY = "unicycle"

# Get tokens from: https://api.slack.com/docs/oauth-test-tokens
# SLACK_TOKEN = "REDACTED"

SLACK_CHANNEL = "#forsale"

BOTNAME = "craigslist_bot"

# Any private settings are imported here. (SLACK_TOKEN)
try:
    from private import *
except Exception:
    pass
