from rapidsms.contrib.handlers.app import App as handler_app
from rapidsms.contrib.messagelog.app import App as logger_app
from rapidsms.contrib.locations.models import LocationType, Location
from rapidsms.models import Contact, Connection
from rapidsms.tests.scripted import TestScript
from mwana.const import get_clinic_worker_type, get_cba_type, get_zone_type
from mwana.apps.broadcast.app import App as broadcast_app
from mwana.apps.broadcast.models import BroadcastMessage, BroadcastResponse
import mwana.const as const

class TestApp(TestScript):
    
    def setUp(self):
        super(TestApp, self).setUp()
        type, _ = LocationType.objects.get_or_create(singular="clinic", 
                                                     plural="clinics", 
                                                     slug="clinics")
        clinic = Location.objects.create(type=type, name="demo", slug="demo") 
        self.clinic_zone= Location.objects.create(type=get_zone_type(), name="child", 
                                             slug="child", parent=clinic) 
        clinic_worker = self.create_contact(name="clinic_worker", location=clinic, 
                                            types=[get_clinic_worker_type()])
        clinic_worker2 = self.create_contact(name="clinic_worker2", location=self.clinic_zone,
                                             types=[get_clinic_worker_type()])
        
#        script = "help_admin > hello world"
#        self.runScript(script)
#        connection = Connection.objects.get(identity="help_admin")
#        help_admin = Contact.objects.create(alias='help_admin', is_active = True, name="help_admin",
#                                         location=clinic_zone,is_help_admin = True)
#        help_admin.types.add(const.get_clinic_worker_type())
#                                
#        connection.contact = help_admin
#        connection.save()
        
        cba = self.create_contact(name="cba", location=clinic,
                                  types=[get_cba_type()])
        cba2 = self.create_contact(name="cba2", location=self.clinic_zone,
                                   types=[get_cba_type()])
        active_contacts = Contact.active.all()
        
        self.all = [clinic_worker, clinic_worker2, cba, cba2]
        self.expected_keyword_to_groups = \
            {"ALL":    [clinic_worker, clinic_worker2, cba, cba2],
             "CLINIC": [clinic_worker, clinic_worker2],
             "CBA":    [cba, cba2],
             }
        
   
        
    def testGroupMessaging(self):
        self.assertEqual(0, BroadcastMessage.objects.count())
        self.assertEqual(0, BroadcastResponse.objects.count())
        running_count = 0
        response_count = 0
        self.startRouter()
        try:
            # test from each person so we know it works from all cases
            for contact in self.all:
                for keyword, recipients in self.expected_keyword_to_groups.items():
                    running_count += 1
                    message_body = "what up fools!"
                    response = "not much G!"
                    self.sendMessage(contact.default_connection.identity, "%s %s" %\
                                     (keyword, message_body))
                    messages = self.receiveAllMessages()
                    recipients_minus_self = [c for c in recipients if c != contact]
                    self.assertEqual(len(recipients_minus_self), len(messages), 
                                     ("message from %s went to correct amount of "
                                      "people for keyword %s. Expected %s but was "
                                      "%s") % (contact, keyword, len(recipients) - 1,
                                               len(messages)))
                    for msg in messages:
                        self.assertEqual("%(text)s [from %(from)s to %(keyword)s]" % \
                                         {"text": message_body, "from": contact.name,
                                          "keyword": keyword}, 
                                         msg.text)
                    
                    # check DB objects
                    self.assertEqual(running_count, BroadcastMessage.objects.count())
                    last_msg = BroadcastMessage.objects.order_by("-date")[0]
                    self.assertEqual(contact, last_msg.contact)
                    self.assertEqual(keyword, last_msg.group)
                    self.assertEqual(message_body, last_msg.text)
                    for responder in recipients_minus_self:
                        self.assertTrue(responder in last_msg.recipients.all(),
                                        "Recipient %s was linked in the db" % responder)
                        
                    msg_recipients = [msg.peer for msg in messages]
                    for responder in recipients_minus_self:
                        self.assertTrue(responder.default_connection.identity in msg_recipients)
                        
                        # response workflow
                        self.sendMessage(responder.default_connection.identity, response)
                        responses = self.receiveAllMessages()
                        self.assertEqual(1, len(responses))
                        self.assertEqual(contact.default_connection.identity, responses[0].peer)
                        self.assertEqual("%(text)s [from %(from)s]" % \
                                         {"text": response, "from": responder.name},
                                         responses[0].text)
                        
                        # check models
                        response_count += 1
                        self.assertEqual(response_count, BroadcastResponse.objects.count())
                        last_resp = BroadcastResponse.objects.order_by("-date")[0]
                        self.assertEqual(last_msg, last_resp.broadcast)
                        self.assertEqual(response, last_resp.text)
                        self.assertEqual(responder, last_resp.contact)

        finally:
            self.stopRouter()
    
    def create_contact(self, name, location, types):
        contact = Contact.objects.create(alias=name, name=name,
                                         location=location)
        contact.types = types
        script = "%(name)s > hello world" % {"name": name}
        self.runScript(script)
        connection = Connection.objects.get(identity=name)
        connection.contact = contact
        connection.save()
        return contact
    
    def testBlaster(self):
        script = "help_admin > hello world"
        self.runScript(script)
        connection = Connection.objects.get(identity="help_admin")
        help_admin = Contact.objects.create(alias='help_admin', is_active = True, name="help_admin",
                                         location=self.clinic_zone,is_help_admin = True)
        help_admin.types.add(const.get_clinic_worker_type())
                                
        connection.contact = help_admin
        connection.save()
        
        script = """
            help_admin > blast hello
            clinic_worker < hello [from help_admin to Mwana Users]
            clinic_worker2 < hello [from help_admin to Mwana Users]
            cba < hello [from help_admin to Mwana Users]
            cba2 < hello [from help_admin to Mwana Users]                 
        """
        self.runScript(script)
        