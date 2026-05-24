from langchain.chat_models import init_chat_model

from app.conf.app_config import app_config

llm = init_chat_model(model=app_config.llm.model_name,
                      model_provider="deepseek",
                      base_url=app_config.llm.base_url,
                      temperature=0)
if __name__ == '__main__':
    print(llm.invoke("你好").content)