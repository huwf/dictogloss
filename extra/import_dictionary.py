from bs4 import BeautifulSoup

example = """
<lexicon>
  <ar>
    <k>abort</k>
    <def>
      <gr>nn</gr>
      <dtrn>abortion</dtrn>
      <tr>abÅr+t:</tr>
      <iref href="http://lexin.nada.kth.se/sound/abort.swf" />
      <iref href="http://spraakbanken.gu.se/ws/saldo-ws/fl/html/abort" />
      <ex type="exm"><ex_orig>göra abort</ex_orig><ex_transl>göra abort</ex_transl>      </ex>
      <ex type="exm"><ex_orig>få abort</ex_orig><ex_transl>få abort</ex_transl>      </ex>
      <ex type="exm"><ex_orig>illegal abort</ex_orig><ex_transl>illegal abort</ex_transl>      </ex>
      <ex type="phr"><ex_orig>spontan abort (&quot;missfall&quot;)</ex_orig><ex_transl>spontan abort (&amp;quot;missfall&amp;quot;)</ex_transl></ex>
      <def>(avsiktligt) avbrytande av havandeskap</def>
    </def>
  </ar>
</lexicon>
"""

with open('static/folkets_sv_en_public.xml', encoding='utf-8') as f:


    soup = BeautifulSoup(example)

words = soup.lexicon.find_all('ar')


if __name__ == '__main__':
    for w in words:
        word = w.k.text
        definition = w.find('def')
        examples = {
            e.ex_orig.text: e.ex_transl.text for e in definition.find_all('ex')
        }

        ret = {
            word: [
                {
                    'Definition': definition.dtrn,
                    'Examples': examples
                }
            ]
        }

        print(ret)







