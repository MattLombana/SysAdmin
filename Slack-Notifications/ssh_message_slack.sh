#! /bin/bash

# Slack SSH-Notification script

# A simple script to notify Slack when someone SSH's into a server
# Original Source: http://redgreenrepeat.com/2017/03/10/configuring-mail-and-slack-for-ssh-notifications/

# To use this script, copy it to the target machine, and add the following line to /etc/pam.d/sshd
#  # on any activity, execute ssh_message_slack.sh
#  session   optional      pam_exec.so /absolute/path/to/ssh_message_slack.sh

function post_to_slack () {
	TITLE="$1"
	MESSAGE="$2"
	MESSAGE_LEVEL="$3"

    SLACK_MESSAGE="${TITLE}\n\`\`\`${MESSAGE}\`\`\`"
    SLACK_URL="https://hooks.slack.com/services/CHANGEME"

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

    curl -X POST --data "payload={\"text\": \"${SLACK_ICON} ${SLACK_MESSAGE}\", \"username\": \"login-bot\", \"icon_emoji\": \"${SLACK_ICON}\"}" ${SLACK_URL}
}

LOGINMESSAGE="*${PAM_SERVICE} login on* \``hostname -s`\` *for account* \`${PAM_USER}\`"
USER="User:            $PAM_USER"
REMOTE="Remote host:     $PAM_RHOST"
SERVICE="Service:         $PAM_SERVICE"
TTY="TTY:             $PAM_TTY"
DATE="Date:            `date`"
SERVER="Server:          `uname -a`"

if [[ "$PAM_TYPE" = "open_session" ]]; then
    post_to_slack "${LOGINMESSAGE}" "${USER}\n${REMOTE}\n${SERVICE}\n${TTY}\n${DATE}\n${SERVER}" "INFO"
fi

exit 0
