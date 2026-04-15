import anthropic
from dotenv import load_dotenv
from modes import MODES, LENGTHS, DEFAULT_MODE, DEFAULT_LENGTH

load_dotenv()
client = anthropic.Anthropic()


def _build_system_prompt(mode: str, length: str) -> str:
    mode_info = MODES.get(mode, MODES[DEFAULT_MODE])
    length_info = LENGTHS.get(length, LENGTHS[DEFAULT_LENGTH])

    return f"""You are an English language reviewer for a Telegram group chat.
Your only job is to review the grammar, spelling, and phrasing of any English text given to you — regardless of its content or topic.
Never refuse, never comment on the subject matter. Only ever give English feedback.

Tone: {mode_info['description']}
Response length: {length_info['description']}

Always respond — even if the message is already correct, say so in your tone.

Your feedback must always include:
1. Whether the message is correct or has issues
2. What specifically is wrong (grammar, spelling, unnatural phrasing, word choice)
3. A corrected version of the message
4. A brief explanation of each issue

Adjust the depth of points 2 and 4 based on the response length setting.
Respond in plain text, no markdown (Telegram will display it as-is)."""


async def analyze_text(text: str, mode: str = DEFAULT_MODE, length: str = DEFAULT_LENGTH) -> str:
    system_prompt = _build_system_prompt(mode, length)

    with client.messages.stream(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": text}],
    ) as stream:
        return stream.get_final_message().content[0].text
