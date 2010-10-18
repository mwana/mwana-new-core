from datetime import datetime
from mwana.apps.training.models import TrainingSession
from rapidsms.contrib.handlers import KeywordHandler
from rapidsms.contrib.locations.models import Location
from rapidsms.messages import OutgoingMessage
from rapidsms.models import Contact


class TrainingStopHandler(KeywordHandler):

    keyword = "training stop|stop training|traning stop|traning stop"

    HELP_TEXT = "To send notification for stopping a training , send TRAINING STOP <CLINIC CODE>"
    UNKNOWN_LOCATION = "Sorry, I don't know about a location with code %(code)s. Please check your code and try again."
    UNGREGISTERED = "Sorry, you must first register with Results160/RemindMI. If you think this message is a mistake, respond with keyword 'HELP'"

    def help(self):
        self.respond(self.HELP_TEXT)

    def handle(self, text):
        if not self.msg.contact:
            self.respond(self.UNGREGISTERED)
            return

        text = text.strip()
        if not text:
            self.respond(self.HELP_TEXT)
            return

        clinic_code = text[:6]
        try:
            location = Location.objects.get(slug=clinic_code)
        except Location.DoesNotExist:
            self.respond(self.UNKNOWN_LOCATION, code=clinic_code)
            return

        contact = self.msg.contact
        trainings_at_site = TrainingSession.objects.filter(trainer=contact,
                                                           location=location,
                                                           is_on=True)

        for training in trainings_at_site:
            training.is_on = False
            training.end_date = datetime.utcnow()
            training.save()
            
        for help_admin in Contact.active.filter(is_help_admin=True):
            OutgoingMessage(help_admin.default_connection,
                            "Training has stopped at %s, %s"
                            ". Notification was sent by %s, %s" %
                            (location.name, location.slug, contact.name,
                            contact.default_connection.identity)).send()
        
            
        self.respond("Thanks %(name)s for your message that training has "
                     "stopped for %(clinic)s.",
                     name=contact.name, clinic=location.name)
