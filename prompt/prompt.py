import random, os

class Prompt:
    def __init__(self):
        self.prompt_path = os.path.join(os.path.dirname(__file__), "prompt.txt")

    def get_intro_text(self):
        filename = os.path.join(os.path.dirname(__file__), "info.txt")
        with open(filename, 'r') as file:
            return file.read().strip()

    def get_prompt(self):
        with open(self.prompt_path) as file:
            self.base_prompt = file.read().strip()
        tones = ["urgent", "emotional", "calm but serious", "formal", "compassionate"]
        prompt = self.base_prompt + 'Each message must have a completely different *opening line* that does not resemble the structure or language of previous letters. Do not begin with “I am writing to you today with a heavy heart…” or anything close. Instead, vary tone, entry point, and sentence structure creatively while remaining appropriate and respectful.'
        prompt += f'Tone: {random.choice(tones)}'
        prompt += 'Please generate an email subject line (start with "Subject:") as the first line, then the message body.'
        return prompt
