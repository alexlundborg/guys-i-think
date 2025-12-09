#!/bin/bash
cd "/Users/alexander/Documents/guys I think I"
source venv/bin/activate
export OPENAI_API_KEY='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'

echo "Regenerating chunks 3, 6, and 8..."
python3 regenerate_chunk.py 3
python3 regenerate_chunk.py 6
python3 regenerate_chunk.py 8

echo ""
echo "Done! Now merging..."
cat > filelist.txt << 'EOF'
file 'narration_chunk_1.mp3'
file 'narration_chunk_2.mp3'
file 'narration_chunk_3.mp3'
file 'narration_chunk_4.mp3'
file 'narration_chunk_5.mp3'
file 'narration_chunk_6.mp3'
file 'narration_chunk_7.mp3'
file 'narration_chunk_8.mp3'
file 'narration_chunk_9.mp3'
file 'narration_chunk_10.mp3'
file 'narration_chunk_11.mp3'
EOF

ffmpeg -f concat -safe 0 -i filelist.txt -c:a libmp3lame -q:a 2 -ar 44100 story-narration.mp3 -y
rm filelist.txt

echo ""
echo "✓ All done! Refresh localhost:8080 to hear the updated narration."
