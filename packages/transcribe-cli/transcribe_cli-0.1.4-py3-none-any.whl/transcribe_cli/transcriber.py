import os
import json
from collections import defaultdict
from typing import List, Dict, Any
import assemblyai as aai

from .downloader import create_youtube_timestamp_link

def get_or_create_transcription(audio_file_path: str, api_key: str, language: str = 'en', force_transcribe: bool = False) -> List[Dict[str, Any]]:
    """
    Get an existing transcription or create a new one using AssemblyAI API.
    
    :param audio_file_path: Path to the audio file
    :param api_key: AssemblyAI API key
    :param language: Language code for transcription (default: 'en')
    :param force_transcribe: If True, transcribe even if the file exists in cache
    :return: Transcription text with timestamps and speaker labels
    """
    video_id = os.path.splitext(os.path.basename(audio_file_path))[0]
    transcription_file = os.path.join('.audio', f"{video_id}-{language}.json")
    
    if os.path.exists(transcription_file) and not force_transcribe:
        print(f"Using cached transcription: {transcription_file}")
        with open(transcription_file, 'r') as f:
            return json.load(f)
    
    # Configure AssemblyAI client
    aai.settings.api_key = api_key
    
    # Create a transcription config
    config = aai.TranscriptionConfig(
        language_code=language,
        speaker_labels=True,
        word_boost=["[inaudible]"],
        boost_param=aai.WordBoost.high
    )
    
    # Create a transcriber
    transcriber = aai.Transcriber(config=config)
    
    # Start the transcription
    transcript = transcriber.transcribe(audio_file_path)
    
    # Process utterances to create timestamped paragraphs with speaker labels
    timestamped_transcript = []
    
    for utterance in transcript.utterances:
        timestamped_transcript.append({
            "start": format_timestamp(utterance.start),
            "end": format_timestamp(utterance.end),
            "speaker": "Speaker" + utterance.speaker,
            "text": utterance.text,
            "audio_file": audio_file_path
        })
    
    # Save the transcription to a file
    with open(transcription_file, 'w') as f:
        json.dump(timestamped_transcript, f, indent=2)
    
    return timestamped_transcript

def name_speakers(timestamped_transcript: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Allow the user to name each speaker in the transcript.
    
    :param timestamped_transcript: List of utterances with speaker labels
    :return: Updated transcript with named speakers
    """
    speaker_names = {}
    speaker_utterances = defaultdict(list)

    # Group utterances by speaker
    for utterance in timestamped_transcript:
        speaker_utterances[utterance['speaker']].append(utterance)

    video_id = os.path.splitext(os.path.basename(timestamped_transcript[0]['audio_file']))[0]

    for speaker_index, (speaker, utterances) in enumerate(speaker_utterances.items(), 1):
        if not speaker.startswith("Speaker"):  # Check if the speaker already has a name
            speaker_names[speaker] = speaker
        else:
            print(f"\nGlimpse of Speaker {speaker_index}'s lines:")
            for i, utterance in enumerate(utterances[:4], 1):
                timestamp_link = create_youtube_timestamp_link(video_id, utterance['start'])
                print(f"{i}. [{utterance['start']}]({timestamp_link}) {utterance['text']}")
            
            name = input(f"\nEnter a name for Speaker {speaker_index}: ").strip()
            speaker_names[speaker] = name if name else f"Speaker {speaker_index}"

    named_transcript = []
    for utterance in timestamped_transcript:
        named_utterance = utterance.copy()
        named_utterance['speaker'] = speaker_names[utterance['speaker']]
        named_transcript.append(named_utterance)

    return named_transcript

def format_timestamp(ms: int) -> str:
    """Convert milliseconds to HH:MM:SS format"""
    seconds = int(ms / 1000)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
