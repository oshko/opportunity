# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Mentorship'
        db.create_table('tracker_mentorship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('jobseeker', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jobseeker', to=orm['tracker.UserProfile'])),
            ('mentor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mentor', to=orm['tracker.UserProfile'])),
            ('coach', self.gf('django.db.models.fields.related.ForeignKey')(related_name='coach', to=orm['tracker.UserProfile'])),
            ('startDate', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('tracker', ['Mentorship'])


    def backwards(self, orm):
        # Deleting model 'Mentorship'
        db.delete_table('tracker_mentorship')


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
            'Meta': {'ordering': "['-when', 'time']", 'object_name': 'Apply'},
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
            'Meta': {'ordering': "['-when', 'time']", 'object_name': 'Conversation'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.Person']", 'unique': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.UserProfile']"}),
            'via': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'when': ('django.db.models.fields.DateField', [], {})
        },
        'tracker.gratitude': {
            'Meta': {'ordering': "['-when', 'time']", 'object_name': 'Gratitude'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.Person']", 'unique': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.UserProfile']"}),
            'when': ('django.db.models.fields.DateField', [], {})
        },
        'tracker.interview': {
            'Meta': {'ordering': "['-when', 'time']", 'object_name': 'Interview'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.Position']", 'unique': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.UserProfile']"}),
            'when': ('django.db.models.fields.DateField', [], {}),
            'withWhom': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.Person']"})
        },
        'tracker.lunch': {
            'Meta': {'ordering': "['-when', 'time']", 'object_name': 'Lunch'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.UserProfile']"}),
            'venue': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'when': ('django.db.models.fields.DateField', [], {}),
            'withWhom': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.Person']"})
        },
        'tracker.mentorship': {
            'Meta': {'object_name': 'Mentorship'},
            'coach': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coach'", 'to': "orm['tracker.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jobseeker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jobseeker'", 'to': "orm['tracker.UserProfile']"}),
            'mentor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mentor'", 'to': "orm['tracker.UserProfile']"}),
            'startDate': ('django.db.models.fields.DateField', [], {})
        },
        'tracker.networking': {
            'Meta': {'ordering': "['-when', 'time']", 'object_name': 'Networking'},
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