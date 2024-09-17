# -*- coding: utf-8 -*-

from collective import dexteritytextindexer
from collective.classification.folder import _
from collective.classification.folder import utils
from collective.classification.folder.browser.faceted import IClassificationFacetedNavigable
from collective.classification.folder.content.vocabularies import full_title_categories
from collective.classification.folder.content.vocabularies import get_folders_tree
from collective.classification.folder.content.vocabularies import ServiceInChargeSourceBinder
from collective.classification.folder.content.vocabularies import ServiceInCopySourceBinder
from collective.classification.folder.content.vocabularies import set_folders_tree
from collective.classification.tree.vocabularies import ClassificationTreeSourceBinder
from collective.z3cform.select2.widget.widget import MultiSelect2FieldWidget
from dexterity.localrolesfield.field import LocalRoleField
from dexterity.localrolesfield.field import LocalRolesField
from eea.facetednavigation.events import FacetedEnabledEvent
from eea.facetednavigation.events import FacetedWillBeEnabledEvent
from eea.facetednavigation.layout.interfaces import IFacetedLayout
from eea.facetednavigation.settings.interfaces import IDisableSmartFacets
from eea.facetednavigation.settings.interfaces import IHidePloneRightColumn
from os import path
from plone import api
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from plone.supermodel import model
from Products.statusmessages.interfaces import IStatusMessage
from zExceptions import Redirect
from zope import schema
from zope.component import getMultiAdapter
from zope.container.contained import ContainerModifiedEvent
from zope.event import notify
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant
from zope.lifecycleevent import IObjectRemovedEvent
from zope.schema.fieldproperty import FieldProperty


class IClassificationFolder(model.Schema):
    """Marker interface and Dexterity Python Schema for ClassificationFolder"""

    dexteritytextindexer.searchable("title")
    title = schema.TextLine(
        title=_(u"Name"),
        # description=_(u"Name of the folder"),
    )

    dexteritytextindexer.searchable("internal_reference_no")
    internal_reference_no = schema.TextLine(
        title=_(u"Classification identifier"),
        # description=_(u"Unique identifier of the folder"),
        required=False,
    )

    dexteritytextindexer.searchable("classification_categories")
    form.widget(classification_categories=AutocompleteMultiFieldWidget)
    classification_categories = schema.List(
        title=_(u"Classification categories"),
        # description=_(u"List of categories / subcategories"),
        value_type=schema.Choice(
            source=ClassificationTreeSourceBinder(enabled=True),
        ),
        required=False,
    )

    treating_groups = LocalRoleField(
        title=_(u"Service in charge"),
        # description=_(u"ID of the service that are in charge of this folder"),
        source=ServiceInChargeSourceBinder(),
        required=True,
    )

    form.widget(recipient_groups=MultiSelect2FieldWidget)
    recipient_groups = LocalRolesField(
        title=_(u"Services in copy"),
        # description=_(u"ID of the services that can access this folder"),
        value_type=schema.Choice(
            source=ServiceInCopySourceBinder(),
        ),
        required=False,
    )

    dexteritytextindexer.searchable("classification_informations")
    classification_informations = schema.Text(
        title=_(u"Classification informations"),
        # description=_(u"Informations"),
        required=False,
    )

    archived = schema.Bool(
        title=_(u"Archived"),
        required=False,
        default=False,
    )

    @invariant
    def unique_identifier_invariant(data):
        data_uuid = None
        portal_types = ("ClassificationFolder", "ClassificationSubfolder")
        if getattr(data, "__context__", None):
            try:
                data_uuid = api.content.get_uuid(data.__context__)
            except TypeError:
                # This can happen during creation with API
                pass
        elif getattr(data, "portal_type", None) in portal_types:
            try:
                data_uuid = api.content.get_uuid(data)
            except TypeError:
                # This can happen during creation with API
                pass

        brains = api.content.find(
            context=api.portal.get(),
            internal_reference_no=data.internal_reference_no,
        )
        if len([b for b in brains if b.UID != data_uuid]) != 0:
            raise Invalid(
                _(u"The classification identifier must be unique to this folder.")
            )


