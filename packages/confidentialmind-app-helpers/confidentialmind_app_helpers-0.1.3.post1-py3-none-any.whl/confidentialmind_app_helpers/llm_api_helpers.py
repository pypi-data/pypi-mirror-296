from typing import Literal, Optional, List
import requests
from .streaming import parse_stream

from confidentialmind_core.config_manager import (
    load_environment,
    get_api_parameters,
)


class ChatMessage:
    """
    Represents a chat message in the context of an AI assistant.

    Attributes:
        role (Literal["user", "assistant", "system"]): The role associated with the message.
            Typically, the system message is optional and the order must be: system, user, assistant, user, assistant, ...
        content (str): The text content of the message.
    """

    def __init__(self, role: Literal["user", "assistant", "system"], content: str):
        self.role = role
        self.content = content


class LLMAPIHandler:
    """
    Handles API interactions for a language model.

    Attributes:
        config_id (str): The identifier of the LLM connector to use.
        embedding_id (Optional[str]): The identifier of the embedding connector, if any.

    Methods:
        handle_query: Processes and sends chat messages to an LLM endpoint for completion.
    """

    def __init__(self, config_id: str, embedding_id=None):
        self.config_id = config_id
        self.embedding_id = embedding_id

        load_environment()

    # TODO: define the handle_query method to use at initialization
    def handle_query(
        self,
        messages: list[ChatMessage],
        token_callback: Optional[callable] = None,
        temperature: float = 0.7,
        top_p: Optional[float] = 0.95,
        max_tokens: Optional[int] = None,
        stream: bool = True,
        return_full_response: bool = False,
    ):
        """
        Handles a query by sending it to the LLM service and processing the response.

        Args:
            messages (list[ChatMessage]): List of chat messages representing the conversation.
            token_callback (Optional[callable], optional): The callback function for handling tokens in streaming responses. Defaults to None.
            temperature (float, optional): Sampling temperature for text generation. Defaults to 0.7.
            top_p (float, optional): Model considers the results of the tokens with top_p probability mass. Defaults to 0.95.
            max_tokens (Optional[int], optional): Maximum number of tokens in the generated response. Defaults to None.
            stream (bool, optional): Whether to enable streaming mode for receiving results. Defaults to True.
            return_full_response (bool, optional): Whether to return full response as a second return value. Defaults to False.

        Returns:
            str: The LLM's response as a string.
            json: If return_full_response is True, returns JSON object containing the full response from LLM.

        """

        print("CALLING HANDLE QUERY")

        url_base, headers = get_api_parameters(self.config_id)

        url = url_base + "/v1/chat/completions"

        # TODO embedding service should be handled separately and the context should be passed to the function
        url_base_embedding, headers_embedding = get_api_parameters(self.embedding_id)
        if url_base_embedding is not None:
            # create url
            url_embeddings = url_base_embedding + "/query"
            # body: query: str, top_k: int optional
            # fetch
            # TODO make function async
            results = requests.post(
                url_embeddings,
                json={"query": messages[-1].content},
                headers=headers_embedding,
            )
            # parse results
            # TODO read this correctly
            # print(results.json())
            results_to_loop = results.json()["results"]["results"]
            # Add results to last message
            if len(results_to_loop) > 0:
                string_to_add = "\n\nHere are references which to use when answering to the question:\n"
                for result in results_to_loop:
                    print(result)
                    array_str = [str(x) for x in result["sql_metadata"]["pages"]]
                    string_to_add += (
                        "source file: "
                        + result["sql_metadata"]["filename"]
                        + " . source pages: "
                        + ".".join(array_str)
                        + " result score: "
                        + str(result["score"])
                        + "\n\n"
                    )
                    string_to_add += result["sql_metadata"]["text"] + "\n\n"
                string_to_add += "\n\n  Include the source file, source page and result score in your answer."

                messages[-1].content += string_to_add
        else:
            print("No config for embedding service")

        response = get_response(
            messages,
            url,
            headers=headers,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            stream=stream,
        )
        if stream:
            answer = parse_stream(response, token_callback)
        else:
            res = response.json()
            answer = res["choices"][0]["message"]["content"]
            if token_callback:
                token_callback(answer)
            if return_full_response:
                return answer, res
        return answer

    def handle_embedding(
        self,
        texts: list[str],
    ):
        print("CALLING HANDLE EMBEDDING")

        url_base, headers = get_api_parameters(self.config_id)

        if url_base is None:
            print("No config for embedding service")

        url = url_base + "/v1/embeddings"

        return get_embeddings(texts, url, headers)


def get_response(
    messages: list[ChatMessage],
    url: str,
    headers: dict = {},
    temperature: float = 0.7,
    top_p: Optional[float] = 0.95,
    max_tokens: Optional[int] = None,
    stream: bool = True,
):
    """
    Sends a request to the LLM API and returns the response.

    Args:
        messages (list[ChatMessage]): List of chat messages representing the conversation.
        url (str): The URL endpoint for the LLM service.
        apikey (str): Optional API key.
        temperature (float, optional): Sampling temperature for text generation. Defaults to 0.7.
        top_p (float, optional): Model considers the results of the tokens with top_p probability mass. Defaults to 0.95.
        max_tokens (Optional[int], optional): Maximum number of tokens in the generated response. Defaults to None.
        stream (bool, optional): Whether to enable streaming mode for receiving results. Defaults to True.

    Returns:
        requests.Response: The raw response object from the API call.
    """

    final_headers = {"Content-Type": "application/json"} | headers

    parsed_messages = [obj.__dict__ for obj in messages]
    jsonBody = {
        "messages": parsed_messages,
        "temperature": temperature,
        "top_p": top_p,
        "stream": stream,
        "model": "cm-llm",  # Hardcoded model for vllm; ignored by our proxy
    }
    if max_tokens:
        jsonBody["max_tokens"] = max_tokens
    res = requests.post(
        url,
        json=jsonBody,
        stream=stream,
        headers=final_headers,
    )
    if res.status_code != 200:
        raise Exception(f"LLM request returned status code {res.status_code}.")

    return res


# Original version of this was copied from apis/rag-service/services/embeddings.py
def get_embeddings(
    texts: List[str],
    url: str,
    headers: dict = {},
) -> List[List[float]]:
    """
    Embed texts using Connected Embedding service.

    Args:
        texts: The list of texts to embed.
        url (str): The URL endpoint for the LLM service.
        apikey (str): Optional API key.

    Returns:
        A list of embeddings, each of which is a list of floats.

    Raises:
        Exception: If the HTTP call fails.
    """
    # if url is None:
    #    raise Exception("No embedding connector found")

    final_headers = {"Content-Type": "application/json"} | headers

    print(f"Calling Embedding service with {url}")
    # Call the Connected Embedding service
    try:
        response = requests.post(
            url,
            headers=final_headers,
            json={
                "input": texts,
            },
        )
        if response.status_code == 200:
            data = response.json()
            embeddings = [item["embedding"] for item in data["data"]]
            return embeddings
        else:
            raise Exception(
                f"Embedding request returned status code {response.status_code}."
            )
    except Exception as e:
        print(e)
        raise Exception(f"Error calling Embedding service: {e}")
