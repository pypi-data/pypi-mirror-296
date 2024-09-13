from __future__ import annotations
import math
from collections import namedtuple
import torch
import gc
import re

re_attention = re.compile(r"""
\\\(|
\\\{|
\\\)|
\\\}|
\\\[|
\\]|
\\\\|
\\|
\(|
\{|
\[|
:([+-]?[.\d]+)\)|
\)|
\}|
]|
[^\\()\\{}\[\]:]+|
:
""", re.X)


def parse_prompt_attention(text):
    res = []
    round_brackets = []
    square_brackets = []

    round_bracket_multiplier = 1.1
    square_bracket_multiplier = 1 / 1.1

    def multiply_range(start_position, multiplier):
        for p in range(start_position, len(res)):
            res[p][1] *= multiplier

    for m in re_attention.finditer(text):
        text = m.group(0)
        weight = m.group(1)

        if text.startswith('\\'):
            res.append([text[1:], 1.0])
        elif text == '(' or text == '{':
            round_brackets.append(len(res))
        elif text == '[':
            square_brackets.append(len(res))
        elif weight is not None and len(round_brackets) > 0:
            multiply_range(round_brackets.pop(), float(weight))
        elif (text == ')' or text == '}') and len(round_brackets) > 0:
            multiply_range(round_brackets.pop(), round_bracket_multiplier)
        elif text == ']' and len(square_brackets) > 0:
            multiply_range(square_brackets.pop(), square_bracket_multiplier)
        else:
            res.append([text, 1.0])

    for pos in round_brackets:
        multiply_range(pos, round_bracket_multiplier)

    for pos in square_brackets:
        multiply_range(pos, square_bracket_multiplier)

    if len(res) == 0:
        res = [["", 1.0]]

    # merge runs of identical weights
    i = 0
    while i + 1 < len(res):
        if res[i][1] == res[i + 1][1]:
            res[i][0] += res[i + 1][0]
            res.pop(i + 1)
        else:
            i += 1

    return res


class Emphasis:
    """Emphasis class decides how to death with (emphasized:1.1) text in prompts"""

    name: str = "Base"
    description: str = ""

    tokens: list[list[int]]
    """tokens from the chunk of the prompt"""

    multipliers: torch.Tensor
    """tensor with multipliers, once for each token"""

    z: torch.Tensor
    """output of cond transformers network (CLIP)"""

    def after_transformers(self):
        """Called after cond transformers network has processed the chunk of the prompt; this function should modify self.z to apply the emphasis"""

        pass


class EmphasisNone(Emphasis):
    name = "None"
    description = "disable the mechanism entirely and treat (:.1.1) as literal characters"


class EmphasisIgnore(Emphasis):
    name = "Ignore"
    description = "treat all empasised words as if they have no emphasis"


class EmphasisOriginal(Emphasis):
    name = "Original"
    description = "the original emphasis implementation"

    def after_transformers(self):
        original_mean = self.z.mean()
        self.z = self.z * self.multipliers.reshape(self.multipliers.shape + (1,)).expand(self.z.shape)

        # restoring original mean is likely not correct, but it seems to work well to prevent artifacts that happen otherwise
        new_mean = self.z.mean()
        self.z = self.z * (original_mean / new_mean)


class EmphasisOriginalNoNorm(EmphasisOriginal):
    name = "No norm"
    description = "same as original, but without normalization (seems to work better for SDXL)"

    def after_transformers(self):
        self.z = self.z * self.multipliers.reshape(self.multipliers.shape + (1,)).expand(self.z.shape)


def get_current_option(emphasis_option_name):
    return next(iter([x for x in options if x.name == emphasis_option_name]), EmphasisOriginal)


def get_options_descriptions():
    return ", ".join(f"{x.name}: {x.description}" for x in options)


options = [
    EmphasisNone,
    EmphasisIgnore,
    EmphasisOriginal,
    EmphasisOriginalNoNorm,
]


class PromptChunk:
    """
    This object contains token ids, weight (multipliers:1.4) and textual inversion embedding info for a chunk of prompt.
    If a prompt is short, it is represented by one PromptChunk, otherwise, multiple are necessary.
    Each PromptChunk contains an exact amount of tokens - 77, which includes one for start and end token,
    so just 75 tokens from prompt.
    """

    def __init__(self):
        self.tokens = []
        self.multipliers = []
        self.fixes = []