@implementer(IClassificationFolder)
class ClassificationFolder(Container):
    """ """

    __ac_local_roles_block__ = True
    treating_groups = FieldProperty(IClassificationFolder[u"treating_groups"])
    recipient_groups = FieldProperty(IClassificationFolder[u"recipient_groups"])

    def cf_parent(self):
        """In ClassificationSubfolder, the same method returns the ClassificationFolder. Here None"""
        return None

    def _increment_internal_reference(self):
        utils.increment_internal_reference("folder_number")


def on_create(obj, event):
    """Configures faceted navigation. Increases settings counter."""
    notify(FacetedWillBeEnabledEvent(obj))
    alsoProvides(obj, IClassificationFacetedNavigable)
    if not IDisableSmartFacets.providedBy(obj):
        alsoProvides(obj, IDisableSmartFacets)
    if not IHidePloneRightColumn.providedBy(obj):
        alsoProvides(obj, IHidePloneRightColumn)
    notify(FacetedEnabledEvent(obj))

    IFacetedLayout(obj).update_layout("folder-listing-view")

    # We use a method to allow override by subfolder
    obj._increment_internal_reference()


def on_modify(obj, event):
    """Reindexes SearchableText (folder, subfolder) and ClassificationFolderSort (sub).
    Updates folders tree."""
    if isinstance(event, ContainerModifiedEvent):  # when adding a subfolder, the folder is modified
        return
    # obj.reindexObject(idxs=["SearchableText"])
    if obj.portal_type == "ClassificationFolder":
        for subfolder in obj.listFolderContents(
            contentFilter={"portal_type": "ClassificationSubfolder"}
        ):
            subfolder.reindexObject(idxs=["ClassificationFolderSort", "SearchableText"])
    # update annotated tree on portal annotation (uid: (title, categories))
    folders_dic = get_folders_tree()
    if obj.UID() not in folders_dic:
        set_folders_tree(api.portal.get())
        folders_dic = get_folders_tree()
    folders_dic[obj.UID()] = full_title_categories(obj)


def on_delete(obj, event):
    """Checks if some content is linked to the folder to delete."""
    obj_uid = api.content.get_uuid(obj)
    try:
        linked_content = api.content.find(classification_folders=obj_uid)
    except api.exc.CannotGetPortalError:
        # This happen when we try to remove plone object
        return
    if linked_content:
        IStatusMessage(obj.REQUEST).addStatusMessage(
            _(
                "cannot_delete_referenced_folder",
                default="This folder cannot be deleted because it is referenced elsewhere",
            ),
            type="warning",
        )
        view_url = getMultiAdapter(
            (obj, obj.REQUEST), name=u"plone_context_state"
        ).view_url()
        raise Redirect(view_url)


def on_will_move(obj, event):
    """Avoid being renamed. No more used !"""
    if IObjectRemovedEvent.providedBy(event) and event.object.portal_type == "Plone Site":
        return
    if event.oldName is not None and event.newName is not None and event.oldName != event.newName:  # rename
        IStatusMessage(obj.REQUEST).addStatusMessage(_(u"Renaming of folder is not allowed"), type="error")
        # so the redirection is made to the original page, not the renamed one
        event.object.REQUEST.set('orig_template', path.join(event.oldParent.absolute_url(), event.oldName))
        raise ValueError(_(u"Renaming of folder is not allowed"))


def on_move(obj, event):
    """Updates folders tree."""
    if IObjectRemovedEvent.providedBy(event) and event.object.portal_type == 'Plone Site':
        return
    # update annotated tree
    folders_dic = get_folders_tree()
    if event.newParent is None:  # delete
        if obj.UID() not in folders_dic:
            set_folders_tree(api.portal.get())
            folders_dic = get_folders_tree()
        else:
            del folders_dic[obj.UID()]
    else:
        folders_dic[obj.UID()] = full_title_categories(obj)
