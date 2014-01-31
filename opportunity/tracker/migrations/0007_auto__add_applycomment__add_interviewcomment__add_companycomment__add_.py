# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ApplyComment'
        db.create_table(u'tracker_applycomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Apply'])),
        ))
        db.send_create_signal(u'tracker', ['ApplyComment'])

        # Adding model 'InterviewComment'
        db.create_table(u'tracker_interviewcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Interview'])),
        ))
        db.send_create_signal(u'tracker', ['InterviewComment'])

        # Adding model 'CompanyComment'
        db.create_table(u'tracker_companycomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Company'])),
        ))
        db.send_create_signal(u'tracker', ['CompanyComment'])

        # Adding model 'MentorMeetingComment'
        db.create_table(u'tracker_mentormeetingcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.MentorMeeting'])),
        ))
        db.send_create_signal(u'tracker', ['MentorMeetingComment'])

        # Adding model 'ConversationComment'
        db.create_table(u'tracker_conversationcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Conversation'])),
        ))
        db.send_create_signal(u'tracker', ['ConversationComment'])

        # Adding model 'NetworkingComment'
        db.create_table(u'tracker_networkingcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Networking'])),
        ))
        db.send_create_signal(u'tracker', ['NetworkingComment'])

        # Adding model 'PositionComment'
        db.create_table(u'tracker_positioncomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('position', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Position'])),
        ))
        db.send_create_signal(u'tracker', ['PositionComment'])

        # Adding model 'LunchComment'
        db.create_table(u'tracker_lunchcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.UserProfile'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Lunch'])),
        ))
        db.send_create_signal(u'tracker', ['LunchComment'])

        # Deleting field 'Company.comment'
        db.delete_column(u'tracker_company', 'comment')

        # Deleting field 'Interview.comment'
        db.delete_column(u'tracker_interview', 'comment')

        # Deleting field 'Position.comment'
        db.delete_column(u'tracker_position', 'comment')

        # Deleting field 'MentorMeeting.comment'
        db.delete_column(u'tracker_mentormeeting', 'comment')

        # Deleting field 'Apply.comment'
        db.delete_column(u'tracker_apply', 'comment')

        # Deleting field 'Conversation.comment'
        db.delete_column(u'tracker_conversation', 'comment')

        # Deleting field 'Networking.comment'
        db.delete_column(u'tracker_networking', 'comment')

        # Deleting field 'Lunch.comment'
        db.delete_column(u'tracker_lunch', 'comment')


    def backwards(self, orm):
        # Deleting model 'ApplyComment'
        db.delete_table(u'tracker_applycomment')

        # Deleting model 'InterviewComment'
        db.delete_table(u'tracker_interviewcomment')

        # Deleting model 'CompanyComment'
        db.delete_table(u'tracker_companycomment')

        # Deleting model 'MentorMeetingComment'
        db.delete_table(u'tracker_mentormeetingcomment')

        # Deleting model 'ConversationComment'
        db.delete_table(u'tracker_conversationcomment')

        # Deleting model 'NetworkingComment'
        db.delete_table(u'tracker_networkingcomment')

        # Deleting model 'PositionComment'
        db.delete_table(u'tracker_positioncomment')

        # Deleting model 'LunchComment'
        db.delete_table(u'tracker_lunchcomment')

        # Adding field 'Company.comment'
        db.add_column(u'tracker_company', 'comment',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Interview.comment'
        db.add_column(u'tracker_interview', 'comment',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Position.comment'
        db.add_column(u'tracker_position', 'comment',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'MentorMeeting.comment'
        db.add_column(u'tracker_mentormeeting', 'comment',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Apply.comment'
        db.add_column(u'tracker_apply', 'comment',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Conversation.comment'
        db.add_column(u'tracker_conversation', 'comment',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Networking.comment'
        db.add_column(u'tracker_networking', 'comment',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Lunch.comment'
        db.add_column(u'tracker_lunch', 'comment',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tracker.apply': {
            'Meta': {'object_name': 'Apply'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Position']", 'unique': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"}),
            'when': ('django.db.models.fields.DateField', [], {})
        },
        u'tracker.applycomment': {
            'Meta': {'object_name': 'ApplyComment'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Apply']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'tracker.company': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Company'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'division': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_prospective': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'zipCode': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        u'tracker.companycomment': {
            'Meta': {'object_name': 'CompanyComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Company']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'tracker.conversation': {
            'Meta': {'object_name': 'Conversation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Person']", 'unique': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"}),
            'via': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'when': ('django.db.models.fields.DateField', [], {})
        },
        u'tracker.conversationcomment': {
            'Meta': {'object_name': 'ConversationComment'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Conversation']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'tracker.interview': {
            'Meta': {'object_name': 'Interview'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Position']", 'unique': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"}),
            'when': ('django.db.models.fields.DateField', [], {}),
            'withWhom': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Person']"})
        },
        u'tracker.interviewcomment': {
            'Meta': {'object_name': 'InterviewComment'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Interview']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'tracker.lunch': {
            'Meta': {'object_name': 'Lunch'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"}),
            'venue': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'when': ('django.db.models.fields.DateField', [], {}),
            'withWhom': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Person']"})
        },
        u'tracker.lunchcomment': {
            'Meta': {'object_name': 'LunchComment'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Lunch']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'tracker.mentormeeting': {
            'Meta': {'object_name': 'MentorMeeting'},
            'face_to_face': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mentorship': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Mentorship']", 'unique': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"}),
            'when': ('django.db.models.fields.DateField', [], {})
        },
        u'tracker.mentormeetingcomment': {
            'Meta': {'object_name': 'MentorMeetingComment'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.MentorMeeting']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'tracker.mentorship': {
            'Meta': {'ordering': "[u'-startDate']", 'object_name': 'Mentorship'},
            'expirationDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jobseeker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'jobseeker'", 'to': u"orm['tracker.UserProfile']"}),
            'mentor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'mentor'", 'to': u"orm['tracker.UserProfile']"}),
            'startDate': ('django.db.models.fields.DateField', [], {})
        },
        u'tracker.networking': {
            'Meta': {'object_name': 'Networking'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Company']", 'unique': 'True'}),
            'when': ('django.db.models.fields.DateField', [], {})
        },
        u'tracker.networkingcomment': {
            'Meta': {'object_name': 'NetworkingComment'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Networking']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'tracker.onlinepresence': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'OnlinePresence'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"})
        },
        u'tracker.par': {
            'Meta': {'ordering': "[u'question']", 'object_name': 'PAR'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'par_response': ('django.db.models.fields.TextField', [], {}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"})
        },
        u'tracker.person': {
            'Meta': {'object_name': 'Person'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Company']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"})
        },
        u'tracker.pitch': {
            'Meta': {'object_name': 'Pitch'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'thePitch': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"})
        },
        u'tracker.position': {
            'Meta': {'ordering': "[u'title']", 'object_name': 'Position'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'tracker.positioncomment': {
            'Meta': {'object_name': 'PositionComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.UserProfile']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Position']"})
        },
        u'tracker.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_upglo_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "u'jobseeker'", 'max_length': '12'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['tracker']