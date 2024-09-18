from plone import schema
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from plone.schema.email import Email
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class IRSSFeed(model.Schema):
    """Dexterity-Schema for RSS Feed"""

    max_title_length = schema.Int(
        title=u"Maximum Title Length",
        description=u"Maximum number of characters allowed for titles.",
        required=True,
        default=150,
    )

    max_description_length = schema.Int(
        title=u"Maximum Description Length",
        description=u"Maximum number of characters allowed for descriptions.",
        required=True,
        default=400,
    )
    


@implementer(IRSSFeed)
class RSSFeed(Container):
    """Content-type class for IRSSFeed"""