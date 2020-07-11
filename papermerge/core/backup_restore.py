import os
import tarfile

from papermerge.core.models import Document

def backup_documents(backup_path:str):
    allDocuments = Document.objects.all()
    with tarfile.open(backup_path, "w") as backup_archive:
        for currentDocument in allDocuments: #type: Document
            targetPath = _createTargetPath(currentDocument)
            backup_archive.add(currentDocument.absfilepath, arcname=targetPath)


def _createTargetPath(document: Document):
    targetPath = document.file_name
    currentNode = document
    while currentNode.parent is not None:
        currentNode = currentNode.parent
        targetPath = os.path.join(currentNode.title, targetPath)

    return targetPath