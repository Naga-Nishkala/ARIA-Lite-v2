import pandas as pd
from transformers import pipeline
from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM
import torch
import spacy

# TIER 1: Strong GLOBAL triggers (highest priority)
GLOBAL_STRONG = [
    "overview", "summarize", "summary", "landscape",
    "what are", "what types", "types of",
    "compare", "comparison", "differences between",
    "list", "survey", "state of"
]

# TIER 2: Weaker GLOBAL signals
GLOBAL_WEAK = [
    "approaches", "methods used", "trends", "recent trends",
    "major", "common"
]

# TIER 3: Strong LOCAL triggers
LOCAL_STRONG = [
    "how does", "why does", "how is",
    "mechanism", "interaction between",
    "relationship between", "role of",
    "explain the role", "describe the interaction"
]

# TIER 4: Weaker LOCAL signals
LOCAL_WEAK = [
    "predict", "target", "associated", "explain"
]

# Load your Scispacy model (same one you used for papers)
nlp = spacy.load("en_core_sci_md")

def extract_query_entities(query):
    """
    Extract entities from query using Scispacy NER.
    Returns list of entity texts.
    """
    doc = nlp(query)

    entities = []
    for ent in doc.ents:
        entities.append(ent.text.lower())

    return entities

def hybrid_router(query):
    q_lower = query.lower()

    # --------------------------------------------------------
    # TIER 1: Check strong phrase-level triggers FIRST
    # --------------------------------------------------------

    # Strong GLOBAL triggers (immediate return)
    for trigger in GLOBAL_STRONG:
        if trigger in q_lower:
            return "GLOBAL"

    # Strong LOCAL triggers (immediate return)
    for trigger in LOCAL_STRONG:
        if trigger in q_lower:
            return "LOCAL"

    # --------------------------------------------------------
    # TIER 2: Score weaker signals
    # --------------------------------------------------------

    global_score = sum(1 for kw in GLOBAL_WEAK if kw in q_lower)
    local_score = sum(1 for kw in LOCAL_WEAK if kw in q_lower)

    # High confidence from weak signals
    if abs(global_score - local_score) >= 2:
        if global_score > local_score:
            return "GLOBAL"
        return "LOCAL"

    # Clear winner from weak signals
    if global_score > local_score:
        return "GLOBAL"
    elif local_score > global_score:
        return "LOCAL"

    # --------------------------------------------------------
    # TIER 3: Entity-based routing
    # --------------------------------------------------------

    # Extract entities from query
    entities = extract_query_entities(query)

    if len(entities) >= 2:
        return "LOCAL"  # Multi-entity = specific relationship
    elif len(entities) == 0:
        return "GLOBAL"  # No entities = vague overview

    # --------------------------------------------------------
    # TIER 4: Query length heuristic fallback
    # --------------------------------------------------------

    word_count = len(query.split())

    if word_count <= 3:
        return "LOCAL"   # Very short = entity lookup
    else:
        return "GLOBAL"  # Longer ambiguous = exploratory
