from typing import AsyncGenerator

from pyflowery.models import FloweryAPIConfig, Language, Voice
from pyflowery.rest_adapter import RestAdapter


class FloweryAPI:
    """Main class for interacting with the Flowery API

    Attributes:
        config (FloweryAPIConfig): Configuration object for the API
        adapter (RestAdapter): Adapter for making HTTP requests
    """
    def __init__(self, config: FloweryAPIConfig = FloweryAPIConfig()):
        self.config = config
        self.adapter = RestAdapter(config)

    async def get_voice(self, voice_id: str) -> Voice:
        """Get a voice from the Flowery API

        Args:
            voice_id (str): The ID of the voice

        Returns:
            Voice: The voice
        """
        async for voice in self.get_voices():
            if voice.id == voice_id:
                return voice

    async def get_voices(self) -> AsyncGenerator[Voice, None]:
        """Get a list of voices from the Flowery API

        Returns:
            AsyncGenerator[Voice, None]: A generator of Voices
        """
        request = await self.adapter.get('/tts/voices')
        for voice in request.data['voices']:
            yield Voice(
                id=voice['id'],
                name=voice['name'],
                gender=voice['gender'],
                source=voice['source'],
                language=Language(**voice['language']),
            )

    async def get_tts(self, text: str, voice: Voice | str | None = None, translate: bool = False, silence: int = 0, audio_format: str = 'mp3', speed: float = 1.0):
        """Get a TTS audio file from the Flowery API

        Args:
            text (str): The text to convert to speech
            voice (Voice | str): The voice to use for the speech
            translate (bool): Whether to translate the text
            silence (int): Number of seconds of silence to add to the end of the audio
            audio_format (str): The audio format to return
            speed (float): The speed of the speech

        Returns:
            bytes: The audio file
        """
        if len(text) > 2048:
            if not self.config.allow_truncation:
                raise ValueError('Text must be less than 2048 characters')
            self.config.logger.warning('Text is too long, will be truncated to 2048 characters by the API')
        params = {
            'text': text,
            'translate': str(translate).lower(),
            'silence': silence,
            'audio_format': audio_format,
            'speed': speed,
        }
        if voice:
            params['voice'] = voice.id if isinstance(voice, Voice) else voice
        request = await self.adapter.get('/tts', params, timeout=180)
        return request.data
