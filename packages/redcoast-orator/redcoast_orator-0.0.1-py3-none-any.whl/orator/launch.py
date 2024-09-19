import os
from dotenv import load_dotenv
import gradio as gr
from loguru import logger
from orator.agents.lite import OratorLite
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser



def change_lang(target_lang):
    global agent_instance, greet_translator

    greet_template = os.getenv("ORATOR_GREETING").format(name=os.getenv("ORATOR_AGENT_NAME"), title=os.getenv("ORATOR_TITLE"))

    new_greeting = greet_translator.invoke({"greeting": greet_template, "language": target_lang})

    return [(None, new_greeting)]

SUPPORTED_LANG = [
    "English (EN)",
    "简体中文 (ZH-CN)",
    "繁體中文 (ZH-TW)",
    "Español (ES)",
    "Hindi (HI)",
    "Français (FR)",
    "العربية (AR)",
    "Bengali (BN)",
    "Русский (RU)",
    "Português (PT)",
    "日本語 (JA)",
    "한국어 (KO)",
    "Deutsch (DE)",
    "Nederlands (NL)",
    "Italiano (IT)",
    "Türkçe (TR)",
    "Svenska (SV)",
    "Polski (PL)",
    "Suomi (FI)",
    "Dansk (DA)",
    "Norsk (NO)",
    "עברית (HE)",
    "Čeština (CS)",
    "Ελληνικά (EL)",
    "Magyar (HU)"
]


def make_title(title, authors, detailed_info):
    title_html = f"""<div style="text-align: center;">
<h1>{title}</h1>
<h3>{authors}</h3>
<text>{detailed_info}</text>
</div>"""
    return title_html

def update_history(query, chatbot):
    chatbot += [(query, None)]
    return "", chatbot

def chat(chatbot, language):
    global agent_instance
    query = chatbot[-1][0]
    if agent_instance is None:
        logger.error("Please launch the Orator first.")
        raise Exception("Please launch the Orator first.")
    
    resp = agent_instance.reply(query, language)
    
    chatbot[-1] = [query, resp]

    return chatbot

if __name__ == "__main__":
    load_dotenv(dotenv_path="./.env")

    agent_instance = None

    emb_model = OpenAIEmbeddings(
        model=os.getenv("EMBEDDING_MODEL"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_API_BASE"),
    )

    llm = ChatOpenAI(
        model=os.getenv("LANGUAGE_MODEL"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_API_BASE")
    )

    agent_instance = OratorLite(
        name=os.getenv("ORATOR_AGENT_NAME"),
        paper_title=os.getenv("ORATOR_TITLE"),        # <Your paper title> 
        paper_fpath=os.getenv("ORATOR_PATH_PAPER"),         # <Your pdf file>
        code_fdir=os.getenv("ORATOR_PATH_CODE"),
        embedding_model=emb_model,
        language_model=llm
    )

    translate_prompt = ChatPromptTemplate.from_messages(
        [
            ("user", """Please translate the given raw sentence into {language}. Please return the translation result directly in the target language without any additional explanatory information.
            
            Raw Sentence: {greeting}
            Translated Sentence: """)
        ]
    )
    greet_translator = translate_prompt | llm | StrOutputParser()

    with gr.Blocks(theme=gr.themes.Soft(), css="footer {visibility: hidden}") as demo:

        title_html = gr.HTML(
            make_title(os.getenv("ORATOR_TITLE"), os.getenv("ORATOR_AUTHOR"), os.getenv("ORATOR_DETAILED_INFO")))

        with gr.Row():
            with gr.Column(scale=1):
                target_lang = gr.Dropdown(value="简体中文 (ZH-CN)", choices=SUPPORTED_LANG, label="Language Setting")
                # start_btn = gr.Button("Change Language", variant="primary")

                if os.getenv("ORATOR_SHARELINK_CODE"):
                    gr.Markdown(f"💻**Code**: [[url]({os.getenv('ORATOR_SHARELINK_CODE')})]")
                if os.getenv("ORATOR_SHARELINK_PAPER"):
                    gr.Markdown(f"📄**Paper**: [[url]({os.getenv('ORATOR_SHARELINK_PAPER')})]")
                if os.getenv("ORATOR_SHARELINK_DATASET"):
                    gr.Markdown(f"🔗**Dataset**: [[url]({os.getenv('ORATOR_SHARELINK_DATASET')})]")

            with gr.Column(scale=2):
                chatbot = gr.Chatbot(label=f"""{os.getenv("ORATOR_AGENT_NAME")}""", height=750, value=[(None, os.getenv("ORATOR_GREETING").format(name=os.getenv("ORATOR_AGENT_NAME"), title=os.getenv("ORATOR_TITLE")))])
                user_input = gr.Textbox(show_label=False, interactive=True, placeholder="Start chatting...")

        target_lang.change(change_lang, inputs=[target_lang], outputs=[chatbot])
        user_input.submit(update_history, inputs=[user_input, chatbot],
                          outputs=[user_input, chatbot]).then(chat, inputs=[chatbot, target_lang], outputs=[chatbot])

    demo.launch(server_name=os.getenv("ORATOR_SERVER_HOST"), server_port=int(os.getenv("ORATOR_SERVER_PORT")))

