from flask import *
from time import time, strftime, gmtime
from sqlalchemy import *
from sqlalchemy.orm import relationship

from .mix_ins import Stndrd, Age_times
from ruqqus.helpers.base36 import *
from ruqqus.__main__ import Base


class Conversation(Base, Stndrd, Age_times):

    __tablename__="conversations"
    id=Column(Integer, primary_key=True)
    author_id=Column(Integer, ForeignKey("users.id"))
    created_utc=Column(Integer)
    subject=Column(String(256))

    members=relationship("ConvoMember", lazy="joined")
    messages=relationship("Message", lazy="joined")

    
    def __repr__(self):

        return f"<Conversation(id={self.base36id})>"

    @property
    def permalink(self):
        return f"/messages/{self.base36id}"

    def has_member(self, user):
        return user.id in [x.user_id for x in self.members]

    @property
    def fullname(self):
        return f"t6_{self.base36id}"




class Message(Base, Stndrd, Age_times):

    __tablename__="messages"
    id=Column(Integer, primary_key=True)
    author_id=Column(Integer, ForeignKey("users.id"))
    created_utc=Column(Integer)
    body=Column(String(10000))
    body_html=Column(String(15000))
    distinguish_level=Column(Integer, default=0)
    convo_id=Column(Integer, ForeignKey("conversations.id"))

    conversation=relationship("Conversation")
    author=relationship("User", lazy="joined")

    def __repr__(self):

        return f"<Message(id={self.base36id}, from={self.author.username})>"

    @property
    def permalink(self):
        return f"{self.conversation.permalink}/message/{self.base36id}"

    @property
    def convo_fullname(self):
        return f"t6_{base36encode(self.convo_id)}"
    

class ConvoMember(Base, Stndrd, Age_times):

    __tablename__="convo_member"
    id=Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey("users.id"))
    convo_id=Column(Integer, ForeignKey("conversations.id"))

    user=relationship("User")
    conversation=relationship("Conversation")


    def __repr__(self):

        return f"<ConvoMember(id={self.base36id})>"

class MessageNotif(Base, Stndrd, Age_times):

    __tablename__="message_notifications"
    id=Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey("users.id"))
    message_id=Column(Integer, ForeignKey("messages.id"))
    has_read=Column(Boolean, default=False)