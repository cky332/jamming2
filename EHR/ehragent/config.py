import os


def openai_config(model):
    if model.startswith("Pro/deepseek-ai/") or model.startswith("deepseek-ai/"):
        # DeepSeek-V3.2 经 SiliconFlow OpenAI 兼容接口；key 只从环境变量读取
        config = {
            "model": model,
            "api_key": os.getenv("SILICONFLOW_API_KEY"),
            "base_url": "https://api.siliconflow.cn/v1",
        }
    elif model == 'gpt-4':
        config = {
            "model": "gpt-4",
            "api_key": "your-key"
        }
    elif model == 'gpt-4o':
        config = {
            "model": "gpt-4o",
            "api_key": "your-key"
        }
    else:
        config = {
            "model": "o1-preview",
            "api_key": "your-key"
        }
    return config

def llm_config_list(seed, config_list):
    llm_config_list = {
        "functions": [
            {
                "name": "python",
                "description": "run the entire code and return the execution result. Only generate the code.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "cell": {
                            "type": "string",
                            "description": "Valid Python code to execute.",
                        }
                    },
                    "required": ["cell"],
                },
            },
        ],
        "config_list": config_list,
        "timeout": 120,
        "cache_seed": seed,
        "temperature": 0,
    }
    return llm_config_list