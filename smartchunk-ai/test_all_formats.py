#!/usr/bin/env python3
"""Test chunking with multiple file formats."""

import sys
sys.path.insert(0, '.')

from parsers.file_parser import FileParser
from chunkers.fixed_chunker import FixedChunker
from chunkers.recursive_chunker import RecursiveChunker

test_files = [
    ("uploads/sample.txt", "TXT"),
    ("uploads/sample.docx", "DOCX"),
]

print("=" * 70)
print("SUPPORTED FILE TYPES")
print("=" * 70)
print(f"Supported: {', '.join(FileParser.get_supported_types())}\n")

for file_path, file_type in test_files:
    print("=" * 70)
    print(f"Testing {file_type}: {file_path}")
    print("=" * 70)
    
    try:
        # Parse file
        text = FileParser.extract_text(file_path)
        print(f"✓ Successfully extracted text ({len(text)} chars)\n")
        
        # Test FixedChunker
        print(f"  FixedChunker (chunk_size=500, overlap=50):")
        fixed = FixedChunker(chunk_size=500, overlap=50)
        fixed_chunks = fixed.chunk(text)
        print(f"    Generated {len(fixed_chunks)} chunks")
        
        # Test RecursiveChunker
        print(f"  RecursiveChunker (chunk_size=500, overlap=50):")
        recursive = RecursiveChunker(chunk_size=500, overlap=50)
        recursive_chunks = recursive.chunk(text)
        print(f"    Generated {len(recursive_chunks)} chunks\n")
        
    except FileNotFoundError:
        print(f"⚠ File not found: {file_path}\n")
    except Exception as e:
        print(f"✗ Error processing {file_type}: {e}\n")

print("=" * 70)
print("Testing complete!")
print("=" * 70)
