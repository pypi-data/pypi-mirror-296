import argparse
import os
import json
from dotenv import load_dotenv
from downloader import extract_video_id, create_youtube_timestamp_link
from audio_providers.youtube_audio_provider import YouTubeAudioProvider
from transcriber import get_or_create_transcription, name_speakers


def main() -> None:
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY not found in environment variables")

    parser = argparse.ArgumentParser(
        description="Download audio from YouTube videos and transcribe it with speaker labels")
    parser.add_argument("input", help="YouTube video URL or video ID")
    parser.add_argument("-l", "--language", default="en", help="Language code for transcription (default: en)")
    parser.add_argument("-fd", "--force-download", action="store_true",
                        help="Force download even if audio file exists in cache")
    parser.add_argument("-ft", "--force-transcribe", action="store_true",
                        help="Force transcription even if transcription file exists in cache")
    parser.add_argument("-s", "--skip-naming", action="store_true", help="Skip naming speakers")
    parser.add_argument("-o", "--output", help="Output markdown file (default: display in console)")
    args = parser.parse_args()

    # Ensure the .audio directory exists
    os.makedirs('.audio', exist_ok=True)

    # Determine if the input is a URL or a video ID
    if args.input.startswith(('http://', 'https://', 'www.')):
        video_id = extract_video_id(args.input)
        url = args.input
    else:
        video_id = args.input
        url = f"https://www.youtube.com/watch?v={video_id}"

    audio_provider = YouTubeAudioProvider(video_id, force_download=args.force_download)
    transcription_file = os.path.join('.audio', f"{video_id}-{args.language}.json")

    if os.path.exists(transcription_file) and not args.force_transcribe:
        print(f"Using cached transcription: {transcription_file}")
        with open(transcription_file, 'r') as f:
            timestamped_transcript = json.load(f)
    else:
        audio_file = audio_provider.download_audio()
        print(f"Audio file: '{audio_file}'")

        print(f"Getting or creating transcription in {args.language}...")
        timestamped_transcript = get_or_create_transcription(audio_file, api_key, args.language,
                                                             force_transcribe=args.force_transcribe)

    if not args.skip_naming:
        print("Naming speakers...")
        timestamped_transcript = name_speakers(timestamped_transcript)

        # Save the updated transcription with named speakers
        with open(transcription_file, 'w') as f:
            json.dump(timestamped_transcript, f, indent=2)

    markdown_content = f"# Transcript for {url}\n\n"
    for utterance in timestamped_transcript:
        timestamp_link = create_youtube_timestamp_link(video_id, utterance['start'])
        markdown_content += f"## [{utterance['start']}]({timestamp_link}) - {utterance['speaker']}\n\n"
        markdown_content += f"{utterance['text']}\n\n"

    if args.output:
        print(f"Generating markdown output: {args.output}")
        with open(args.output, 'w') as f:
            f.write(markdown_content)
        print(f"Markdown transcript saved to: {args.output}")
    else:
        print("Displaying markdown content:\n")
        print(markdown_content)


if __name__ == "__main__":
    main()
