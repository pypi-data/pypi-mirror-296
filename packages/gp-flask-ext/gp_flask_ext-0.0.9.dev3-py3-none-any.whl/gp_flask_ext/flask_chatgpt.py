import openai
from loguru import logger
from flask import Blueprint, Flask, request, render_template

__all__ = ["init_app"]

def init_app(app: Flask, config=None):
    # Merge the default config with the provided config
    base_config = app.config.get("CHATGPT_CONFIG", {})
    if config:
        base_config.update(config)
    config = base_config

    if config.get("blueprint", True):
        bp = Blueprint("chatgpt", __name__, url_prefix="/chatgpt", template_folder="templates")  # 创建一个蓝图对象
        @bp.route('/')
        def index():
            return render_template("chatgpt/index.html")
        
        @bp.route('/ask', methods=["POST"])
        def ask():
            user_input = request.json.get("user_input")
            max_tokens = request.json.get("max_tokens", 500)
            if not user_input:
                return {"error": "User input is required."}, 400
            data = {
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ],
                "max_tokens": max_tokens,
                "model": "4o-test",
                "temperature": 0.5,
                "top_p": 1.0,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.,
                "stream": False
            }
            response = openai.chat.completions.create(
                **data
            )
            # for chunk in response:
            #     message = chunk.choices[0].delta.content or ""
            logger.info(response)
            message = response.choices[0].message.content or ""
            return message

        app.register_blueprint(bp)  # 注册蓝图
        logger.info("Registered the ChatGPT blueprint")
