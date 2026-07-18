# analyzer.py
# Evaluation engine using regular expressions, structured blocks, and semantic similarity.

import re
import numpy as np

class SRSAnalyzer:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        """Lazy load the sentence transformer model to save memory and load time."""
        if self._model is None:
            print(f"[INFO] Initializing SentenceTransformer model: {self.model_name}...")
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
            print("[SUCCESS] Model initialized successfully.")
        return self._model

    def preprocess_document(self, text):
        """
        Cleans and splits text into paragraphs and lines (for backwards compatibility).
        """
        paras = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return paras, lines

    def is_requirements_table(self, table_block):
        """
        Detects if a table is a requirements specification table by checking its column headers.
        """
        headers = table_block.get("headers", [])
        if not headers:
            return False
        
        req_indicators = {"id", "req", "requirement", "description", "priority", "feature", "specification"}
        # Check if at least two headers match requirements keywords (e.g., ID and Requirement)
        matched_indicators = [h for h in headers if any(ind in h for ind in req_indicators)]
        return len(matched_indicators) >= 2

    def check_regex_match(self, section, blocks):
        """
        Search for section IDs, names, or aliases in heading blocks.
        """
        sec_id = section["id"]
        sec_aliases = section.get("aliases", [section["name"]])
        escaped_id = re.escape(sec_id)

        for idx, block in enumerate(blocks):
            if block["type"] != "heading":
                continue
            text = block["text"].strip()

            for alias in sec_aliases:
                # Option A: Check strict ID + Name/Alias match (e.g. "1.1 Purpose")
                pattern_with_id = r'^' + escaped_id + r'[\.\s\-]+' + re.escape(alias) + r'\b'
                if re.match(pattern_with_id, text, re.IGNORECASE):
                    return True, idx, text, "Regex Heading Match"
                
                # Option B: Check loose match of the alias name itself (case-insensitive)
                # This helps if section numbers were excluded
                if text.lower() == alias.lower():
                    return True, idx, text, "Alias Heading Match"
        
        return False, -1, "", None

    def analyze_compliance(self, document, standard_def):
        """
        Performs structural and semantic audit of document blocks against a target standard.
        `document` can be a list of parsed block dicts or a raw string.
        """
        import traceback
        try:
            from sklearn.metrics.pairwise import cosine_similarity

            # 1. Parse document to blocks if it is a raw string
            if isinstance(document, str):
                from parser import extract_blocks_from_plaintext
                blocks = extract_blocks_from_plaintext(document)
            else:
                blocks = document

            if not blocks:
                return {
                    "score": 0.0,
                    "sections": {},
                    "summary": "Document is empty or could not be parsed."
                }

            # Filter paragraph & table texts for semantic encoding
            content_blocks = [b for b in blocks if b["type"] in ("paragraph", "table")]
            
            # Diagnostic check to ensure b["text"] is a string
            for idx, b in enumerate(blocks):
                if not isinstance(b.get("text", ""), str):
                    raise TypeError(f"Block at index {idx} has non-string text of type {type(b.get('text'))}: {repr(b.get('text'))}")

            content_texts = [b["text"] for b in content_blocks]
            
            # Precompute paragraph/table embeddings
            para_embeddings = None
            if content_texts:
                print(f"[INFO] Computing document embeddings for {len(content_texts)} content blocks...")
                para_embeddings = self.model.encode(content_texts)
                print("[SUCCESS] Content block embeddings computed.")

            report = {}
            total_possible_weight = 0
            earned_weight = 0

            # Whitelist headings that are expected to contain placeholders (no penalty)
            whitelist_headings = {"open items", "tbd", "to be determined", "todo", "appendices", "appendix"}

            for sec in standard_def["sections"]:
                sec_id = sec["id"]
                sec_name = sec["name"]
                sec_weight = sec["weight"]
                sec_aliases = sec.get("aliases", [sec_name])
                
                report[sec_id] = {
                    "name": sec_name,
                    "required": sec["required"],
                    "weight": sec_weight,
                    "status": "Missing",
                    "matched_text": "",
                    "match_type": None,
                    "char_count": 0,
                    "feedback": ""
                }

                total_possible_weight += sec_weight

                # 1. Strict/Alias Regex Header Match
                matched, matched_idx, matched_text, match_type = self.check_regex_match(sec, blocks)
                matched_heading_text = ""
                
                if matched:
                    report[sec_id]["status"] = "Matched"
                    report[sec_id]["matched_text"] = matched_text
                    report[sec_id]["match_type"] = match_type
                    matched_heading_text = matched_text

                # 2. Semantic Embedding Fallback (Lowered similarity threshold to 0.42 for reasonable matches)
                if report[sec_id]["status"] == "Missing" and para_embeddings is not None:
                    anchors = sec.get("anchors", [sec_name])
                    anchor_embeddings = self.model.encode(anchors)
                    
                    # Compare similarity
                    sim_matrix = cosine_similarity(anchor_embeddings, para_embeddings)
                    max_sim_idx = np.unravel_index(np.argmax(sim_matrix), sim_matrix.shape)
                    best_anchor_idx, best_content_idx = max_sim_idx
                    best_similarity = sim_matrix[best_anchor_idx, best_content_idx]

                    if best_similarity >= 0.42:
                        report[sec_id]["status"] = "Matched"
                        matched_text = content_texts[best_content_idx]
                        report[sec_id]["matched_text"] = matched_text[:150] + ("..." if len(matched_text) > 150 else "")
                        report[sec_id]["match_type"] = f"Semantic Match ({int(best_similarity*100)}%)"
                        
                        # Associate preceding heading if available
                        matched_heading_text = content_blocks[best_content_idx].get("preceding_heading", "")

                # 3. Gather Content Blocks associated with this matched heading
                associated_blocks = []
                if matched_heading_text:
                    associated_blocks = [b for b in blocks if b["preceding_heading"] == matched_heading_text]
                
                # 4. Check for Requirements Table boost for Specific Requirements (Section 3)
                has_req_table_boost = False
                if sec_id.startswith("3"):
                    for block in associated_blocks:
                        if block["type"] == "table" and self.is_requirements_table(block):
                            has_req_table_boost = True
                            break

                # 5. Content Quality & Context-Aware Placeholder Auditing
                if report[sec_id]["status"] == "Matched":
                    total_char_len = sum(len(b["text"]) for b in associated_blocks if b["type"] != "heading")
                    report[sec_id]["char_count"] = total_char_len
                    
                    # Check for placeholders in a context-aware way (skip whitelisted headings)
                    placeholders = ["todo", "tbd", "insert here", "placeholder", "write description", "lorem ipsum"]
                    is_heading_whitelisted = matched_heading_text and any(wh in matched_heading_text.lower() for wh in whitelist_headings)

                    flagged_lines = []
                    if not is_heading_whitelisted:
                        for block in associated_blocks:
                            if block["type"] in ("paragraph", "table"):
                                for line in block["text"].split("\n"):
                                    if any(p in line.lower() for p in placeholders):
                                        flagged_lines.append(line.strip())

                    if flagged_lines:
                        # Report specific warning context rather than penalizing the whole section if substantial content is present
                        snippet = flagged_lines[0]
                        if len(snippet) > 80:
                            snippet = snippet[:80] + "..."
                        
                        if total_char_len < 100:  # Section is mostly just placeholders
                            report[sec_id]["status"] = "Weak"
                            report[sec_id]["feedback"] = f"Section contains placeholders: '{snippet}' and lacks requirements depth."
                        else:
                            # Matched with specific warnings
                            report[sec_id]["feedback"] = f"Present, but contains warning: '{snippet}'"
                    elif total_char_len < 60 and not has_req_table_boost:
                        report[sec_id]["status"] = "Weak"
                        report[sec_id]["feedback"] = "Section has very brief content details."
                    else:
                        report[sec_id]["feedback"] = "Section is present and appears to contain valid specifications."

                    # Apply Score Boost if a requirement table is detected
                    if has_req_table_boost:
                        report[sec_id]["status"] = "Matched"
                        report[sec_id]["feedback"] = "Requirements table (ID & Requirement columns) detected. Content score boosted!"

                else:
                    report[sec_id]["feedback"] = "Required section is entirely missing from the document."

                # Calculate score contributions
                if report[sec_id]["status"] == "Matched":
                    earned_weight += sec_weight
                elif report[sec_id]["status"] == "Weak":
                    earned_weight += (sec_weight * 0.4)

            # Compute overall score percentage
            score = (earned_weight / total_possible_weight) * 100 if total_possible_weight > 0 else 0.0

            return {
                "score": round(score, 1),
                "sections": report,
                "summary": f"Analyzed against standard. Compliance score is {round(score, 1)}%."
            }
        except Exception as e:
            tb_str = traceback.format_exc()
            print(f"[ERROR] Exception in compliance analysis:\n{tb_str}")
            # Raise a clear message with traceback so the user/developer gets it
            raise ValueError(f"{str(e)}\n\nTraceback:\n{tb_str}")
