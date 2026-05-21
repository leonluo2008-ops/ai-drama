#!/usr/bin/env python3
"""
feishu_send.py - 飞书消息发送
"""
import sys
import subprocess

def send(message: str, chat_id: str = "oc_7ccd8484af704222aa5705ec6496aaa7"):
    try:
        from hermes_tools import terminal
        # 用 lark-cli 发消息
        result = terminal(
            f'lark-cli im message send --chat-id {chat_id} --msg-type text --content "\\"{message}\\""'
        )
        print(result)
    except Exception as e:
        print(f"发送失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python feishu_send.py --message '消息内容'")
        sys.exit(1)

    msg = sys.argv[1]
    if msg == "--message" and len(sys.argv) >= 3:
        msg = sys.argv[2]

    send(msg)
