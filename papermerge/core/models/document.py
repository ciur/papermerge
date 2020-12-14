import logging
import os

from django.db import models
from django.urls import reverse
from django.db import transaction, IntegrityError
from django.utils.translation import ugettext_lazy as _

from polymorphic_tree.managers import (
    PolymorphicMPTTModelManager,
    PolymorphicMPTTQuerySet
)

from mglib import step
from mglib.path import DocumentPath, PagePath
from mglib.pdfinfo import get_pagecount
from mglib.utils import get_assigns_after_delete

from papermerge.contrib.admin.registries import sidebar
from papermerge.core import validators
from papermerge.core.storage import default_storage
from .kvstore import (
    KVCompNode,
    KVNode,
    get_currency_formats,
    get_date_formats,
    get_kv_types,
    get_numeric_formats
)

from .node import (
    BaseTreeNode,
    AbstractNode,
    RELATED_NAME_FMT,
    RELATED_QUERY_NAME_FMT
)
from .access import Access
from .utils import group_per_model
from .finder import default_parts_finder

from papermerge.search import index


logger = logging.getLogger(__name__)


class DocumentManager(PolymorphicMPTTModelManager):

    @transaction.atomic
    def create_document(
        self,
        user,
        title,
        lang,
        size,
        page_count,
        file_name,
        notes=None,
        parent_id=None,
        **kwargs
    ):
        """
        Creates a document.

        Special keyword argument ``parts`` is a dictionary
        of extra document parts (added by extra apps)
        """
        # extra document parts
        kw_parts = kwargs.pop('parts', {})

        parent = self._get_parent(parent_id=parent_id)

        doc = Document(
            title=title,
            size=size,
            lang=lang,
            user=user,
            parent=parent,
            notes=notes,
            file_name=file_name,
            page_count=page_count
        )
        # validate before saving
        # will raise ValidationError in case of
        # problems
        doc.full_clean()
        doc.save()
        # Important! - first document must inherit metakeys from
        # parent folder
        if parent:
            doc.inherit_kv_from(parent)

        doc.create_pages()
        doc.full_clean()

        # document parts are created regardless whether there
        # are arguments for them or no.
        self._create_doc_parts(doc, **kw_parts)
        self._create_node_parts(doc, **kw_parts)

        return doc

    def _create_node_parts(self, doc, **kw_parts):
        node_parts = default_parts_finder.find(AbstractNode)
        node_grouped_args = group_per_model(node_parts, **kw_parts)

        for model in node_parts:
            if model != BaseTreeNode:
                args = node_grouped_args.get(model, {})
                instance, _ = model.objects.get_or_create(
                    base_ptr=doc.basetreenode_ptr,
                    **args
                )
                instance.clean()

    def _create_doc_parts(self, doc, **kw_parts):
        # 1. figure out document parts
        # document_parts = [
        #    app1.Document,
        #    app2.Document,
        #    app3.Document
        # ]
        doc_parts = default_parts_finder.find(AbstractDocument)
        # 2. group arguments by document_parts
        # doc_grouped_args = {
        #    app1.Document: {},
        #    app2.Document: {},
        #    app3.Document: {}
        # }
        doc_grouped_args = group_per_model(doc_parts, **kw_parts)
        for model_klass in doc_parts:
            if model_klass != Document:
                args = doc_grouped_args.get(model_klass, {})
                instance, _ = model_klass.objects.get_or_create(
                    base_ptr=doc,
                    **args
                )
                instance.clean()

    def _get_parent(self, parent_id):
        """
        Returns parent node instance based on ``parent_id``
        """
        parent = None

        if parent_id is None or parent_id == '':
            parent = None
        else:
            try:
                parent = BaseTreeNode.objects.get(id=parent_id)
            except BaseTreeNode.DoesNotExist:
                parent = None

        return parent


class DocumentQuerySet(PolymorphicMPTTQuerySet):
    pass


