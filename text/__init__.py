""" from https://github.com/keithito/tacotron """
import re
from text import cleaners
from text.symbols import symbols


# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}


def text_to_sequence(text, cleaner_names):
  '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    Args:
      text: string to convert to a sequence
      cleaner_names: names of the cleaner functions to run the text through
    Returns:
      List of integers corresponding to the symbols in the text
  '''
  sequence = []

  clean_text = _clean_text(text, cleaner_names)
  for symbol in clean_text:
    symbol_id = _symbol_to_id[symbol]
    sequence += [symbol_id]
  return sequence


def cleaned_text_to_sequence(cleaned_text):
  '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    Args:
      text: string to convert to a sequence
    Returns:
      List of integers corresponding to the symbols in the text
  '''
  # *****************for chinese phoneme text*******************
  s = 0
  phos = []
  # 按空格将phoneme分开
  for i,p in enumerate(cleaned_text):
    if p == ' ':
      pho = cleaned_text[s:i]
      phos.append(pho)
      phos.append(p)
      s = i + 1
  phos.append(cleaned_text[s:])  # 处理文本最后空格后的一个词

  dic = {}
  for i,j in enumerate(phos):
    if re.search(r'[,.!?;:()]', j) is not None:
      index = i + 1
      punc = j[-1]
      dic[punc] = int(index)
      phos[i] = j.replace(punc, '')

  v = 0
  for k in dic:
    dic[k] += v
    if dic[k] < len(phos):
      phos.insert(dic[k], k)
      v += 1
    else:
      phos.append(k)
  
  for i,pho in enumerate(phos):
    if pho not in _symbol_to_id.keys():
      phos[i] = '<UNK>'
  sequence = [_symbol_to_id[pho] for pho in phos]  
# *************************************************************

# original version
  sequence = [_symbol_to_id[symbol] for symbol in cleaned_text]
  return sequence


def sequence_to_text(sequence):
  '''Converts a sequence of IDs back to a string'''
  result = ''
  for symbol_id in sequence:
    s = _id_to_symbol[symbol_id]
    result += s
  return result


def _clean_text(text, cleaner_names):
  for name in cleaner_names:
    cleaner = getattr(cleaners, name)
    if not cleaner:
      raise Exception('Unknown cleaner: %s' % name)
    text = cleaner(text)
  return text
