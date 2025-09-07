STRUCTURED_INFO_EXTRACTION_TOOL = {
    "type": "function",
    "function": {
        "name": "structured_info_extraction",
        "description": "Extract structured information from text. Extracts the title of the text, a brief summary, sentiment (positive, negative, neutral) and topics discussed. Use this to extract structured information from articles, documents, or any text content.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the text. If the text does not have a title, return an empty string.",
                },
                "summary": {
                    "type": "string",
                    "description": "A brief summary of the text, capturing the main points and essence of the content.",
                },
                "sentiment": {
                    "type": "string",
                    "enum": ["positive", "negative", "neutral"],
                    "description": "The overall sentiment of the text. Should be one of: positive, negative, neutral.",
                },
                "topics": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "A list of main topics discussed in the text.",
                },
            },
            "required": ["title", "summary", "sentiment", "topics"],
            "additionalProperties": False,
        },
    },
}
