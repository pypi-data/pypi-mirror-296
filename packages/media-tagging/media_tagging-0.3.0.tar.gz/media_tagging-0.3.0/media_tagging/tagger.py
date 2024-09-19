# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Module for performing media tagging.

Media tagging sends API requests to tagging engine (i.e. Google Vision API)
and returns tagging results that can be easily written.
"""

import logging
import os
from collections.abc import Sequence

from media_tagging import utils
from media_tagging.taggers import api, base, llm

_TAGGERS = {
  'vision-api': api.GoogleVisionAPITagger,
  'video-api': api.GoogleVideoIntelligenceAPITagger,
  'gemini-image': llm.GeminiImageTagger,
  'gemini-structured-image': llm.GeminiImageTagger,
  'gemini-description-image': llm.GeminiImageTagger,
  'gemini-video': llm.GeminiVideoTagger,
  'gemini-structured-video': llm.GeminiVideoTagger,
  'gemini-description-video': llm.GeminiVideoTagger,
}

_LLM_TAGGERS_TYPES = {
  'gemini-image': llm.LLMTaggerTypeEnum.UNSTRUCTURED,
  'gemini-structured-image': llm.LLMTaggerTypeEnum.STRUCTURED,
  'gemini-description-image': llm.LLMTaggerTypeEnum.DESCRIPTION,
  'gemini-video': llm.LLMTaggerTypeEnum.UNSTRUCTURED,
  'gemini-structured-video': llm.LLMTaggerTypeEnum.STRUCTURED,
  'gemini-description-video': llm.LLMTaggerTypeEnum.DESCRIPTION,
}


def create_tagger(
  tagger_type: str, tagger_parameters: dict[str, str] | None = None
) -> base.BaseTagger:
  """Factory for creating taggers based on provided type.

  Args:
    tagger_type: Type of tagger.
    tagger_parameters: Various parameters to instantiate tagger.

  Returns:
    Concrete tagger class.
  """
  if not tagger_parameters:
    tagger_parameters = {}
  if tagger := _TAGGERS.get(tagger_type):
    if issubclass(tagger, llm.LLMTagger):
      return tagger(
        tagger_type=_LLM_TAGGERS_TYPES.get(tagger_type), **tagger_parameters
      )
    return tagger(**tagger_parameters)
  raise ValueError(
    f'Incorrect tagger {type} is provided, '
    f'valid options: {list(_TAGGERS.keys())}'
  )


def tag_media(
  media_paths: Sequence[str | os.PathLike],
  tagger_type: base.BaseTagger,
  tagging_parameters: dict[str, str] | None = None,
) -> list[base.TaggingResult]:
  """Runs media tagging algorithm.

  Args:
    media_paths: Local or remote path to media file.
    tagger_type: Initialized tagger.
    tagging_parameters: Optional keywords arguments to be sent for tagging.

  Returns:
    Results of tagging for all media.
  """
  if not tagging_parameters:
    tagging_parameters = {}
  results = []
  for path in media_paths:
    media_name = utils.convert_path_to_media_name(path)
    logging.info('Processing media: %s', path)
    media_bytes = utils.read_media_as_bytes(path)
    results.append(
      tagger_type.tag(
        media_name,
        media_bytes,
        tagging_options=base.TaggingOptions(**tagging_parameters),
      )
    )
  return results
