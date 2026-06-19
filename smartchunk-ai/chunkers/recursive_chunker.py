from typing import List, Optional


class RecursiveChunker:

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50,
        separators: Optional[List[str]] = None,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap
        # prefer larger, more semantic separators first
        self.separators = separators or ["\n\n", "\n", ". ", " ", ""]

    def chunk(self, text: str) -> List[str]:
        text = (text or "").strip()
        if not text:
            return []

        if len(text) <= self.chunk_size:
            return [text]

        # try to split using semantic separators
        for sep in self.separators:
            if sep == "":
                continue
            parts = [p for p in text.split(sep) if p]
            if len(parts) == 1:
                continue

            chunks: List[str] = []
            current = ""

            for part in parts:
                candidate = (current + sep + part) if current else part
                if len(candidate) <= self.chunk_size:
                    current = candidate
                else:
                    if current:
                        chunks.append(current)
                    if len(part) <= self.chunk_size:
                        current = part
                    else:
                        # part is too large, fall back to fixed slicing for this part
                        chunks.extend(self._chunk_fallback(part))
                        current = ""

            if current:
                chunks.append(current)

            if chunks:
                return self._apply_overlap(chunks)

        # final fallback: fixed-size slicing with overlap
        return self._chunk_fallback(text)

    def _chunk_fallback(self, text: str) -> List[str]:
        chunks: List[str] = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start += max(1, self.chunk_size - self.overlap)
        return chunks

    def _apply_overlap(self, chunks: List[str]) -> List[str]:
        if self.overlap <= 0:
            return chunks

        out: List[str] = []
        for i, chunk in enumerate(chunks):
            if i == 0:
                out.append(chunk)
            else:
                prev = out[-1]
                overlap_text = prev[-self.overlap:] if self.overlap < len(prev) else prev
                out.append(overlap_text + chunk)
        return out