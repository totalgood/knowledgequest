#!/usr/bin/env python
#!/python -m spacy download en
# import lxml.html
import html2text
import spacy
import gensim
from gensim.summarization.summarizer import summarize
import textract


if __name__ == "__main__":
    summaries = []
    paths = [
        '/Users/hobs/Downloads/The PwC Internal Audit.html',
        '/Users/hobs/Downloads/Internal Audit - Risk Assurance - Assurance and Audit Services - PwC in the Middle East.html',
        '/Users/hobs/Downloads/PWC-Expect More copy.pdf',
    ]
#     ## 5% summaries:
#     [
#      "The PwC Internal Audit  Close  ###### Start adding items to your reading lists:  Sign in  or  Create your account  \n
#      *Regulatory good citizenship   ** Leading organisations that are regarded as 'regulatory good citizens' are those that
#        embrace regulation, recognising that it drives resilience, good practice, control, competition, governance and performance.\n
#      *Regulatory good citizenship   ** Leading organisations that are regarded as 'regulatory good citizens' are those that embrace regulation, 
#        recognising that it drives resilience, good practice, control, competition, governance and performance.",
#
#      'The right skills and experience to help you identify, prioritise and gain assurance over the current and emerging risks that matter most to your business.',
#
#      'Stakeholders expect IA to ‘look deeper and see  further’, acting as a lever for change supporting an  organisation’s strategic agenda moving up from  an 
#       assurance provider to trusted advisor (fig.\nTrusted  advisor  Providing value-added services  and proactive strategic advice  to the business well beyond 
#       the  effective and efficient execution  of the audit plan.\nIn this time of constantly changing business  terrain, business alignment, risk focus, talent
#       model and technology are four key areas  recognised by Chief Audit Executives (CAE) and  key stakeholders as top enablers for IA to be a  valued contributor.'
#     ]
#     ## 8% summaries:
#     ["The PwC Internal Audit  Close  ###### Start adding items to your reading lists:  Sign in  or  Create your account  \n## **Regulatory Response – Redefining the value of regulation\n** It may seem like a paradox, but if you sort it out and do it well, a good regulatory response buys you a lot of freedom, allowing you to invest in your business with less scrutiny.\n*Regulatory good citizenship   ** Leading organisations that are regarded as 'regulatory good citizens' are those that embrace regulation, recognising that it drives resilience, good practice, control, competition, governance and performance.\n*Regulatory good citizenship   ** Leading organisations that are regarded as 'regulatory good citizens' are those that embrace regulation, recognising that it drives resilience, good practice, control, competition, governance and performance.",
#      'These attributes are:    * Having an internal audit function focusing on the risks that matter to your organisation, both current and emerging.\nThe right skills and experience to help you identify, prioritise and gain assurance over the current and emerging risks that matter most to your business.',
#      'Stakeholders expect IA to ‘look deeper and see  further’, acting as a lever for change supporting an  organisation’s strategic agenda moving up from  an assurance provider to trusted advisor (fig.\nTrusted  advisor  Providing value-added services  and proactive strategic advice  to the business well beyond the  effective and efficient execution  of the audit plan.\nIn this time of constantly changing business  terrain, business alignment, risk focus, talent  model and technology are four key areas  recognised by Chief Audit Executives (CAE) and  key stakeholders as top enablers for IA to be a  valued contributor.\nOutsourcing to manage your cost more effectively   •  Developing risk assessments, Internal Audit plans and scope \nDelivering value to your business  To help companies meet the demands of  maintaining an effective internal audit function,  we offer flexible, scalable, sophisticated solutions to  address your unique needs.']



    for path in paths:
        ext = path.lower().split('.')[-1]
        if ext == 'html':
            html = open(path).read()
            txt = html2text.html2text(html)
        elif ext == 'pdf':
            txt = textract.process(path).decode()

        nlp = spacy.load('en')
        docobj = nlp(txt)
        sents = [str(s.text) for s in docobj.sents if '.html' not in s.text and 'http' not in s.text and len(s) > 2]
        tokenized_sents = [[str(w) for w in s] for s in sents]

        # summarize([str(s) for s in sents].join('\n'))
        txt = '\n'.join([str(s).replace('\n', ' ') for s in sents])
        summary = summarize(txt, .08)
        print(txt)
        print()
        print()
        print(summary)
        summaries.append(summary)