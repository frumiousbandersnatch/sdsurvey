from converters import *

# meta data about the short survey
# (short name, converter, c++ type, tree type)
desc = [
    ('timestamp', timestamp_convert, 'int'),
    ('age', integerify, 'int'),
    ('country', str, 'std::string'),
    ('state', str, 'std::string'),
    ('province', str, 'std::string'),
    ('soberdate', date_convert, 'int'),
]
