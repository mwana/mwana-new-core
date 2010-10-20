# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SampleNotification'
        db.create_table('labresults_samplenotification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rapidsms.Contact'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Location'])),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('count_in_text', self.gf('django.db.models.fields.CharField')(max_length=160, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
        ))
        db.send_create_signal('labresults', ['SampleNotification'])

        # Adding model 'Result'
        db.create_table('labresults_result', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sample_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('requisition_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('payload', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='lab_results', null=True, to=orm['labresults.Payload'])),
            ('clinic', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='lab_results', null=True, to=orm['locations.Location'])),
            ('clinic_code_unrec', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('result_detail', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('collected_on', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('entered_on', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('processed_on', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('notification_status', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('child_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('child_age_unit', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('mother_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('collecting_health_worker', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('coll_hw_title', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('record_change', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
            ('old_value', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('verified', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('result_sent_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('labresults', ['Result'])

        # Adding model 'Payload'
        db.create_table('labresults_payload', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('incoming_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('auth_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('client_timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('parsed_json', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('validated_schema', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('raw', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('labresults', ['Payload'])

        # Adding model 'LabLog'
        db.create_table('labresults_lablog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('line', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('payload', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labresults.Payload'])),
            ('raw', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('labresults', ['LabLog'])


    def backwards(self, orm):
        
        # Deleting model 'SampleNotification'
        db.delete_table('labresults_samplenotification')

        # Deleting model 'Result'
        db.delete_table('labresults_result')

        # Deleting model 'Payload'
        db.delete_table('labresults_payload')

        # Deleting model 'LabLog'
        db.delete_table('labresults_lablog')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contactsplus.contacttype': {
            'Meta': {'object_name': 'ContactType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'labresults.lablog': {
            'Meta': {'object_name': 'LabLog'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'line': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'payload': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labresults.Payload']"}),
            'raw': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'labresults.payload': {
            'Meta': {'object_name': 'Payload'},
            'auth_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'client_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incoming_date': ('django.db.models.fields.DateTimeField', [], {}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'parsed_json': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'raw': ('django.db.models.fields.TextField', [], {}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'validated_schema': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'labresults.result': {
            'Meta': {'ordering': "('collected_on', 'requisition_id')", 'object_name': 'Result'},
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'child_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'child_age_unit': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'clinic': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'lab_results'", 'null': 'True', 'to': "orm['locations.Location']"}),
            'clinic_code_unrec': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'coll_hw_title': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'collected_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'collecting_health_worker': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'entered_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mother_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'notification_status': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'old_value': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'payload': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'lab_results'", 'null': 'True', 'to': "orm['labresults.Payload']"}),
            'processed_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'record_change': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'requisition_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'result_detail': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'result_sent_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sample_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'verified': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'labresults.samplenotification': {
            'Meta': {'object_name': 'SampleNotification'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms.Contact']"}),
            'count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'count_in_text': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Location']"})
        },
        'locations.location': {
            'Meta': {'object_name': 'Location'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Point']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'locations'", 'null': 'True', 'to': "orm['locations.LocationType']"})
        },
        'locations.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'primary_key': 'True', 'db_index': 'True'})
        },
        'locations.point': {
            'Meta': {'object_name': 'Point'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'})
        },
        'rapidsms.contact': {
            'Meta': {'object_name': 'Contact'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_help_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'contacts'", 'blank': 'True', 'to': "orm['contactsplus.ContactType']"})
        }
    }

    complete_apps = ['labresults']
