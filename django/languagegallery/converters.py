from django.forms.models import model_to_dict

# Data converters

def hex_to_bytes(string):
  return bytearray.fromhex(string)


def bytes_to_hex(data):
  return ''.join(['%02x' % b for b in bytes(data)])


# Model converters

def updateFile(file_model):
  return { **model_to_dict(file_model), **model_to_dict(file_model.mimetype),
    'hash_hex': bytes_to_hex(file_model.sha256) }


# Path parameter converters

class FileHash:
  regex = '[\da-f]{64}'

  def to_python(self, string):
    return hex_to_bytes(string)

  def to_url(self, data):
    return bytes_to_hex(data)


class FileExtension:
  regex = '(jpe?g|gif|png|tiff?)'

  def to_python(self, string):
    return string

  def to_url(self, data):
    return data

