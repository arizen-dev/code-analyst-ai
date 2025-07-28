import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import re
import chainlit as cl
from analyzer import GitHubRepoAnalyzer

def is_github_url(url):
    """Checks if the provided text is a valid GitHub repository URL."""
    return re.match(r'https?://github\.com/[\w-]+/[\w.-]+/?', url) is not None

@cl.on_chat_start
async def on_chat_start():
    # Check for required API keys at the start of the chat
    if not os.environ.get("OPENAI_API_KEY") or not os.environ.get("OPENROUTER_API_KEY"):
        await cl.Message(
            content="API keys are not configured. Please set `OPENAI_API_KEY` and `OPENROUTER_API_KEY` in your `.env` file."
        ).send()
        return

    await cl.Message(
        content="Hello! I can analyze a GitHub repository for you. Please provide a public GitHub URL to begin."
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    if cl.user_session.get("analyzer") is None:
        if not is_github_url(message.content):
            await cl.Message(content="That doesn't look like a GitHub repository URL. Please provide a valid URL.").send()
            return
        
        repo_url = message.content
        loading_msg = cl.Message(content=f"Cloning `{repo_url}` and starting analysis... This may take a few minutes.")
        await loading_msg.send()

        try:
            analyzer = GitHubRepoAnalyzer()
            cl.user_session.set("analyzer", analyzer)

            status = cl.Step(name="Cloning repository...", type="run")
            await status.send()
            success, status_message = analyzer.clone_repo(repo_url)
            if not success:
                await cl.Message(content=status_message).send()
                analyzer.cleanup()
                cl.user_session.set("analyzer", None)
                return
            status.output = status_message
            await status.update()
            
            status = cl.Step(name="Indexing codebase...", type="run")
            await status.send()
            analyzer.load_and_index_files()
            status.output = "Codebase indexed successfully."
            await status.update()

            status = cl.Step(name="Performing high-level analysis...", type="run")
            await status.send()
            initial_analysis = await analyzer.get_initial_analysis()
            await cl.Message(content=initial_analysis, author="Initial Analysis").send()
            status.output = "Analysis complete."
            await status.update()
            
            loading_msg.content = f"Repository analysis complete! You can now ask questions about the code."
            await loading_msg.update()

        except Exception as e:
            await cl.Message(content=f"A critical error occurred: {str(e)}").send()
            if cl.user_session.get("analyzer"):
                cl.user_session.get("analyzer").cleanup()
            cl.user_session.set("analyzer", None)
    else:
        analyzer = cl.user_session.get("analyzer")
        rag_chain = analyzer.get_rag_chain()
        
        response_msg = cl.Message(content="")
        await response_msg.send()

        async for chunk in rag_chain.astream(message.content):
            await response_msg.stream_token(chunk.content)
        await response_msg.update()

@cl.on_chat_end
def on_chat_end():
    analyzer = cl.user_session.get("analyzer")
    if analyzer:
        analyzer.cleanup()