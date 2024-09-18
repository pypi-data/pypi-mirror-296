from __future__ import annotations

import random
import re
from typing import Any

import torch
from deep_translator.exceptions import NotValidLength, RequestError, TooManyRequests, TranslationNotFound

from textmentations.augmentations.utils import (
    _squeeze_first,
    autopsy_sentence,
    autopsy_text,
    get_translator,
    join_words_into_sentence,
    pass_empty_text,
)
from textmentations.corpora.types import Language, Sentence, Text, Word


@pass_empty_text
def back_translate(text: Text, from_lang: Language, to_lang: Language) -> Text:
    """Back-translates the text by translating it to the target language and then back to the original.

    Args:
        text: The input text.
        from_lang: The language of the input text.
        to_lang: The language to which the input text will be translated.

    Returns:
        A back-translated text.

    Examples:
        >>> import textmentations.augmentations.generation.functional as fg
        >>> text = "짜장면을 맛있게 먹었다. 짬뽕도 맛있게 먹었다. 짬짜면도 먹고 싶었다."
        >>> from_lang = "ko"
        >>> to_lang = "en"
        >>> augmented_text = fg.back_translate(text, from_lang, to_lang)
    """
    try:
        translator = get_translator()
        translator.source, translator.target = from_lang, to_lang
        translated_text = translator.translate(text)
        translator.source, translator.target = to_lang, from_lang
        back_translated_text = translator.translate(translated_text)
        return back_translated_text
    except (NotValidLength, RequestError, TooManyRequests, TranslationNotFound):
        return text


@pass_empty_text
def iterative_mask_fill(text: Text, model: Any, tokenizer: Any, top_k: int, device: str | torch.device) -> Text:
    """Iteratively masks words in a randomly selected sentence and replaces them with language model predictions.

    Args:
        text: The input text.
        model: The masked language model used for making predictions.
        tokenizer: The tokenizer that will be used to encode text for the model and decode the model's output.
        top_k: The number of candidate words to replace the masked word at each iteration
        device: The device to use for computation (e.g., "cpu", "cuda:1", torch.device("cuda")).

    Returns:
        A augmented text.

    Examples:
        >>> import textmentations.augmentations.generation.functional as fg
        >>> from transformers import AutoModelForMaskedLM, AutoTokenizer
        >>> text = "짜장면을 맛있게 먹었다. 짬뽕도 맛있게 먹었다. 짬짜면도 먹고 싶었다."
        >>> pretrained_model_name_or_path = "Pre-trained huggingface masked language model name or path you want to use"
        >>> model = AutoModelForMaskedLM.from_pretrained(pretrained_model_name_or_path)
        >>> tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path)
        >>> top_k = 5
        >>> device = "cuda:0"
        >>> augmented_text = fg.iterative_mask_fill(text, model, tokenizer, top_k, device)
    """
    model.to(device)
    augmented_text = _iterative_mask_fill(text, model, tokenizer, top_k, device)
    augmented_text = re.sub(r"\s*##\b", "", augmented_text)  # e.g., 나는 짬뽕 ##을 먹었다. -> 나는 짬뽕을 먹었다.
    return augmented_text


@autopsy_text
def _iterative_mask_fill(
    sentences: list[Sentence],
    model: Any,
    tokenizer: Any,
    top_k: int,
    device: str | torch.device,
) -> list[Sentence]:
    num_sentences = len(sentences)
    index = random.randrange(0, num_sentences)
    sentence = sentences[index]
    sentences[index] = _iterative_mask_fill_in_sentence(sentence, model, tokenizer, top_k, device)
    return sentences


@autopsy_sentence
def _iterative_mask_fill_in_sentence(
    words: list[Word],
    model: Any,
    tokenizer: Any,
    top_k: int,
    device: str | torch.device,
) -> list[Word]:
    for masking_index, word in enumerate(words):
        words[masking_index] = tokenizer.mask_token
        sentence = join_words_into_sentence(words)
        plausible_words = _predict_mask(sentence, model, tokenizer, top_k, device)
        if not plausible_words:
            words[masking_index] = word
            continue
        plausible_word = _squeeze_first(plausible_words)
        words[masking_index] = plausible_word
    return words


def _predict_mask(sentence: Sentence, model: Any, tokenizer: Any, top_k: int, device: str | torch.device) -> list[Word]:
    mask_token_id = tokenizer.mask_token_id
    input_ids = tokenizer.encode(sentence, truncation=True, return_tensors="pt")
    if mask_token_id not in input_ids:
        return []
    input_ids = input_ids.to(device)
    with torch.no_grad():
        mlm_output = model(input_ids)
    mask_tokens_index = torch.where(input_ids.eq(mask_token_id))
    topk = mlm_output.logits[mask_tokens_index].cpu().topk(top_k)
    token_ids_list, scores_list = topk.indices.tolist(), topk.values.tolist()
    token_ids_to_decode = []
    for token_ids, scores in zip(token_ids_list, scores_list):
        token_id = _squeeze_first(random.choices(token_ids, weights=scores, k=1))
        token_ids_to_decode.append(token_id)
    plausible_words = [tokenizer.decode(token_id) for token_id in token_ids_to_decode]
    return plausible_words
