# coding=utf-8
# Copyright 2018 The Google AI Language Team Authors and The HuggingFace Inc. team.
# Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Masked BERT model configuration. It replicates the class `~transformers.BertConfig`
and adapts it to the specificities of MaskedBert (`pruning_method`, `mask_init` and `mask_scale`."""


import logging

from transformers.configuration_utils import PretrainedConfig

logger = logging.getLogger(__name__)


class MaskedBertConfig(PretrainedConfig):
    """
    A class replicating the `~transformers.BertConfig` with additional parameters for pruning/masking configuration.
    """

    model_type = "masked_bert"

    def __init__(
        self,
        vocab_size=30522,
        hidden_size=768,
        num_hidden_layers=12,
        num_attention_heads=12,
        intermediate_size=3072,
        hidden_act="gelu",
        hidden_dropout_prob=0.1,
        attention_probs_dropout_prob=0.1,
        max_position_embeddings=512,
        type_vocab_size=2,
        initializer_range=0.02,
        layer_norm_eps=1e-12,
        pad_token_id=0,
        pruning_method="topK",
        mask_init="constant",
        mask_scale=0.0,
        mask_block_rows=1,
        mask_block_cols=1,
        ampere_pruning_method: str = None,
        ampere_mask_init: str = "constant",
        ampere_mask_scale: float = 0.0,
        shuffling_method: str = None,
        in_shuffling_group: int = 4,
        out_shuffling_group: int = 4,
        num_splopa_prototypes: int = 64,
        splopa_prototype_rank: int = 1,
        shared_splopa_prototypes: bool = True,
        shared_splopa_pos_weights: bool = False,
        splopa_init_range: float = 1e-4,
        **kwargs,
    ):
        super().__init__(pad_token_id=pad_token_id, **kwargs)

        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.hidden_act = hidden_act
        self.intermediate_size = intermediate_size
        self.hidden_dropout_prob = hidden_dropout_prob
        self.attention_probs_dropout_prob = attention_probs_dropout_prob
        self.max_position_embeddings = max_position_embeddings
        self.type_vocab_size = type_vocab_size
        self.initializer_range = initializer_range
        self.layer_norm_eps = layer_norm_eps
        self.pruning_method = pruning_method
        self.mask_init = mask_init
        self.mask_scale = mask_scale
        self.mask_block_rows = mask_block_rows
        self.mask_block_cols = mask_block_cols
        self.ampere_pruning_method = ampere_pruning_method
        self.ampere_mask_init = ampere_mask_init
        self.ampere_mask_scale = ampere_mask_scale
        self.shuffling_method = shuffling_method
        self.in_shuffling_group = in_shuffling_group
        self.out_shuffling_group = out_shuffling_group
        self.num_splopa_prototypes = num_splopa_prototypes
        self.splopa_prototype_rank = splopa_prototype_rank
        self.shared_splopa_prototypes = shared_splopa_prototypes
        self.shared_splopa_pos_weights = shared_splopa_pos_weights
        self.splopa_init_range = splopa_init_range
