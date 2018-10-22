# coding: utf-8

def sent_splitter_ja(text, delimiters=set(u'。、,．.？?！!\n\r'),
                     parenthesis=u'（）()「」[]{}『』“”<>＜＞'):
    """ specification
    - input: UTF-8 string
    - output: Separated string (generate type)
    - params
    -- text: utf-8 string
    """

    paren_chars = set(parenthesis)
    close2open = dict(zip(parenthesis[1::2], parenthesis[0::2]))  # e.g. {")": "(", ">": "<", ...}
    pstack = []
    buff = []

    # For exclude parenthesis
    for i, c in enumerate(text):
        c_next = text[i+1] if i+1 < len(text) else None
        # check correspondence of parenthesis
        if c in paren_chars:
            if c in close2open:  # close
                if len(pstack) > 0 and pstack[-1] == close2open[c]:
                    pstack.pop()
            else:  # open
                pstack.append(c)

        buff.append(c)
        if c in delimiters:
            if len(pstack) == 0 and c_next not in delimiters:
                yield ''.join(buff)
                buff = []

    if len(buff) > 0:
        yield ''.join(buff)


if __name__ == '__main__':
    pass