PromptChunkFix = namedtuple('PromptChunkFix', ['offset', 'embedding'])
"""An object of this type is a marker showing that textual inversion embedding's vectors have to placed at offset in the prompt
chunk. Those objects are found in PromptChunk.fixes and, are placed into FrozenCLIPEmbedderWithCustomWordsBase.hijack.fixes, and finally
are applied by sd_hijack.EmbeddingsWithFixes's forward function."""


class FrozenCLIPEmbedderWithCustomWordsBase(torch.nn.Module):
    """A pytorch module that is a wrapper for FrozenCLIPEmbedder module. it enhances FrozenCLIPEmbedder, making it possible to
    have unlimited prompt length and assign weights to tokens in prompt.
    """

    def __init__(self, wrapped):
        super().__init__()

        self.wrapped = wrapped
        """Original FrozenCLIPEmbedder module; can also be FrozenOpenCLIPEmbedder or xlmr.BertSeriesModelWithTransformation,
        depending on model."""

        # self.hijack: sd_hijack.StableDiffusionModelHijack = hijack
        self.chunk_length = 75

        self.is_trainable = getattr(wrapped, 'is_trainable', False)
        self.input_key = getattr(wrapped, 'input_key', 'txt')
        self.legacy_ucg_val = None

    def empty_chunk(self):
        """creates an empty PromptChunk and returns it"""

        chunk = PromptChunk()
        chunk.tokens = [self.id_start] + [self.id_end] * (self.chunk_length + 1)
        chunk.multipliers = [1.0] * (self.chunk_length + 2)
        return chunk

    def get_target_prompt_token_count(self, token_count):
        """returns the maximum number of tokens a prompt of a known length can have before it requires one more PromptChunk to be represented"""

        return math.ceil(max(token_count, 1) / self.chunk_length) * self.chunk_length

    def tokenize(self, texts):
        """Converts a batch of texts into a batch of token ids"""

        raise NotImplementedError

    def encode_with_transformers(self, tokens):
        """
        converts a batch of token ids (in python lists) into a single tensor with numeric representation of those tokens;
        All python lists with tokens are assumed to have same length, usually 77.
        if input is a list with B elements and each element has T tokens, expected output shape is (B, T, C), where C depends on
        model - can be 768 and 1024.
        Among other things, this call will read self.hijack.fixes, apply it to its inputs, and clear it (setting it to None).
        """

        raise NotImplementedError

    def encode_embedding_init_text(self, init_text, nvpt):
        """Converts text into a tensor with this text's tokens' embeddings. Note that those are embeddings before they are passed through
        transformers. nvpt is used as a maximum length in tokens. If text produces less teokens than nvpt, only this many is returned."""

        raise NotImplementedError

    def tokenize_line(self, line):

        if self.emphasis != "None":
            parsed = parse_prompt_attention(line)
        else:
            parsed = [[line, 1.0]]
        # print(parsed)

        tokenized = self.tokenize([text for text, _ in parsed])

        chunks = []
        chunk = PromptChunk()
        token_count = 0
        last_comma = -1

        def next_chunk(is_last=False):
            """puts current chunk into the list of results and produces the next one - empty;
            if is_last is true, tokens <end-of-text> tokens at the end won't add to token_count"""
            nonlocal token_count
            nonlocal last_comma
            nonlocal chunk

            if is_last:
                token_count += len(chunk.tokens)
            else:
                token_count += self.chunk_length

            to_add = self.chunk_length - len(chunk.tokens)
            if to_add > 0:
                chunk.tokens += [self.id_end] * to_add
                chunk.multipliers += [1.0] * to_add

            chunk.tokens = [self.id_start] + chunk.tokens + [self.id_end]
            chunk.multipliers = [1.0] + chunk.multipliers + [1.0]

            last_comma = -1
            chunks.append(chunk)
            chunk = PromptChunk()

        for tokens, (text, weight) in zip(tokenized, parsed):
            if text == 'BREAK' and weight == -1:
                next_chunk()
                continue

            position = 0
            while position < len(tokens):
                token = tokens[position]

                if token == self.comma_token:
                    last_comma = len(chunk.tokens)

                # this is when we are at the end of allotted 75 tokens for the current chunk, and the current token is not a comma. opts.comma_padding_backtrack
                # is a setting that specifies that if there is a comma nearby, the text after the comma should be moved out of this chunk and into the next.
                elif self.comma_padding_backtrack != 0 and len(chunk.tokens) == self.chunk_length and last_comma != -1 and len(chunk.tokens) - last_comma <= self.comma_padding_backtrack:
                    break_location = last_comma + 1

                    reloc_tokens = chunk.tokens[break_location:]
                    reloc_mults = chunk.multipliers[break_location:]

                    chunk.tokens = chunk.tokens[:break_location]
                    chunk.multipliers = chunk.multipliers[:break_location]

                    next_chunk()
                    chunk.tokens = reloc_tokens
                    chunk.multipliers = reloc_mults

                if len(chunk.tokens) == self.chunk_length:
                    next_chunk()

                chunk.tokens.append(token)
                chunk.multipliers.append(weight)
                position += 1
                continue

        if chunk.tokens or not chunks:
            next_chunk(is_last=True)

        return chunks, token_count

    def process_texts(self, texts):

        token_count = 0

        cache = {}
        batch_chunks = []
        for line in texts:
            if line in cache:
                chunks = cache[line]
            else:
                chunks, current_token_count = self.tokenize_line(line)
                token_count = max(current_token_count, token_count)

                cache[line] = chunks

            batch_chunks.append(chunks)

        return batch_chunks, token_count

    def forward(self, texts, get_pooled=False):
        self.get_pooled = get_pooled

        if isinstance(texts, str):
            texts = [texts]
        # print("starting forward")
        # print(texts)

        batch_chunks, token_count = self.process_texts(texts)

        chunk_count = max([len(x) for x in batch_chunks])

        zs = []
        for i in range(chunk_count):
            batch_chunk = [chunks[i] if i < len(chunks) else self.empty_chunk() for chunks in batch_chunks]

            tokens = [x.tokens for x in batch_chunk]
            multipliers = [x.multipliers for x in batch_chunk]

            z = self.process_tokens(tokens, multipliers)
            zs.append(z)

        if self.get_pooled:  # hasattr(zs, "pooled"): # if zs.shape[-1] == 1280:
            return torch.hstack(zs), zs[0].pooled  # self.pooled
        else:
            return torch.hstack(zs)

    def process_tokens(self, remade_batch_tokens, batch_multipliers):
        tokens = torch.asarray(remade_batch_tokens).to(self.device)

        # this is for SD2: SD1 uses the same token for padding and end of text, while SD2 uses different ones.
        if self.id_end != self.id_pad:
            for batch_pos in range(len(remade_batch_tokens)):
                index = remade_batch_tokens[batch_pos].index(self.id_end)
                tokens[batch_pos, index+1:tokens.shape[1]] = self.id_pad

        if hasattr(self.wrapped, "text_encoder_2"):
            z, pooled = self.encode_with_transformers_xl(tokens)
        else:
            z, pooled = self.encode_with_transformers(tokens)

        emphasis = get_current_option(self.emphasis)()
        emphasis.tokens = remade_batch_tokens
        emphasis.multipliers = torch.asarray(batch_multipliers).to(self.device)
        emphasis.z = z

        emphasis.after_transformers()

        z = emphasis.z

        if pooled is not None:
            z.pooled = pooled

        return z


