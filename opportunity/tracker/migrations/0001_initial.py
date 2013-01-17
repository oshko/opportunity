# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('tracker_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('tracker', ['UserProfile'])

        # Adding model 'Company'
        db.create_table('tracker_company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('division', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('state_province', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('zipCode', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
        ))
        db.send_create_signal('tracker', ['Company'])

        # Adding model 'Person'
        db.create_table('tracker_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Company'], unique=True, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
        ))
        db.send_create_signal('tracker', ['Person'])

        # Adding model 'Position'
        db.create_table('tracker_position', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Company'], unique=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
        ))
        db.send_create_signal('tracker', ['Position'])

        # Adding model 'Interview'
        db.create_table('tracker_interview', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
            ('position', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Position'], unique=True)),
            ('withWhom', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Person'])),
        ))
        db.send_create_signal('tracker', ['Interview'])

        # Adding model 'Apply'
        db.create_table('tracker_apply', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
            ('position', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Position'], unique=True)),
        ))
        db.send_create_signal('tracker', ['Apply'])

        # Adding model 'Networking'
        db.create_table('tracker_networking', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Company'], unique=True)),
        ))
        db.send_create_signal('tracker', ['Networking'])

        # Adding model 'Lunch'
        db.create_table('tracker_lunch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
            ('withWhom', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Person'])),
            ('venue', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('tracker', ['Lunch'])

        # Adding model 'Gratitude'
        db.create_table('tracker_gratitude', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Person'], unique=True)),
        ))
        db.send_create_signal('tracker', ['Gratitude'])

        # Adding model 'Conversation'
        db.create_table('tracker_conversation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
            ('via', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Person'], unique=True)),
        ))
        db.send_create_signal('tracker', ['Conversation'])

        # Adding model 'Pitch'
        db.create_table('tracker_pitch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('thePitch', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
        ))
        db.send_create_signal('tracker', ['Pitch'])

        # Adding model 'OnlinePresence'
        db.create_table('tracker_onlinepresence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
        ))
        db.send_create_signal('tracker', ['OnlinePresence'])

        # Adding model 'PAR'
        db.create_table('tracker_par', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('par_response', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
        ))
        db.send_create_signal('tracker', ['PAR'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('tracker_userprofile')

        # Deleting model 'Company'
        db.delete_table('tracker_company')

        # Deleting model 'Person'
        db.delete_table('tracker_person')

        # Deleting model 'Position'
        db.delete_table('tracker_position')

        # Deleting model 'Interview'
        db.delete_table('tracker_interview')

        # Deleting model 'Apply'
        db.delete_table('tracker_apply')

        # Deleting model 'Networking'
        db.delete_table('tracker_networking')

        # Deleting model 'Lunch'
        db.delete_table('tracker_lunch')

        # Deleting model 'Gratitude'
        db.delete_table('tracker_gratitude')

        # Deleting model 'Conversation'
        db.delete_table('tracker_conversation')

        # Deleting model 'Pitch'
        db.delete_table('tracker_pitch')

        # Deleting model 'OnlinePresence'
        db.delete_table('tracker_onlinepresence')

        # Deleting model 'PAR'
        db.delete_table('tracker_par')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'tracker.apply': {
            'Meta': {'ordering': "['when']", 'object_name': 'Apply'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.Position']", 'unique': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.UserProfile']"}),
            'when': ('django.db.models.fields.DateField', [], {})
        },
        'tracker.company': {
            'Meta': {'ordering': "['name']", 'object_name': 'Company'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'division': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.UserProfile']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'zipCode': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'tracker.conversation': {
            'Meta': {'ordering': "['when']", 'object_name': 'Conversation'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.Person']", 'unique': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.UserProfile']"}),
            'via': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'when': ('django.db.models.fields.DateField', [], {})
        },
        'tracker.gratitude': {
            'Meta': {'ordering': "['when']", 'object_name': 'Gratitude'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.Person']", 'unique': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.UserProfile']"}),
            'when': ('django.db.models.fields.DateField', [], {})
        },
        'tracker.interview': {
            'Meta': {'ordering': "['when']", 'object_name': 'Interview'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.Position']", 'unique': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.UserProfile']"}),
            'when': ('django.db.models.fields.DateField', [], {}),
            'withWhom': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.Person']"})
        },
        'tracker.lunch': {
            'Meta': {'ordering': "['when']", 'object_name': 'Lunch'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.UserProfile']"}),
            'venue': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'when': ('django.db.models.fields.DateField', [], {}),
            'withWhom': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.Person']"})
        },
        'tracker.networking': {
            'Meta': {'ordering': "['when']", 'object_name': 'Networking'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.UserProfile']"}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.Company']", 'unique': 'True'}),
            'when': ('django.db.models.fields.DateField', [], {})
        },
        'tracker.onlinepresence': {
            'Meta': {'ordering': "['name']", 'object_name': 'OnlinePresence'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.UserProfile']"})
        },
        'tracker.par': {
            'Meta': {'ordering': "['question']", 'object_name': 'PAR'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'par_response': ('django.db.models.fields.TextField', [], {}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.UserProfile']"})
        },
        'tracker.person': {
            'Meta': {'object_name': 'Person'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.Company']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.UserProfile']"})
        },
        'tracker.pitch': {
            'Meta': {'object_name': 'Pitch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'thePitch': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.UserProfile']"})
        },
        'tracker.position': {
            'Meta': {'ordering': "['title']", 'object_name': 'Position'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.Company']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.UserProfile']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'tracker.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['tracker']