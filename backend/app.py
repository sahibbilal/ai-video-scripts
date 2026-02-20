"""
Flask backend API for Video Script Generator
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import traceback

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ai_client import OllamaClient
from src.idea_generator import IdeaGenerator
from src.script_generator import ScriptGenerator

app = Flask(__name__)
CORS(app)

# Enable detailed error messages in debug mode
app.config['DEBUG'] = True

# Initialize clients
ollama_client = OllamaClient()
idea_generator = IdeaGenerator(ollama_client)
script_generator = ScriptGenerator(ollama_client)


@app.route('/api/ollama/check', methods=['GET'])
def check_ollama():
    """Check if Ollama is connected."""
    try:
        connected = ollama_client.check_connection()
        return jsonify({'connected': connected})
    except Exception as e:
        return jsonify({'connected': False, 'error': str(e)}), 500


@app.route('/api/ollama/models', methods=['GET'])
def get_models():
    """Get available Ollama models."""
    try:
        models = ollama_client.get_available_models()
        return jsonify({'models': models})
    except Exception as e:
        return jsonify({'models': [], 'error': str(e)}), 500


@app.route('/api/ideas/generate', methods=['POST'])
def generate_ideas():
    """Generate video topic ideas."""
    try:
        data = request.json
        category = data.get('category', 'Any')
        model = data.get('model', 'llama3')
        
        ideas = idea_generator.generate_ideas(category=category, model=model)
        return jsonify({'ideas': ideas})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/discuss', methods=['POST'])
def discuss():
    """Discuss and refine an idea."""
    try:
        data = request.json
        idea = data.get('idea')
        question = data.get('question')
        conversation_history = data.get('conversationHistory', [])
        model = data.get('model', 'llama3')
        
        response = ollama_client.discuss_idea(
            idea=idea,
            user_question=question,
            conversation_history=conversation_history,
            model=model
        )
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/script/generate', methods=['POST'])
def generate_script():
    """Generate a video script."""
    try:
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        app.logger.info(f"Script generation request: {data}")
        
        model = data.get('model')
        if not model:
            # Try to get first available model
            available_models = ollama_client.get_available_models()
            if available_models:
                model = available_models[0]
                app.logger.info(f"Using default model: {model}")
            else:
                return jsonify({'error': 'No Ollama models available. Please pull a model first (e.g., ollama pull llama3)'}), 400
        
        idea = data.get('idea')
        if not idea:
            return jsonify({'error': 'Idea/topic is required'}), 400
        
        language = data.get('language', 'English')
        app.logger.info(f"Generating script in {language} language...")
        
        result = script_generator.generate(
            idea=idea,
            keywords=data.get('keywords', ''),
            video_length_minutes=float(data.get('videoLengthMinutes', 1.0)),
            tone=data.get('tone', 'Professional'),
            language=language,
            model=model,
            include_images=data.get('includeImages', False),
            image_type=data.get('imageType', 'descriptions')
        )
        app.logger.info("Script generated successfully")
        return jsonify(result)
    except ValueError as e:
        app.logger.error(f"ValueError in generate_script: {str(e)}")
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400
    except Exception as e:
        app.logger.error(f"Error in generate_script: {str(e)}")
        app.logger.error(traceback.format_exc())
        error_msg = str(e)
        if 'timeout' in error_msg.lower() or 'timed out' in error_msg.lower():
            error_msg = f"Request timed out. This can happen with non-English languages. Please try again or use a faster model. Original error: {error_msg}"
        return jsonify({'error': error_msg, 'traceback': traceback.format_exc() if app.config['DEBUG'] else None}), 500


@app.route('/api/script/series', methods=['POST'])
def generate_series():
    """Generate a series of video scripts."""
    try:
        data = request.json
        num_episodes = int(data.get('numEpisodes', 3))
        if num_episodes < 1 or num_episodes > 10:
            return jsonify({'error': 'Number of episodes must be between 1 and 10'}), 400
        
        model = data.get('model')
        if not model:
            # Try to get first available model
            available_models = ollama_client.get_available_models()
            if available_models:
                model = available_models[0]
            else:
                return jsonify({'error': 'No Ollama models available. Please pull a model first (e.g., ollama pull llama3)'}), 400
        
        language = data.get('language', 'English')
        app.logger.info(f"Generating series of {num_episodes} episodes in {language} language...")
        
        episodes = script_generator.generate_series(
            idea=data.get('idea'),
            num_episodes=num_episodes,
            keywords=data.get('keywords', ''),
            video_length_minutes=float(data.get('videoLengthMinutes', 1.0)),
            tone=data.get('tone', 'Professional'),
            language=language,
            model=model,
            include_images=data.get('includeImages', False),
            image_type=data.get('imageType', 'descriptions')
        )
        
        app.logger.info(f"Series generation completed: {len(episodes)} episodes")
        
        # Combine all episodes
        combined_script = f"📺 SERIES: {data.get('idea', '').upper()}\n"
        combined_script += "=" * 80 + "\n\n"
        
        for episode in episodes:
            ep_num = episode["episode_number"]
            script = episode["script"]
            combined_script += f"\n{'=' * 80}\n"
            combined_script += f"EPISODE {ep_num} of {data.get('numEpisodes', 3)}\n"
            combined_script += f"{'=' * 80}\n\n"
            combined_script += script
            combined_script += f"\n\n[Episode {ep_num} - {episode['actual_chars']}/{episode['target_chars']} characters]\n"
            combined_script += "\n" + "-" * 80 + "\n\n"
        
        return jsonify({
            'episodes': episodes,
            'combinedScript': combined_script
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)
    app.run(debug=True, port=5000, host='127.0.0.1')
