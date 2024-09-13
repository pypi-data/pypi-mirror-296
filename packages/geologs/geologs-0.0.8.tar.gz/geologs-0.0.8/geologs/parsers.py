# -*- coding: utf-8 -*-
"""
Created on Sat Sep 07 20:14 2024

Simple parsers to make the log files look pretty.

@author: james
"""


def _log_level_to_emoji(level: str) -> str:
    """Conver the log level to an emoji"""
    l = level.lower().strip()
    if l == "debug":
        return ":bug: "
    elif l == "info":
        return ":mag: "
    elif l == "warning" or l == "warn":
        return ":warning: "
    elif l == "error":
        return ":x: "
    else:
        return ":grey_question: "


def basic(message: str) -> str:
    """Do nothing"""
    return message


def monty(message: str) -> str:
    """Parse message output from monty"""
    comps = message.split(" ")
    if len(comps) < 4:
        return message  # corrupted format
    if "start" in message.lower():
        return _log_level_to_emoji(comps[2]) + ":large_green_circle: " + " ".join(comps[3:])
    elif "end" in message.lower() or "finish" in message.lower():
        return _log_level_to_emoji(comps[2]) + ":octagonal_sign: " + " ".join(comps[3:])
    else:
        return _log_level_to_emoji(comps[2]) + " ".join(comps[3:])


def ssh(message: str) -> str:
    """Parse message from sshd."""
    comps = message.split(" ")
    if "accepted publickey" in message.lower():
        # Confirmation of public key
        return ":key: " + " ".join(comps[5:13])
    elif "session opened" in message.lower():
        # Creation of a new session
        return ":satellite_antenna: " + " ".join(comps[5:])
    else:
        return message



PARSERS = {
    "basic": basic,
    "monty": monty,
    "ssh": ssh,
}


if __name__ == "__main__":
    print(monty("[2024-09-10 11:28:44,276] INFO Run finished and took 3 seconds"))
    print(ssh("Sep 13 06:17:24 hostname sshd[281443]: Accepted publickey for user from 1.1.1.1 port 22 ssh2: RSA SHA256:HASH"))
    print(ssh("Sep 13 06:17:24 hostname sshd[281443]: pam_unix(sshd:session): session opened for user user(uid=1001) by (uid=0)"))