class DocumentPartsManager:
    """
    Manages document parts added by extra apps.
    """

    def __init__(self, document):
        self.document = document

    def __setattr__(self, name, value):
        """
        Assign ``value`` to the attribute ``name`` on the document part model.

        document part model = django model which inherits from
        one of two classes:

            * papermerge.core.models.AbstractDocument
            * papermerge.core.models.AbstractNode

        This method provides a way to assign values to part models
        via Document model:

            doc = Document.objects.create_document(...)
            doc.parts.policy = policy  # <- this assignment is managed here
            doc.save()
        """
        model_klass = default_parts_finder.get(
            AbstractNode,
            attr_name=name
        )
        is_abs_doc = True

        if model_klass:
            is_abs_doc = False
        else:
            model_klass = default_parts_finder.get(
                AbstractDocument,
                attr_name=name
            )

        if is_abs_doc:
            # model_klass inherits from AbstractDocument
            # thus link accordingly
            base_ptr = self.document
        else:
            # model_klass inherits from AbstractNode
            # thus link accordingly
            base_ptr = self.document.basetreenode_ptr

        if model_klass:
            part_instance, _ = model_klass.objects.get_or_create(
                base_ptr=base_ptr
            )

            setattr(part_instance, name, value)
            part_instance.save()
            part_instance.clean()
        else:
            # name is a standard attribute, thus proceed with
            # standard way of assigning things
            self.__dict__[name] = value

    def __getattr__(self, name):
        """
        Looks for missing attributes in document parts
        (added by external apps).

        An example of usage:

        doc = Document.objects.get(id=3001)
        doc.parts.policy # <- this parts.policy is managed by this method.
        """
        # check for the attribute in classes that inherit from AbstractDocument
        model_klass = default_parts_finder.get(
            AbstractDocument,
            attr_name=name
        )

        # check for the attribute in classes that inherit from AbstractNode
        if not model_klass:
            model_klass = default_parts_finder.get(
                AbstractNode,
                attr_name=name
            )

        if model_klass:
            instance = model_klass.objects.get(base_ptr=self.document)
            if hasattr(instance, name):
                ret = getattr(instance, name)
                return ret


CustomDocumentManager = DocumentManager.from_queryset(DocumentQuerySet)