class StableDiffusionLongPromptProcessor(FrozenCLIPEmbedderWithCustomWordsBase):
    def __init__(self, wrapped, tokenizer_1, text_encoder_1, clip_skip=2, emphasis="Original", comma_padding_backtrack=20):
        super().__init__(wrapped)
        self.device = wrapped.device
        self.tokenizer = tokenizer_1
        self.text_encoder = text_encoder_1
        self.get_pooled = False
        if hasattr(wrapped, "text_encoder_2"):
            self.layer = "hidden"
            self.layer_idx = 11

        self.emphasis = emphasis
        self.CLIP_stop_at_last_layers = clip_skip
        self.comma_padding_backtrack = comma_padding_backtrack

        vocab = self.tokenizer.get_vocab()

        self.comma_token = vocab.get(',</w>', None)

        self.token_mults = {}
        tokens_with_parens = [(k, v) for k, v in vocab.items() if '(' in k or ')' in k or '[' in k or ']' in k]
        for text, ident in tokens_with_parens:
            mult = 1.0
            for c in text:
                if c == '[':
                    mult /= 1.1
                if c == ']':
                    mult *= 1.1
                if c == '(':
                    mult *= 1.1
                if c == ')':
                    mult /= 1.1

            if mult != 1.0:
                self.token_mults[ident] = mult

        self.id_start = self.wrapped.tokenizer.bos_token_id
        self.id_end = self.wrapped.tokenizer.eos_token_id
        self.id_pad = self.id_end

    def tokenize(self, texts):
        tokenized = self.wrapped.tokenizer(texts, truncation=False, add_special_tokens=False)["input_ids"]

        return tokenized

    # sd1.5
    def encode_with_transformers(self, tokens):
        outputs = self.text_encoder(input_ids=tokens, output_hidden_states=-self.CLIP_stop_at_last_layers)

        if self.CLIP_stop_at_last_layers > 1:
            z = outputs.hidden_states[-self.CLIP_stop_at_last_layers]
            z = self.text_encoder.text_model.final_layer_norm(z)
        else:
            z = outputs.last_hidden_state

        return z, None  # no pooled

    # sdxl no clip skip
    def encode_with_transformers_xl(self, tokens):
        outputs = self.text_encoder(input_ids=tokens, output_hidden_states=self.layer == "hidden")

        pooled = None
        if outputs[0].shape[-1] == 1280:
            pooled = outputs[0]

        if self.layer == "last":
            z = outputs.last_hidden_state
        else:
            z = outputs.hidden_states[self.layer_idx]

        return z, pooled


