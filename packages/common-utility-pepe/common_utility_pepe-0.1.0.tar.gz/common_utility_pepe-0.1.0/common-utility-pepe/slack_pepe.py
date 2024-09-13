from typing import Optional
import requests
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackPepe:
    """
    Slack 메시지를 보내고 업데이트하는 페페
    Pepe for sending and updating Slack messages
    """

    def __init__(self, webhook_url: Optional[str] = None, channel: Optional[str] = None, bot_token: Optional[str] = None) -> None:
        """
        SlackPepe 클래스의 생성자입니다.
        Constructor for the SlackPepe class.

        :param webhook_url: Slack 웹훅 URL (선택적) / Slack webhook URL (optional)
        :param channel: Slack 채널 ID (선택적) / Slack channel ID (optional)
        :param bot_token: Slack 봇 토큰 (선택적) / Slack bot token (optional)
        """
        self.webhook_url = webhook_url
        self.channel = channel
        self.bot_token = bot_token

        if not (webhook_url or (channel and bot_token)):
            raise ValueError("webhook_url 또는 (channel과 bot_token)을 제공해야 합니다. / You must provide either webhook_url or (channel and bot_token).")

    @classmethod
    def from_webhook(cls, webhook_url: str) -> "SlackPepe":
        """
        웹훅 URL을 사용하여 SlackPepe 인스턴스를 생성합니다.
        Creates a SlackPepe instance using a webhook URL.

        :param webhook_url: Slack 웹훅 URL / Slack webhook URL
        :return: SlackPepe 인스턴스 / SlackPepe instance
        """
        return cls(webhook_url=webhook_url)

    @classmethod
    def from_bot(cls, channel: str, bot_token: str) -> "SlackPepe":
        """
        채널 ID와 봇 토큰을 사용하여 SlackPepe 인스턴스를 생성합니다.
        Creates a SlackPepe instance using a channel ID and bot token.

        :param channel: Slack 채널 ID / Slack channel ID
        :param bot_token: Slack 봇 토큰 / Slack bot token
        :return: SlackPepe 인스턴스 / SlackPepe instance
        """
        return cls(channel=channel, bot_token=bot_token)

    # 나머지 메서드들은 그대로 유지...
    # Other methods remain unchanged...

    def update_slack_message(self, timestamp: str, title: str,):
        """
        슬랙메시지 갱신 메서드
        Method to update Slack message

        Args:
            timestamp (str): send_slack_message 메서드에서 반환된 타임스탬프 / Timestamp returned from send_slack_message method
            title (str): 메시지 제목 / Message title

        Raises:
            ValueError: 웹훅 URL 또는 (채널 ID와 봇 토큰)을 제공해야 합니다. / You must provide either webhook URL or (channel ID and bot token).
            ValueError: 웹훅 요청 중 오류 발생: {response.status_code}, 응답: {response.text} / Error occurred during webhook request: {response.status_code}, response: {response.text}
            ValueError: webhook은 메시지 업데이트를 지원하지않습니다. 봇을 생성하여 채널아이디와 봇 토큰을 주입해주세요 / Webhook does not support message updates. Please create a bot and inject channel ID and bot token.
        """
        if self.webhook_url and self.channel == None and self.botToken == None:
            raise ValueError(
                "webhook은 메시지 업데이트를 지원하지않습니다. 봇을 생성하여 채널아이디와 봇 토큰을 주입해주세요 / Webhook does not support message updates. Please create a bot and inject channel ID and bot token.")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.bot_token}"
        }
        message = f"*{title}*"
        data = {
            "channel": self.channel,
            "ts": timestamp,
            "text": message
        }
        response = requests.post(
            "https://slack.com/api/chat.update", headers=headers, json=data)
        if response.status_code != 200:
            raise ValueError(
                f"Request to slack returned an error {response.status_code}, the response is:\n{response.text}")


    def send_slack_message(self, title="", content:str=None, detail:str=None) -> str | None:
        """
        슬랙 메시지 전송 함수
        Function to send Slack message

        웹훅 사용시 timestamp 반환 *안함*
        봇 토큰과 채널명 사용시에만 timestamp *반환*
        Does *not* return timestamp when using webhook
        *Returns* timestamp only when using bot token and channel name

        Args:
            title (str, optional): 제목 / Title. Defaults to "".
            content (str, optional): 내용 / Content. Defaults to None.
            detail (str, optional): 상세내용 / Detailed content. Defaults to None.

        Raises:
            ValueError: 웹훅 URL 또는 (채널 ID와 봇 토큰)을 제공해야 합니다. / You must provide either webhook URL or (channel ID and bot token).
            ValueError: 웹훅 요청 중 오류 발생: {response.status_code}, 응답: {response.text} / Error occurred during webhook request: {response.status_code}, response: {response.text}
            ValueError: Slack API 오류 발생: {e} / Slack API error occurred: {e}

        Returns:
            str: timestamp optional
        """
        content = content or ""
        detail = detail or ""

        text = f"{title}\n{content}\n{detail}".strip()  # 텍스트 버전 메시지 생성 / Create text version of message

        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{title}*\n{content}"
                }
            }
        ]

        if detail:
            blocks.append({
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"{detail}"
                    }
                ]
            })

        if self.webhook_url:
            # 웹훅 사용 시 코드는 그대로 유지 / Code remains unchanged when using webhook
            headers = {"Content-Type": "application/json"}
            data = {"blocks": blocks, "text": text}  # text 추가 / Add text
            response = requests.post(
                self.webhook_url, headers=headers, data=json.dumps(data))
            if response.status_code != 200:
                raise ValueError(
                    f"웹훅 요청 중 오류 발생: {response.status_code}, 응답: {response.text} / Error occurred during webhook request: {response.status_code}, response: {response.text}")
        elif self.channel and self.bot_token:
            try:
                client = WebClient(token=self.bot_token)
                response = client.chat_postMessage(
                    channel=self.channel,
                    blocks=blocks,
                    text=text  # text 파라미터 추가 / Add text parameter
                )
                return response["ts"]
            except SlackApiError as e:
                print(f"Slack API 오류 발생: {e} / Slack API error occurred: {e}")
                return None
        else:
            raise ValueError("웹훅 URL 또는 (채널 ID와 봇 토큰)을 제공해야 합니다. / You must provide either webhook URL or (channel ID and bot token).")