class Document(BaseTreeNode):

    class CannotUpload(Exception):
        pass

    #: basename + ext of uploaded file.
    #: other path details are deducted from user_id and document_id
    file_name = models.CharField(
        max_length=1024,
        default='',
        validators=[validators.safe_character_validator]
    )

    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True,
        validators=[validators.safe_character_validator]
    )

    size = models.BigIntegerField(
        help_text="Size of file_orig attached. Size is in Bytes",
        blank=False,
        null=False,
    )

    page_count = models.IntegerField(
        blank=False,
        default=1
    )

    # Document's version start with 0 (0 = default value)
    # Document's version is incremented everytime stapler operation
    # is applied to it (page delete, page rotate, page reorder).
    # Versioning is on file level. Means - there is no such thing as model
    # level versioning. I think this will complicate everthing just too much.
    # At any point in time, user sees/works with/searches only last version.
    version = models.IntegerField(
        blank=True,
        null=True,
        default=0
    )
    # Q: If there is no model versions, why version is introduced at all?
    # A: pdftk on every operation creates a new file... well, that new
    # file is the next version of the document.

    text = models.TextField(blank=True)

    objects = CustomDocumentManager()

    PREVIEW_HEIGHTS = (100, 300, 500)

    SMALL = PREVIEW_HEIGHTS[0]
    MEDIUM = PREVIEW_HEIGHTS[1]
    LARGE = PREVIEW_HEIGHTS[2]

    search_fields = [
        index.SearchField('title'),
        index.SearchField('text', partial_match=True, boost=2),
        index.SearchField('notes')
    ]

    def each_part(self, abstract_klasses):
        """
        Iterates through each INSTANCE of document parts which inherits
        from given ``abstract_klasses``
        """
        model_klasses = []

        for klass in abstract_klasses:
            model_klasses.extend(default_parts_finder.find(klass))

        for model_klass in model_klasses:
            # if name is an attribute of a klass which inherits
            # from AbstractDocument or AbstractNode...
            try:
                item = model_klass.objects.get(base_ptr=self)
                yield item
            except model_klass.DoesNotExist:
                # Engineering assumption:
                # There must be either 0 (zero) or 1 (one)
                # instances of model_klass with base_ptr pointing
                # to this document.
                pass

    def delete(self, *args, **kwargs):
        """
        Deletes the document and all associated parts in single transaction.

        If any of the parts objects the deletion - either by raising an
        exception or by returning 0 - deletion is aborted.

        Document part may object deletion by:

            * raising an PermissionDenied exception.
            * returning 0 count (i.e. not voting for deletion)

        Deletion function is really tricky.
        The purpose is to delete main document and its parts (satellite if you
        will) in a single database transaction. If any of the parts
        objects - the whole transaction is aborted. The problem is however,
        that if the parts that objects performs some DB operations, those
        operations will be rolled back as well (e.g. retention policy objects
        deletion, but it advances the document to the next state, or moves the
        document to another folder).
        To solve this problem (where objecting parts want to perform some DB
        operations) following approach was chosen (as if I have many options!):
        objecting parts instances are saved into a
        separate list, ``instances_which_objected`` and for those instances
        delete operation runs another round (the previous round was
        rolled back = forgotten). On second round the database
        changes are committed.
        """
        abstract_klasses = [AbstractDocument, AbstractNode]
        instance_counter = 0
        vote_counter = 0
        instances_which_objected = []

        try:
            with transaction.atomic():
                for model_instance in self.each_part(abstract_klasses):
                    instance_counter += 1

                    # Model.delete() returns a tuple.
                    # First item in tuple is number of deleted objects
                    model_instance.voting = True
                    deleted_count, _ = model_instance.delete(*args, **kwargs)
                    vote_counter += deleted_count
                    if not deleted_count:
                        instances_which_objected.append(
                            model_instance
                        )

                if vote_counter >= instance_counter:
                    # If all document parts successfully deleted
                    # then delete self
                    super().delete(*args, **kwargs)
                else:
                    raise IntegrityError
        except IntegrityError:
            # commit database changes for those parts which objected
            with transaction.atomic():
                for model_instance in instances_which_objected:
                    # a way to distinguish between two deletes
                    model_instance.voting = False
                    model_instance.delete(*args, **kwargs)

    @property
    def parts(self):
        return DocumentPartsManager(self)

    @property
    def part(self):
        return self.parts()

    def to_dict(self):
        item = {}

        pages = []
        for page in self.pages.all():
            pages.append(page.to_dict())

        item['id'] = self.id
        item['title'] = self.title
        item['notes'] = self.notes
        item['versions'] = self.get_versions()
        item['created_at'] = self.human_created_at
        item['updated_at'] = self.human_updated_at
        item['timestamp'] = self.created_at.timestamp()

        if self.parent:
            item['parent_id'] = self.parent.id
        else:
            item['parent_id'] = ''

        item['ctype'] = 'document'
        item['pages'] = pages

        tags = []
        for tag in self.tags.all():
            tags.append(tag.to_dict())
        item['tags'] = tags

        parts = []
        for sidebar_part_klass in sidebar.values():
            sidebar_part = sidebar_part_klass(self)
            parts.append(sidebar_part.to_json())

        item['parts'] = parts

        kvstore = []
        for kv in self.kv.all():
            kvstore.append(kv.to_dict())
        item['metadata'] = {}
        item['metadata']['kvstore'] = kvstore
        item['metadata']['currency_formats'] = get_currency_formats()
        item['metadata']['date_formats'] = get_date_formats()
        item['metadata']['numeric_formats'] = get_numeric_formats()
        item['metadata']['kv_types'] = get_kv_types()

        return item

    def assign_kv_values(self, kv_dict):
        """
        Assignes kv_dict of key value to its metadata
        and metadata of its pages.
        """
        logger.debug(
            f"assign_key_values kv_dict={kv_dict} doc_id={self.id}"
        )
        for key, value in kv_dict.items():
            # for self
            logger.debug(
                f"Assign to DOC key={key} value={value}"
            )
            self.kv[key] = value
            # and for all pages of the document
            for page in self.pages.all():
                logger.debug(
                    f"Assign to page number={page.number}"
                    f" key={key} value={value}"
                )
                try:
                    # Never (automatically) overwrite am
                    # existing Metadata value
                    if not page.kv[key]:
                        # page metadata value is empty fill it in.
                        page.kv[key] = value
                except Exception as e:
                    logging.error(
                        f"Error: page {page.number}, doc_id={self.id} has no key={key}", # noqa
                        exc_info=e
                    )

    @property
    def kv(self):
        return KVNode(instance=self)

    def propagate_changes(
        self,
        diffs_set,
        apply_to_self,
        attr_updates=[]
    ):
        super().propagate_changes(
            diffs_set=diffs_set,
            apply_to_self=apply_to_self,
            attr_updates=attr_updates
        )
        # Access permissions are not applicable
        # for Page models, so if diffs_set contains
        # instances of Access - just return
        if (len(diffs_set)):
            first_diff = diffs_set[0]
            if len(first_diff):
                model = list(first_diff)[0]
                if isinstance(model, Access):
                    return

        # documents need to propage changes
        # to their pages

        for page in self.pages.all():
            page.propagate_changes(
                diffs_set=diffs_set,
                apply_to_self=apply_to_self,
                attr_updates=attr_updates
            )

    @property
    def kvcomp(self):
        return KVCompNode(instance=self)

    def inherit_kv_from(self, node):
        inherited_kv = [
            {
                'key': item.key,
                'kv_type': item.kv_type,
                'kv_format': item.kv_format,
                'value': item.value,
                'kv_inherited': True
            } for item in node.kv.all()
        ]
        self.kv.update(inherited_kv)

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")

    def __repr__(self):
        _t = self.title
        _i = self.id
        _v = self.version
        _p = self.get_pagecount()

        return f"Document(id={_i}, version={_v} title={_t}, page_count={_p})"

    def __str__(self):
        return self.title

    def get_versions(self):
        """
        Returns a list of all versions
        numbers of given document. Version
        counting starts with 0. Example:
        [0, 1, 2] - document has 3 versions.
        Original version is 0. Latest version is 2.
        """
        doc_path = self.path()
        versions_list = default_storage.get_versions(
            doc_path
        )

        return versions_list

    def is_latest_version(self, version):
        if version is None:
            return True

        version = int(version)
        return version == self.version

    def get_pagecount(self, version=None) -> int:
        """
        Returns number of pages in the document of specified version.

        There are two ways to looks at page count. One is via self.page_count
        attribute.
        That attribute reflects only the latest version's page count.
        To find out the previous version's page count, we need to have a look
        at filesystem and count number of directories of form page_<x> inside
        document's results folder of respective version.
        """
        if self.is_latest_version(version=version):
            # self.page_count attribute reflects only the latest version
            # page count
            return self.page_count

        doc_path = self.path(version=version)
        count = default_storage.get_pagecount(doc_path)

        return count

    @property
    def file_ext(self):
        _, ext = os.path.splitext(self.file_name)
        return ext

    def reorder_pages(self, new_order):

        if not isinstance(new_order, list):
            logger.error("Expecting list argument")
            return

        new_version = default_storage.reorder_pages(
            doc_path=self.path(),
            new_order=new_order
        )
        self.version = new_version
        self.save()
        self.recreate_pages()

    def delete_pages(
        self,
        page_numbers: list,
        skip_migration=False
    ):
        """
        Deletes pages with given order numbers from
        the documents.
        """
        if not isinstance(page_numbers, list):
            logger.error("Expecting list argument")
            return

        # delete pages
        new_version = default_storage.delete_pages(
            doc_path=self.path(),
            page_numbers=page_numbers,
            skip_migration=skip_migration
        )

        if new_version == self.version:
            raise Exception("Expecting version to be incremented")

        self.version = new_version

        # total pages before delete (of lastest document version)
        total_page_count = self.pages.count()
        self.pages.filter(number__in=page_numbers).delete()
        # update self.page_count attribute (for latest document version)
        self.page_count = self.pages.count()
        self.save()

        self.reassign_page_nums_after_delete(
            page_count=total_page_count,
            deleted_pages=page_numbers
        )

    def reassign_page_nums_after_delete(
        self,
        deleted_pages: list,
        page_count: int
    ):
        """
        :page_count: page count BEFORE delete operation
        """
        pairs = get_assigns_after_delete(
            total_pages=page_count,
            deleted_pages=deleted_pages
        )
        for new_version_page_num, old_version_page_num in pairs:
            page = self.pages.get(number=old_version_page_num)
            page.number = new_version_page_num
            page.save()

    def recreate_pages(self):
        """
        Recreate page models.
        """

        self.pages.all().delete()
        self.page_count = get_pagecount(
            default_storage.abspath(self.path().url())
        )
        self.save()
        self.create_pages()

    def create_pages(self):
        # Q: why doc.page_count is a valid value and yet there
        #  are no pages assigned to document model ?
        # Because page count is retrieved not via models, but by invoking
        # an external utility on pdf file!
        page_count = self.page_count

        for page_index in range(1, page_count + 1):

            preview = reverse(
                'core:preview',
                args=[self.id, 800, page_index]
            )

            page = self.pages.create(
                user=self.user,
                number=page_index,
                image=preview,
                lang=self.lang,
                page_count=page_count
            )
            page.inherit_kv_from(self)

    def update_text_field(self):
        """Update text field from associated page.text fields.

        It will update text field of all associated pages first
        (from .txt files) and then concatinate all text field
        into doc.text field.

        Returns True if document contains non empty non whitespace
        text (i.e it was OCRed)
        """
        text = ""
        txt_exists = False

        for page in self.pages.all():
            if len(page.text) == 0:
                txt_exists = page.update_text_field()
                # in case .txt for one page is not present - interrupt
                # the whole iteration
                if txt_exists:
                    page.save()
                    logger.debug(
                        f"text saved. len(page.text)=={len(page.text)}"
                    )
                else:
                    # interrupt - if one page's .txt was not found.
                    break
            else:
                logger.debug(
                    f"document_log "
                    f" username={page.user.username}"
                    f" doc_id={page.document.id}"
                    f" page_num={page.number}"
                    f" text_len={len(page.text.strip())}"
                )

            text = text + ' ' + page.text

        if txt_exists:
            # Save this document only in case all .txt
            # were present, otherwise running ./manage.py worker
            # will 'resurrect' deleted documents.
            self.text = text.strip()
            self.save()

        return len(text.strip()) != 0

    @staticmethod
    def paste_pages(
        user,
        parent_id,
        doc_pages,
        dst_document=None,
        after=False,
        before=False,
    ):
        # parent_node is an instance of BaseTreeNode
        # doc_pages is a dictionary of format:
        # {
        #    doc_id_1: [page_num_1a, page_num_2a, ...],
        #    doc_id_2: [page_num_1b, page_num_2b, ...],
        #    doc_id_3: [page_num_1c, page_num_2c, ...]
        # }
        # 1. Create a new document NEWDOC
        # 2. Build new pages for the newly created document
        # num_pages = len(doc_pages[doc_id_1]) + len(doc_pages[doc_id_2]) + ...
        # 3. for each document with ids in doc_pages.keys() (DOC):
        #     a. copy pages data from DOC to NEWDOC
        #     b. deletes pages from DOC (pages mentioned in doc_page[key] list)
        new_page_count = sum(
            [
                len(pages) for pages in doc_pages.values()
            ]
        )

        if new_page_count == 0:
            logger.warning("No pages to paste. Exiting.")
            return

        # 1. Create new document
        # 2. Build new pages for newly created document
        dst_doc_is_new = False
        if not dst_document:
            dst_document = Document.objects.create_document(
                user=user,
                parent_id=parent_id,
                lang=user.preferences['ocr__OCR_Language'],
                title="pasted.pdf",
                size=0,  # updated later, after pdftk will create new doc
                file_name="pasted.pdf",
                page_count=new_page_count
            )
            dst_doc_is_new = True

        # for each document where are pages to paste
        doc_list = []
        data_list = []
        for doc_id in doc_pages.keys():
            try:
                doc = Document.objects.get(id=doc_id)
            except Document.DoesNotExist:
                logger.warning(
                    f"While pasting, doc_id={doc_id} was not found"
                )
                return

            src = default_storage.abspath(doc.path())
            doc_path = doc.path()

            doc_list.append({'doc': doc, 'page_nums': doc_pages[doc_id]})
            data_list.append(
                {
                    'src': src,
                    'doc_path': doc_path,
                    'page_nums': doc_pages[doc_id]
                }
            )

        # returns new document version
        new_version = default_storage.paste_pages(
            dest_doc_path=dst_document.path,
            data_list=data_list,
            dest_doc_is_new=dst_doc_is_new,
            after_page_number=after,
            before_page_number=before
        )

        if new_version == dst_document.version:
            raise Exception("Expecting version to be incremented")

        dst_document.version = new_version
        dst_document.save()
        # update pages model
        dst_document.recreate_pages()

        # delete pages of source document (which where
        # cutted and pasted into new doc)
        for item in doc_list:
            item['doc'].delete_pages(
                page_numbers=item['page_nums']
            )

        return dst_document
        # TODO: update size of the new document (changed doc)

    @property
    def absfilepath(self):
        return default_storage.abspath(
            self.path().url()
        )

    def path(self, version=None):

        if version is None:
            version = self.version

        version = int(version)

        result = DocumentPath(
            user_id=self.user.id,
            document_id=self.id,
            version=version,
            file_name=self.file_name,
        )

        return result

    def page_paths(self, version=None):
        """
        Enables document instance to get quickly page
        paths:

            page_path = doc.page_path[2]
            page_path.url() # local url to second page of the doc.

        This is shortcut method when most used Step(1) is required.
        """

        results = [None]  # indexing starts from 1

        page_count = self.get_pagecount(version=version)

        for page_num in range(1, page_count + 1):
            page_path = PagePath(
                document_path=self.path(version=version),
                page_num=page_num,
                step=step.Step(1),
                page_count=self.get_pagecount(version=version)
            )
            results.append(page_path)

        return results

    def get_page_path(self, page_num, step, version=None):
        """
        For Step(1) shortcut, use doc_instance.page_eps property.
        """
        return PagePath(
            document_path=self.path(version=version),
            page_num=page_num,
            step=step,
            page_count=self.page_count
        )

    def preview_path(self, page, size=None):

        if page > self.page_count or page < 0:
            raise ValueError("Page index out of bound")

        file_name = os.path.basename(self.file_name)
        root, _ = os.path.splitext(file_name)
        page_count = self.pages_num

        if not size:
            size = "orig"

        if page_count <= 9:
            fmt_page = "{root}-page-{num:d}.{ext}"
        elif page_count > 9 and page_count < 100:
            fmt_page = "{root}-page-{num:02d}.{ext}"
        elif page_count > 100:
            fmt_page = "{root}-page-{num:003d}.{ext}"

        return os.path.join(
            self.dir_path,
            str(size),
            fmt_page.format(
                root=root, num=int(page), ext="jpg"
            )
        )

    @property
    def name(self):
        root, ext = os.path.splitext(self.file_name)
        return root

    def add_tags(self, tags):
        """
        tags is an iteratable of papermerge.core.models.Tag instances
        """
        for tag in tags:
            self.tags.add(
                tag,
                tag_kwargs={'user': self.user}
            )


