#!/usr/bin/env python3
"""
Regenerate a specific audio chunk.
Usage: python regenerate_chunk.py <chunk_number>
"""

import os
import sys
from pathlib import Path
from openai import OpenAI

def chunk_text(text, max_chars=4000):
    """Split text into chunks at paragraph boundaries"""
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 > max_chars:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = para
        else:
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def main():
    if len(sys.argv) < 2:
        print("Usage: python regenerate_chunk.py <chunk_number>")
        print("Example: python regenerate_chunk.py 3")
        sys.exit(1)

    chunk_num = int(sys.argv[1])

    # Check for API key
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)

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

    # Split into chunks
    chunks = chunk_text(story_text)
    print(f"Story split into {len(chunks)} chunks")

    if chunk_num < 1 or chunk_num > len(chunks):
        print(f"Error: chunk number must be between 1 and {len(chunks)}")
        sys.exit(1)

    chunk = chunks[chunk_num - 1]
    print(f"\nRegenerating chunk {chunk_num} ({len(chunk)} chars)...")
    print(f"Preview: {chunk[:100]}...")

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Generate audio
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="ash",
        input=chunk,
        speed=1.0
    )

    # Save chunk
    chunk_path = Path(__file__).parent / f'narration_chunk_{chunk_num}.mp3'
    response.stream_to_file(str(chunk_path))
    print(f"✓ Saved chunk {chunk_num} to {chunk_path}")

    print(f"\nDone! Now run the merge command to update story-narration.mp3")

if __name__ == '__main__':
    main()
