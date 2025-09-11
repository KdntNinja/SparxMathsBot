"""Email notification service for SparxMathsBot."""

import os

import resend


class EmailNotifier:
    """Handles email notifications."""

    def __init__(self):
        """Initialize email service with API key."""
        resend.api_key = os.getenv("RESEND_API_KEY")
        self.sender_email = "SparxMathsBot@resend.dev"
        self.recipient_email = os.getenv("RESEND_TO")

    def send_completion_notification(self, log_file: str = "workflow_log.txt") -> None:
        """Send email notification when workflow completes."""
        try:
            with open(log_file, "r") as f:
                log_content = "".join(reversed(f.readlines()))

            resend.Emails.send(
                {
                    "from": self.sender_email,
                    "to": self.recipient_email,
                    "subject": "SparxMathsBot Finished",
                    "html": f"<p>SparxMathsBot Run <strong>Finished</strong>!</p><pre>{log_content}</pre>",
                }
            )
        except Exception as e:
            print(f"Failed to send email notification: {e}")
