#! /bin/bash


# Slack SSH-Notification script
# A simple script to notify Slack when someone SSH's into a server
# Original Source: http://redgreenrepeat.com/2017/03/10/configuring-mail-and-slack-for-ssh-notifications/

# To use this script, copy it to the target machine, and add the following line to /etc/pam.d/sshd
#  # on any activity, execute ssh_message_slack.sh
#  session   optional      pam_exec.so /absolute/path/to/ssh_message_slack.sh

# First, ensure that this is a login event:
if [[ "$PAM_TYPE" != "open_session"  ]]; then
    exit 0
fi

################################################################################
#                              Begin Message Vars                              #
################################################################################
# Global Slack Settings
SLACK_URL="https://hooks.slack.com/services/CHANGEME"
CHANNEL="#ssh-notifications"
USERNAME="Login-Bot"

# Message Content Settings
# Title
MESSAGE_TITLE="*${PAM_SERVICE} login on* \``hostname -s`\` *for account* \`${PAM_USER}\`"

# Body
USER="User:            $PAM_USER"
REMOTE="Remote host:     $PAM_RHOST"
SERVICE="Service:         $PAM_SERVICE"
TTY="TTY:             $PAM_TTY"
DATE="Date:            `date`"
SERVER="Server:          `uname -a`"
MESSAGE_BODY="\`\`\`${USER}\n${REMOTE}\n${SERVICE}\n${TTY}\n${DATE}\n${SERVER}\`\`\`"

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
