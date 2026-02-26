from flask import Flask, request, jsonify
from flask_cors import CORS
from llama_cpp import Llama
import re
import os

app = Flask(__name__)
CORS(app) 

# Absolute pathing for GGUF reliability
from flask import Flask, request, jsonify
from flask_cors import CORS
from llama_cpp import Llama
import re
import os

app = Flask(__name__)
CORS(app) 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "venv", "models", "classics.gguf")

# Offloading to GPU and setting context for winding 19th-century syntax
llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_gpu_layers=-1)


def refine_prose(text):
    """
    The 'Literary Editor' Pipeline.
    Targets SLM tokenization errors (stutters/merges) while 
    polishing 19th-century punctuation.
    """
    if not text:
        return ""

    # 1. THE HEALER: Fix merged words (hissociety, toher, andthe)
    # This regex looks for a lowercase letter followed by common 
    # 'high-probability' tokens that the SLM often skips the space for.
    merge_targets = r'(the|his|her|to|and|was|in|of|it|is|that|with|for)'
    text = re.sub(r'([a-z])' + merge_targets + r'\b', r'\1 \2', text)

    # 2. THE TYPIST: Em-Dash & Punctuation
    # Converts double-hyphens or space-hyphen-space to a proper Em-Dash (—)
    # Note: Victorians often used em-dashes without surrounding spaces.
    text = text.replace("---", "—").replace("--", "—")
    # Ensures a space *after* a comma/period if the SLM forgot it
    text = re.sub(r'(?<=[.,;?!])(?=[^\s"”])', r' ', text)

    # 3. THE PROOFREADER: Specific 'Stutter' Fixes
    # Targets double-consonant artifacts (unfasscinating, ssci)
    stutter_fixes = {
        "ssci": "sci",
        "ffas": "fas",
        "llly": "ly",
        "tthe": "the",
        "ppiq": "piq" # Fixes 'ppiquant'
    }
    for error, correction in stutter_fixes.items():
        text = text.replace(error, correction)

    # 4. THE CLEANER: Whitespace & Markers
    # Removes AI 'thought' artifacts like underscores or asterisks
    text = text.replace("_", "").replace("*", "")
    # Collapses multiple spaces into one
    text = re.sub(r'\s+', ' ', text).strip()

    # 5. THE SURGEON: Sentence Truncation
    # If the SLM cut off mid-sentence, find the last terminal punctuation.
    if text and text[-1] not in ".!?\"”":
        last_punct = max(text.rfind('.'), text.rfind('!'), text.rfind('?'), text.rfind('”'))
        if last_punct != -1:
            text = text[:last_punct + 1]

    return text

@app.route('/api/generate', methods=['POST'])
def generate_prose():
    data = request.json
    user_input = data.get("prompt", "")
    requested_length = int(data.get("length", 250)) 

    # The 'Stylistic Anchor' from your most successful generations
    instruction1 = (
        "Continue the narrative in a refined 19th-century literary style. "
        "Synthesize the social irony of the domestic sphere with deep "
        "psychological introspection. Maintain high vocabulary precision. Write only in English. "
        "Ensure words are never broken by newlines or stray spaces. "
        "Focus on the subtext of the conversation and original character dynamics."
    )
    # Use this exact string for your 'instruction' variable in app.py
    instruction = (
        "Continue the narrative in a refined 19th-century literary style. "
        "Synthesize the social irony of the domestic sphere with earnest moral reflection "
        "and deep psychological introspection. Employ period-appropriate diction and "
        "winding, rhythmic sentences, avoiding modern abstraction. Focus on developing "
        "subtext through gesture, silence, and social constraint while preserving "
        "established character dynamics. Respond only in English, using other languages very sparingly"
    )

    prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{user_input}\n\n### Response:\n"

    output = llm(
        prompt,
        max_tokens=requested_length,
        temperature=0.7,       # Balanced for creative but logical flow
        top_k=4,                # The 'Spelling Shield' from the Jane Eyre success
        top_p=0.9,
        repeat_penalty=1.08,    
        stop=["###", "Instruction:", "Input:"]
    )

    raw_text = output['choices'][0]['text']
    return jsonify({"text": refine_prose(raw_text)})

if __name__ == '__main__':
    app.run(debug=True, port=5001)