#!/usr/bin/env python3
"""Quick test of chunking functions with uploads/sample.txt"""

import sys
sys.path.insert(0, '.')

from parsers.text_parser import TXTParser
from chunkers.fixed_chunker import FixedChunker
from chunkers.recursive_chunker import RecursiveChunker

# Test parsing
print("=" * 60)
print("Testing TXTParser with uploads/sample.txt")
print("=" * 60)

try:
    text = TXTParser.extract_text("uploads/sample.txt")
    print(f"✓ Successfully extracted text ({len(text)} chars)\n")
except Exception as e:
    print(f"✗ Error extracting text: {e}\n")
    sys.exit(1)

# Test FixedChunker
print("=" * 60)
print("Testing FixedChunker (chunk_size=500, overlap=50)")
print("=" * 60)

try:
    fixed = FixedChunker(chunk_size=500, overlap=50)
    fixed_chunks = fixed.chunk(text)
    print(f"✓ Generated {len(fixed_chunks)} chunks")
    for i, chunk in enumerate(fixed_chunks[:2]):
        print(f"  Chunk {i+1} ({len(chunk)} chars): {chunk[:60]}...")
    print()
except Exception as e:
    print(f"✗ Error: {e}\n")
    sys.exit(1)

# Test RecursiveChunker
print("=" * 60)
print("Testing RecursiveChunker (chunk_size=500, overlap=50)")
print("=" * 60)

try:
    recursive = RecursiveChunker(chunk_size=500, overlap=50)
    recursive_chunks = recursive.chunk(text)
    print(f"✓ Generated {len(recursive_chunks)} chunks")
    for i, chunk in enumerate(recursive_chunks[:2]):
        print(f"  Chunk {i+1} ({len(chunk)} chars): {chunk[:60]}...")
    print()
except Exception as e:
    print(f"✗ Error: {e}\n")
    sys.exit(1)

print("=" * 60)
print("All tests passed! ✓")
print("=" * 60)
