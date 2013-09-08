import os
import pydtc


def test_extract_quote():
    this_dir = os.path.dirname(__file__)
    with open(os.path.join(this_dir, "14873.html"), "r") as fp:
        html = fp.read()
    quote = pydtc.extract_quote(html, 14873)
    assert quote == """\
Sam : putain j'ai revu 3 filles du lycée dans le bus
Sam : elles m'ont pas manqué cette année --'
Flo : toi par contre tu me manques <3
Sam : Oo
Sam : wtf x)
Flo : tu me dois encore 20€ je te rappelle
Sam : ah
Sam : je me disais ca paraissait bizarre d'un coup : /
"""

def test_wraps_long_replies():
    html = """
<a href="http://danstonchat.com/42.html">

<span>Me:</span>This is a really long long long line ............................................ <br />
<span>You:</span>And this is my reply
</a>
"""
    quote = pydtc.extract_quote(html, 42)
    assert quote == """\
Me:This is a really long long long line
............................................
You:And this is my reply
"""
