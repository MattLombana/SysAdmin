#! /bin/bash

# Slack SSH-Notification script
# A simple script to notify Slack when someone Logs into my laptop
# Original Source: http://redgreenrepeat.com/2017/03/10/configuring-mail-and-slack-for-ssh-notifications/

# To use this script, copy it to the target machine and run the following command
# sudo defaults write com.apple.loginwindow LoginHook <absolute path to this script>

# First, ensure that this is a login event:

################################################################################
#                              Begin Message Vars                              #
################################################################################
# Global Slack Settings
SLACK_URL="https://hooks.slack.com/services/CHANGEME"
CHANNEL="#ssh-notifications"
USERNAME="Login-Bot"

# Message Content Settings
# Title
MESSAGE_TITLE="*login on* \``hostname`\` *for account* \`$1\`"

# Body
USER="User:            $1"
CURRENT_IP="Local Host IP:   `ifconfig | grep 'inet ' | grep -v 127.0.0.1 | cut -d ' ' -f 2`"
DATE="Date:            `date`"
SERVER="Server:          `uname -a`"
MESSAGE_BODY="\`\`\`${USER}\n${CURRENT_IP}\n${DATE}\n${SERVER}\`\`\`"

# Level
MESSAGE_LEVEL="WARNING"
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
