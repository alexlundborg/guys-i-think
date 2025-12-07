#!/usr/bin/env python3
"""
Generate AI narration for 'Guys, I think...'
Uses OpenAI TTS-1-HD with Ash voice
Handles chunking for long text
Cost: ~$1.23 for full story
"""

import os
from pathlib import Path
from openai import OpenAI

def chunk_text(text, max_chars=4000):
    """Split text into chunks at paragraph boundaries"""
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        # If adding this paragraph would exceed limit, save current chunk and start new one
        if len(current_chunk) + len(para) + 2 > max_chars:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = para
        else:
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para

    # Add final chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def main():
    # Check for API key
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        return

    # Read the story
    story_path = Path(__file__).parent / 'complete_draft.md'
    print(f"Reading story from {story_path}...")

    with open(story_path, 'r') as f:
        story_text = f.read()

    # Remove markdown formatting for better narration
    story_text = story_text.replace('# Guys, I think...', 'Guys, I think...')
    story_text = story_text.replace('**Version 1.0.0** | Published December 7, 2025', '')
    story_text = story_text.replace('**', '')
    story_text = story_text.replace('*', '')
    story_text = story_text.replace('---', '')
    story_text = story_text.replace('## CHAPTER', 'Chapter')
    story_text = story_text.replace('![The team on the terrace at dusk](ending_terrace.jpeg)', '')

    char_count = len(story_text)
    print(f"Story length: {char_count:,} characters")
    print(f"Estimated cost: ${(char_count / 1000) * 0.030:.2f} (TTS-1-HD)")

    # Split into chunks
    chunks = chunk_text(story_text)
    print(f"\nSplit into {len(chunks)} chunks for processing...")

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    print("\nGenerating audio with OpenAI TTS-1-HD (voice: ash)...")
    print("This will take a few minutes...")

    # Generate audio for each chunk
    audio_files = []

    try:
        for i, chunk in enumerate(chunks, 1):
            print(f"\nProcessing chunk {i}/{len(chunks)} ({len(chunk)} chars)...")

            response = client.audio.speech.create(
                model="tts-1-hd",
                voice="ash",
                input=chunk,
                speed=1.0
            )

            # Save chunk
            chunk_path = Path(__file__).parent / f'narration_chunk_{i}.mp3'
            response.stream_to_file(str(chunk_path))
            audio_files.append(chunk_path)
            print(f"  ✓ Saved chunk {i}")

        print(f"\n✓ Generated {len(audio_files)} audio chunks")
        print("\nTo combine chunks into one file, install ffmpeg and run:")
        print(f"  cd \"{Path(__file__).parent}\"")
        print(f"  ffmpeg -i \"concat:{'|'.join([f'narration_chunk_{i}.mp3' for i in range(1, len(audio_files)+1)])}\" -acodec copy story-narration.mp3")
        print("\nOr use the chunks separately in your web app.")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        if "invalid" in str(e).lower() and "voice" in str(e).lower():
            print("\nNote: 'ash' voice may not be available yet.")
            print("Try one of: alloy, echo, fable, onyx, nova, shimmer")
            print("Recommendation for your story: onyx (deep male) or nova (warm female)")

if __name__ == '__main__':
    main()