class AbstractDocument(models.Model):
    """
    Common class apps need to inherit from in order
    to extend Document model.

    This class provides a way to extend papermerge.core.models.Document
    model; it does so by creating a foreign key from document extension model
    to the main model.
    These document extension models are called Document parts. They are sort
    of document model chunks holding various extra attributes.

    To add an extra attribute to main document model you need simply to
    create a new model which will inherit from AbstractDocument:

        from django.db import models
        from papermerge.core.models import AbstractDocument

        class DocumentPart(AbstractDocument):

            extra_special_id = models.CharField(
                max_length=50,
                null=True
            )

        There is one very important rule though: you should never
        instantiate DocumentPart class. The ``extra_special_id`` attribute
        will be managed via ``parts`` attribute of core document class
        for example by adding these code in core document creation signal
        handler:

            document.parts.extra_special_id = f"XYZ_{md5(file_name)}"
    """
    base_ptr = models.ForeignKey(
        Document,
        related_name=RELATED_NAME_FMT,
        related_query_name=RELATED_QUERY_NAME_FMT,
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True

    def get_pagecount(self, version=None):
        return self.base_ptr.get_pagecount(version=None)

    def get_title(self):
        return self.base_ptr.title

    def get_file_name(self):
        return self.base_ptr.file_name

    def get_document_fields(self):
        return self.base_ptr.get_document_fields()

    def get_absfilepath(self):
        """
        Returns absolute file path of the latest version
        of the associated file.
        """
        return self.base_ptr.absfilepath


def _part_field_to_json(field_instance):

    # DocumentPart klass (which inherits from AbstractDocument) instance
    # Name of field of document part class instance
    return {
        "class": "choice",
        "value": field_instance.id,
        "choices": ((1, "one"), (2, "two"))
    }
