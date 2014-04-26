#!/usr/bin/env python

import mailbox

mbox = mailbox.mbox('/home/ibanez/data/ITK/Community/MailingList/python/ITKUsers.txt')

people = {}
messages = {}

for message in mbox:
  message_id = message['Message-Id']
  message_from = message['From']
  message_reply = message['In-Reply-To']
  message_date = message['Date']

  if message_id:
    messages[message_id]={}

    if message_from:
      # remove charactes from email source after the open parenthesis
      sender = message_from.split("(")[0].lower()

      messages[message_id]['From']={}
      messages[message_id]['From'][sender]=''

      people[sender]={}
      people[sender]['Send']={}
      people[sender]['Send'][message_id]=''

    if message_date:
      messages[message_id]['Date']={}
      messages[message_id]['Date'][message_date]=''

    if message_reply:
      messages[message_id]['ReplyTo']={}
      messages[message_id]['ReplyTo'][message_reply]=''

for message in mbox:
  message_id = message['Message-Id']
  message_reply = message['In-Reply-To']
  message_from = message['From']

  if message_reply:
    if message_reply in messages:
      previous_message = messages[message_reply]

      if previous_message:
        recipient = previous_message['From'].itervalues().next()

        if recipient:
          messages[message_id]['To']={}
          messages[message_id]['To'][recipient]=''

          people[recipient]['Received']={}
          people[recipient]['Received'][message_id]=''

          # remove charactes from email source after the open parenthesis
          sender = message_from.split("(")[0].lower()
          people[recipient]['ReceivedFrom'][sender][message_id]=''
          people[sender]['ReceivedFrom'][recipient][message_id]=''




# sort the people dictionary by key
sorted(people, key=people.get)

# list of people with number of emails sents and received
for personid in people:
  person = people[personid]
  if person:
    sent = person['Send']
    number_of_emails_sent = len(sent)
    number_of_emails_received = 0
    if 'Received' in person:
      received = person['Received']
      number_of_emails_received = len(received)
    print personid,' ',number_of_emails_sent,' ',number_of_emails_received



print "Number of messages ",len(messages)
print "Number of people ",len(people)

