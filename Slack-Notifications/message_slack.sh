#! /bin/bash

# Slack Notification script: A simple script to notify Slack
# Original Source: http://redgreenrepeat.com/2017/03/10/configuring-mail-and-slack-for-ssh-notifications/


################################################################################
#                              Begin Message Vars                              #
################################################################################
# Global Slack Settings
# Define in an environment variable, or set here:
SLACK_URL="https://hooks.slack.com/services/CHANGEME"
CHANNEL="#general"
USERNAME="Example-Bot"

# Message Content Settings
# Title
SERVICE="Example Service"
MESSAGE_TITLE="*Example message from* \`${SERVICE}\` *on* \``hostname -s`\`"

# Body
DATE="Date:            `date`"
SERVER="Server:          `uname -a`"
HOST="Host:            `hostname -s`"
MESSAGE_BODY="\`\`\`${DATE}\n${SERVER}\n${HOST}\`\`\`"

# Level
MESSAGE_LEVEL="INFO"
################################################################################
#                               End Message Vars                               #
################################################################################


SLACK_MESSAGE="${MESSAGE_TITLE}\n\n${MESSAGE_BODY}"

case "$MESSAGE_LEVEL" in
    INFO)
        SLACK_ICON=':slack:'
        ;;
    WARNING)
        SLACK_ICON=':warning:'
        ;;
    ERROR)
        SLACK_ICON=':bangbang:'
        ;;
    *)
        SLACK_ICON=':slack:'
        ;;
esac

curl -X POST --data "payload={\"channel\": \"${CHANNEL}\", \"username\": \"${USERNAME}\", \"text\": \"${SLACK_ICON} ${SLACK_MESSAGE}\", \"icon_emoji\": \"${SLACK_ICON}\"}" ${SLACK_URL}

exit 0
