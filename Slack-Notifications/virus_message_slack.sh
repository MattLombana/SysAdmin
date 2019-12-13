#! /bin/bash

# Slack Notification script

# A simple script to notify Slack
# Original Source: http://redgreenrepeat.com/2017/03/10/configuring-mail-and-slack-for-ssh-notifications/


################################################################################
#                              Begin Message Vars                              #
################################################################################
# Global Slack Settings
SLACK_URL="https://hooks.slack.com/services/CHANGEME"
CHANNEL="#virus-alerts"
USERNAME="Virus-Bot"

# Message Content Settings
# Title
SERVICE="ClamAV"
MESSAGE_TITLE="*New virus event from* \`${SERVICE}\` *on* \``hostname -s`\`"

# Body
           DATE="Date:             `date`"
           HOST="Host:             `hostname -s`"
         SERVER="Server:           `uname -a`"
     VIRUS_NAME="Virus Name:       $1"
 VIRUS_FILENAME="CLAMAV Filename:  $2"
VIRUS_VIRUSNAME="CLAMAV VirusName: $3"
MESSAGE_BODY="\`\`\`${DATE}\n${HOST}\n${SERVER}\n${VIRUS_NAME}\n${VIRUS_FILENAME}\n${VIRUS_VIRUSNAME}\n\`\`\`"

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
