"""
Audio Transcription Module using Faster-Whisper.
Optimized for speed, low memory usage, and easy Windows installation.
"""

from faster_whisper import WhisperModel
from typing import Dict, List
import os


class AudioTranscriber:
    """Faster-Whisper-based audio transcriber."""
    
    MODELS = {
        'tiny': {'size': '39 MB', 'speed': '⚡⚡⚡⚡', 'accuracy': '★★'},
        'base': {'size': '74 MB', 'speed': '⚡⚡⚡', 'accuracy': '★★★'},
        'small': {'size': '244 MB', 'speed': '⚡⚡', 'accuracy': '★★★★'},
        'medium': {'size': '769 MB', 'speed': '⚡', 'accuracy': '★★★★★'},
        'large-v3': {'size': '1.5 GB', 'speed': '🐌', 'accuracy': '★★★★★'}
    }
    
    def __init__(self, model_name: str = 'base'):
        """
        Initialize the transcriber.
        device="cpu" ensures it works on any machine. 
        compute_type="int8" reduces memory usage by 4x with minimal accuracy loss.
        """
        print(f"🔄 Loading Faster-Whisper model: {model_name}...")
        
        try:
            self.model = WhisperModel(
                model_name, 
                device="cpu", 
                compute_type="int8"
            )
            self.model_name = model_name
            print(f"✅ Model loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise

    def transcribe(self, audio_path: str, language: str = None, 
                   enable_vad: bool = True) -> Dict:
        """
        Transcribe an audio file.
        
        Args:
            audio_path: Path to audio file
            language: Language code (e.g., 'fa', 'en'). None for auto-detect.
            enable_vad: Enable Voice Activity Detection (filter out non-speech)
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        print(f"🎤 Transcribing: {os.path.basename(audio_path)}")
        
        # Execute transcription
        segments, info = self.model.transcribe(
            audio_path,
            language=language,
            beam_size=5,
            vad_filter=enable_vad,  # Now controllable
            vad_parameters=dict(
                min_silence_duration_ms=500  # Shorter silence threshold
            ) if enable_vad else None
        )
        
        # Format the output
        segments_list = []
        full_text = []
        
        for segment in segments:
            segments_list.append({
                'start': round(segment.start, 2),
                'end': round(segment.end, 2),
                'text': segment.text.strip()
            })
            full_text.append(segment.text.strip())
        
        return {
            'text': ' '.join(full_text),
            'segments': segments_list,
            'detected_language': info.language,
            'language_probability': round(info.language_probability, 2),
            'duration_seconds': round(info.duration, 2)
        }
    
    def get_model_info(self) -> Dict:
        """Get information about the current model."""
        return {
            'model_name': self.model_name,
            'model_info': self.MODELS.get(self.model_name, {}),
        }


# Singleton instance
_transcriber_instance = None

def get_transcriber(model_name: str = 'base') -> AudioTranscriber:
    """Get or create a singleton transcriber instance."""
    global _transcriber_instance
    if _transcriber_instance is None or _transcriber_instance.model_name != model_name:
        _transcriber_instance = AudioTranscriber(model_name)
    return _transcriber_instance


def test_transcriber():
    """Test the transcriber initialization."""
    print("\n=== Testing Audio Transcriber ===\n")
    transcriber = get_transcriber('base')
    info = transcriber.get_model_info()
    
    print(f"✅ Model: {info['model_name']}")
    print(f"📦 Size: {info['model_info']['size']}")
    print(f"🚀 Speed: {info['model_info']['speed']}")
    print("\n💡 To test with a real file, use:")
    print("   result = transcriber.transcribe('your_audio.mp3')")
    print("   print(result['text'])")


if __name__ == "__main__":
    test_transcriber()