import copy,json,tempfile,unittest
from datetime import date
from pathlib import Path
from pipeline.refresh import connect,read_release,refresh
from pipeline.newsletter import edition,send_private
from test_refresh import fixtures,NOW

class Client:
 def __init__(self,fail=False):self.posts=0;self.fail=fail
 def call(self,path,data=None):
  if data is None:return {'subscribers':[{'email_address':'test@example.invalid','state':'active'}],'pagination':{'has_next_page':False}}
  self.posts+=1
  if self.fail:raise TimeoutError('Uncertain response')
  assert data['public'] is False
  return {'broadcast':{'id':1,'status':'sending','public':False}}

class Newsletter(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory();dbpath=Path(cls.tmp.name)/'data.sqlite';sources=fixtures();refresh(dbpath,fetch=sources.__getitem__,now=NOW);db=connect(dbpath);cls.release=read_release(db);db.close()
 @classmethod
 def tearDownClass(cls):cls.tmp.cleanup()
 def test_facts_rendered_and_stale_withheld(self):
  e=edition(self.release,today=date(2026,9,21));self.assertIn('2026-09-14 to 2026-09-21',e['text']);self.assertNotIn('nan',e['content']);self.assertIn('near zero',e['content']);self.assertEqual(e['facts']['release_id'],1)
  with self.assertRaises(ValueError):edition(self.release,today=date(2026,9,25))
 def test_duplicate_and_uncertain_response_are_never_resent(self):
  e=edition(self.release,today=date(2026,9,21));c={'api_key':'fake','test_email':'test@example.invalid','tag_id':1,'template_id':1}
  for failure in (False,True):
   with tempfile.TemporaryDirectory() as d:
    client=Client(failure);ledger=Path(d)/'editions.sqlite'
    if failure:
     with self.assertRaises(TimeoutError):send_private(e,c,ledger,client)
    else:send_private(e,c,ledger,client)
    with self.assertRaises(ValueError):send_private(e,c,ledger,client)
    self.assertEqual(client.posts,1)
 def test_wrong_recipient_is_blocked(self):
  e=edition(self.release,today=date(2026,9,21));client=Client()
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(ValueError):send_private(e,{'test_email':'different@example.invalid','tag_id':1},Path(d)/'l',client)
  self.assertEqual(client.posts,0)