def text_embeddings_equal_len(text_embedder, prompt, negative_prompt, get_pooled=False):
    pooled_cond = pooled_neg_cond = None

    cond_embeddings = text_embedder(prompt, get_pooled)
    uncond_embeddings = text_embedder(negative_prompt, get_pooled)

    if isinstance(cond_embeddings, tuple):
        cond_embeddings, pooled_cond = cond_embeddings[0], cond_embeddings[1]
        uncond_embeddings, pooled_neg_cond = uncond_embeddings[0], uncond_embeddings[1]

    cond_len = cond_embeddings.shape[1]
    uncond_len = uncond_embeddings.shape[1]
    # print(cond_embeddings.shape, uncond_embeddings.shape)
    if cond_len == uncond_len:
        all_embeddings = [cond_embeddings, uncond_embeddings]
    else:
        if cond_len > uncond_len:
            n = (cond_len - uncond_len) // 77
            all_embeddings = [cond_embeddings, torch.cat([uncond_embeddings] + [text_embedder([""])]*n, dim=1)]
        else:
            n = (uncond_len - cond_len) // 77
            all_embeddings = [torch.cat([cond_embeddings] + [text_embedder([""])]*n, dim=1), uncond_embeddings]

    if get_pooled:
        return all_embeddings + [pooled_cond, pooled_neg_cond]
    else:
        return all_embeddings


def long_prompts_with_weighting(pipe, prompt, negative_prompt, clip_skip=2, emphasis="Original", comma_padding_backtrack=20):
    text_embedder = StableDiffusionLongPromptProcessor(
        pipe,
        pipe.tokenizer,
        pipe.text_encoder,
        clip_skip,
        emphasis,
        comma_padding_backtrack
    )

    cond_embeddings, uncond_embeddings = text_embeddings_equal_len(text_embedder, prompt, negative_prompt)

    if not hasattr(pipe, "text_encoder_2"):
        torch.cuda.empty_cache()
        gc.collect()
        return cond_embeddings, uncond_embeddings

    text_embedder_2 = StableDiffusionLongPromptProcessor(
        pipe,
        pipe.tokenizer_2,
        pipe.text_encoder_2,
        clip_skip,
        emphasis,
        comma_padding_backtrack
    )

    (
        cond_embeddings_2,
        uncond_embeddings_2,
        cond_pooled,
        uncond_pooled
    ) = text_embeddings_equal_len(text_embedder_2, prompt, negative_prompt, get_pooled=True)

    cond_embed = torch.cat((cond_embeddings, cond_embeddings_2), dim=2)
    neg_uncond_embed = torch.cat((uncond_embeddings, uncond_embeddings_2), dim=2)

    torch.cuda.empty_cache()
    gc.collect()

    return [cond_embed, cond_pooled], [neg_uncond_embed, uncond_pooled]
