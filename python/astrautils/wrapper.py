def wrapper_factory(wrap_left: str = '', wrap_right: str = '', left_padding: str = '', right_padding: str = ''):
    wrap_left_b = wrap_left.encode('utf-8')
    wrap_right_b = wrap_right.encode('utf-8')
    left_padding_b = left_padding.encode('utf-8')
    right_padding_b = right_padding.encode('utf-8')
    def wrapper(s):
        if isinstance(s, str):
            return wrap_left + left_padding + s + right_padding + wrap_right
        else:
            return wrap_left_b + left_padding_b + s + right_padding_b + wrap_right_b
    return wrapper

wrap_square = wrapper_factory('[', ']')
wrap_round  = wrapper_factory('(', ')')
wrap_curly  = wrapper_factory('{', '}')
wrap_quotes = wrapper_factory('"', '"')
wrap_quote  = wrapper_factory("'", "'")
wrap_tag    = wrapper_factory("<", ">")
