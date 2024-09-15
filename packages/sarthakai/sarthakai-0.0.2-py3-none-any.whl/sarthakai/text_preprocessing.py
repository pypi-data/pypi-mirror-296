from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 500


def recursive_chunking(document: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )

    texts = text_splitter.create_documents([document])
    return [text.page_content for text in texts]


def trim_llm_messages_history(messages, max_length=4096):
    if len("".join([str(message["content"]) for message in messages])) > max_length:
        messages = messages[1:]
        return trim_llm_messages_history(messages)
    else:
        return messages
