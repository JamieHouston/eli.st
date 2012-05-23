# from http://codelog.blogial.com/2008/07/27/singular-form-of-a-word-in-python/

def singularize(word):
    """Return the singular form of a word

    &gt;&gt;&gt; singularize('rabbits')
    'rabbit'
    &gt;&gt;&gt; singularize('potatoes')
    'potato'
    &gt;&gt;&gt; singularize('leaves')
    'leaf'
    &gt;&gt;&gt; singularize('knives')
    'knife'
    &gt;&gt;&gt; singularize('spies')
    'spy'
    """
    sing_rules = [lambda w: w[-3:] == 'ies' and w[:-3] + 'y',
                  lambda w: w[-4:] == 'ives' and w[:-4] + 'ife',
                  lambda w: w[-3:] == 'ves' and w[:-3] + 'f',
                  lambda w: w[-2:] == 'es' and w[:-2],
                  lambda w: w[-1:] == 's' and w[:-1],
                  lambda w: w,
                  ]
    word = word.strip()
    singleword = [f(word) for f in sing_rules if f(word) is not False][0]
    return singleword

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()