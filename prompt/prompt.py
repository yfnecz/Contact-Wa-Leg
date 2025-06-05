import random, os

class Prompt:
    def __init__(self):
        prompt_path = os.path.join(os.path.dirname(__file__), "prompt.txt")
        with open(prompt_path) as file:
            self.base_prompt = file.read().strip()

    def get_prompt(self):
        tones = ["urgent", "emotional", "calm but serious", "formal", "compassionate"]
        prompt = self.base_prompt + 'Each message must have a completely different *opening line* that does not resemble the structure or language of previous letters. Do not begin with “I am writing to you today with a heavy heart…” or anything close. Instead, vary tone, entry point, and sentence structure creatively while remaining appropriate and respectful.'
        prompt += f'Tone: {random.choice(tones)}'
        return prompt
