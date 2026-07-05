import re
import json
import os
import argparse
from typing import Dict, List, Tuple

# Try to import spacy, if not available fallback to regex only
try:
    import spacy
    HAS_SPACY = True
except ImportError:
    HAS_SPACY = False
    print("Warning: spaCy is not installed. Running in regex-only mode.")
    print("To install: pip install spacy && python -m spacy download vi_core_news_lg (or en_core_web_sm)")

class LorebookExtractor:
    def __init__(self, use_spacy: bool = True):
        self.use_spacy = use_spacy and HAS_SPACY
        if self.use_spacy:
            # We would typically use a Vietnamese model, but let's try generic tokenization if specific model fails
            try:
                self.nlp = spacy.load("xx_ent_wiki_sm") # Multi-language NER
            except OSError:
                print("Multi-language spaCy model not found. Proceeding with regex-only.")
                self.use_spacy = False

        # Keywords dictionary for extraction
        self.keywords = {
            "appearance": [
                "cao", "thấp", "gầy", "béo", "mập", "ốm", "tóc", "mắt", "da", 
                "xinh", "đẹp", "dễ thương", "ngực", "vú", "đùi", "mông", "eo", 
                "môi", "mũi", "mảnh mai", "tròn trịa", "trắng"
            ],
            "personality": [
                "hiền", "dữ", "lạnh lùng", "dâm", "ngoan", "nhút nhát", "ngại ngùng",
                "thông minh", "ngốc", "vui vẻ", "tức giận", "kiêu ngạo", "thực dụng",
                "cam chịu", "mạnh mẽ", "yếu đuối", "ngây thơ"
            ],
            "clothing": [
                "váy", "áo", "quần", "đồng phục", "nội y", "đồ lót", "tất", "giày"
            ]
        }

    def _extract_characters_regex(self, text: str) -> List[str]:
        # Very basic heuristic for Vietnamese names: Capitalized words
        # This is a naive approach, usually spaCy is better
        pattern = r"([A-Z][a-zà-ỹ]+(?:\s[A-Z][a-zà-ỹ]+)+)"
        matches = re.findall(pattern, text)
        
        # Filter common non-names
        stop_words = ["Trong", "Khi", "Nhưng", "Vậy", "Một", "Những", "Cái"]
        chars = [m for m in matches if not any(m.startswith(sw) for sw in stop_words)]
        
        # Count frequency to find main characters
        from collections import Counter
        char_counts = Counter(chars)
        return [char for char, count in char_counts.most_common(5)]

    def extract_context_around_name(self, text: str, name: str, window: int = 50) -> str:
        """Extracts context around mentions of a character."""
        words = text.split()
        name_parts = name.split()
        first_name = name_parts[-1] # Usually Vietnamese names are referred by last word
        
        context = []
        for i, word in enumerate(words):
            if first_name.lower() in word.lower():
                start = max(0, i - window)
                end = min(len(words), i + window)
                context.append(" ".join(words[start:end]))
        
        return " ".join(context)

    def analyze_traits(self, context_text: str) -> Dict[str, str]:
        """Analyzes context text against keyword dictionaries."""
        traits = {
            "appearance": [],
            "personality": [],
            "clothing": []
        }
        
        sentences = re.split(r'[.!?]', context_text)
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            for category, words in self.keywords.items():
                for word in words:
                    if re.search(r'\b' + word + r'\b', sentence_lower):
                        traits[category].append(sentence.strip())
                        break # One sentence is enough per category to avoid duplication
                        
        # Deduplicate and limit
        for k in traits:
            traits[k] = list(set(traits[k]))[:5] # Keep top 5 sentences
            
        return traits

    def create_sillytavern_entry(self, uid: int, name: str, traits: Dict) -> Dict:
        """Formats the extracted traits into a SillyTavern JSON entry."""
        
        # Construct content string
        content_dict = {
            "character_profile": {
                "basic_info": {
                    "name": name
                },
                "appearance": " ".join(traits["appearance"]),
                "personality": " ".join(traits["personality"]),
                "clothing": " ".join(traits["clothing"])
            }
        }
        
        content_str = json.dumps(content_dict, ensure_ascii=False, indent=2)
        
        entry = {
            "uid": uid,
            "key": [name, name.split()[-1]],
            "keysecondary": [],
            "comment": f"Auto-extracted: {name}",
            "content": content_str,
            "constant": False,
            "vectorized": False,
            "selective": True,
            "selectiveLogic": 0,
            "addMemo": True,
            "order": 100,
            "position": 0,
            "disable": False,
            "ignoreBudget": False,
            "excludeRecursion": False,
            "preventRecursion": False,
            "probability": 100,
            "useProbability": True,
            "depth": 4,
            "displayIndex": uid
        }
        return entry

    def process_file(self, input_path: str, output_path: str):
        print(f"Reading file: {input_path}")
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()

        print("Extracting characters...")
        if self.use_spacy:
            doc = self.nlp(text[:100000]) # Limit length for speed
            characters = [ent.text for ent in doc.ents if ent.label_ == "PER"]
            from collections import Counter
            characters = [c for c, _ in Counter(characters).most_common(5)]
        else:
            characters = self._extract_characters_regex(text)

        print(f"Found characters: {characters}")

        lorebook = {"entries": {}}
        
        for uid, char in enumerate(characters):
            print(f"Analyzing {char}...")
            context = self.extract_context_around_name(text, char)
            traits = self.analyze_traits(context)
            entry = self.create_sillytavern_entry(uid, char, traits)
            lorebook["entries"][str(uid)] = entry

        print(f"Saving to {output_path}...")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(lorebook, f, ensure_ascii=False, indent=2)
        print("Done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract SillyTavern Lorebook from story text.")
    parser.add_argument("input_file", help="Path to input text file")
    parser.add_argument("output_file", help="Path to output JSON file")
    
    args = parser.parse_args()
    
    if os.path.exists(args.input_file):
        extractor = LorebookExtractor(use_spacy=False) # Defaulting to regex for simplicity in base env
        extractor.process_file(args.input_file, args.output_file)
    else:
        print(f"Error: File {args.input_file} not found.")