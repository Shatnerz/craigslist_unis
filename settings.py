"""Settings for the bot."""

CRAIGSLIST_SITE = "washingtondc"

QUERY = "unicycle"

# Get tokens from: https://api.slack.com/docs/oauth-test-tokens
# SLACK_TOKEN = "REDACTED"

SLACK_CHANNEL = "#forsale"

BOTNAME = "craigslist_bot"

SLEEP_INTERVAL = 20 * 60  # 20 minutes

# Any private settings are imported here. (SLACK_TOKEN)
try:
    from private import *
except Exception:
    pass
