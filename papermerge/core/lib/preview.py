
import os
import subprocess
import logging


logger = logging.getLogger(__name__)


class PreviewCoord:
    """
    Groups page number and height (expressed in pixels).

    The idea is that every document preview, asks for specific page
    number and end pixel dimentions of preview. Because these two values
    are so much repeated - they are better regarded as one coordonate system.

    page_count - is optional argument. Is might be used for formatting
            purposes e.g. if there are 32 pages, then 9th page will be
            formatted with as 'page-09' instead of page-9;
            this is peculiarity is result of pdftoppm utility functionality.
    """

    def __init__(
            self,
            page,
            height,
            step,
            min_height,
            max_height,
            page_count=None
    ):

        for value in (page, height):
            self.basic_positive_validation(value)

        self.page = page
        self.min_height = min_height
        self.max_height = max_height
        self.step = step
        self.height = self.normalize_h(height)
        self.page_count = page_count

    def __str__(self):
        return "({}/{}, {})".format(
            self.page,
            self.page_count,
            self.height
        )

    def basic_positive_validation(self, value):
        err_msg = "{} arg must be a non negative int".format(value)

        if not isinstance(value, int):
            raise ValueError(err_msg)

        if value < 0:
            raise ValueError(err_msg)

    def normalize_h(self, height):
        """
        Given a random height value - return the closest valid
        height i.e. from (min_height, min_height + step, ..., max_height)
        """

        step = self.step
        min_height = self.min_height
        max_height = self.max_height

        if height < min_height or height > max_height:
            return InvalidHeight("Out of bound image height value")

        for item_height in range(min_height, max_height + step, step):
            if abs(item_height - height) <= step / 2:
                return item_height


class InvalidHeight(Exception):
    pass


class Preview:
    """
    Generates on the fly previews of a given document.

    # Task is any callable which take as parameters a tuple of
    # strings - first element of which is utility and next ones
    # are utility command line options.
    """

    PREVIEW_EXT = 'jpg'

    def __init__(
        self,
        document_file,
        # It is convenient (in tests) to have a preview
        # object without a task.
        task=None
    ):
        self.document_file = document_file
        self.task = task

    def ppmroot(self, coord):
        """
        Returns PPM-root of document file of given coord.

        PPM-root is defined as term used by pdftoppm utility
        from poppler package. Anyway, it is "template" path for generating
        output files. Let's say we want to extract jpeg page 1 and 2 of
        the document with name XYZ.pdf. We need to answer first two questions:

        * (1) Where to extract ?
        * (2) What will be the name of newly created files?

        PPM-root answers both answers above. A ppm-root of form /A/B/C/nana
        will extract (1) extract files to /A/B/C/ directory and (2) will
        name them as follows:

            /A/B/C/nana-1.jpeg
            /A/B/C/nana-2.jpeg

        PPM-root is part of absolute filename up to "-<number>.<ext>" .
        """

        root = self.document_file.rootname

        return os.path.join(
            self.document_file.dir_path,
            str(coord.height),
            "{}-page".format(root)
        )

    def abspath(self, coord):
        """
        Absolute path of given coord. The format chosen here is
        very dependent on the pdftoppm (part of poppler package)
        utility.
        """
        ppmroot = self.ppmroot(coord)
        logger.debug(
            "ppmroot={root} coord.page_count={count} coord.page={page}".format(
                root=ppmroot,
                count=coord.page_count,
                page=coord.page
            )
        )

        if coord.page_count <= 9:
            fmt_page = "{root}-{num:d}.{ext}"
        elif coord.page_count > 9 and coord.page_count < 100:
            fmt_page = "{root}-{num:02d}.{ext}"
        elif coord.page_count > 100:
            fmt_page = "{root}-{num:003d}.{ext}"

        returned_value = fmt_page.format(
            root=ppmroot, num=int(coord.page), ext=self.PREVIEW_EXT
        )

        logger.debug(
            "abspath={}".format(returned_value)
        )

        return returned_value

    def is_available(self, coord):

        str_abs_path = self.abspath(coord)

        if not os.path.isfile(str_abs_path):
            return False

        try:
            with open(str_abs_path, "rb") as f:
                return True
        except IOError:
            return False

    def breed_preview(self, coord, validate_paths=True):

        if not self.is_available(coord):
            if not self.task:
                msg = "Preview object doesn't have a task object."
                raise ValueError(msg)

            try:
                if self.document_file.is_image:
                    self.task(
                        *self.image_preview_cmdline(
                            coord, validate_paths=validate_paths
                        )
                    )
                else:
                    self.task(
                        *self.offspring_cmdline(
                            coord, validate_paths=validate_paths
                        )
                    )
            except subprocess.CalledProcessError as e:
                print(e.stderr)
                raise

            if not self.is_available(coord):
                logger.error("Preview generating failed")
                # TODO: Enhacement: in case preview fails, return
                # some generic 200px wide thumbnail

        return self.abspath(coord)

    def image_preview_cmdline(
            self,
            coord,
            validate_paths=False
    ):
        """
        Returns a list of string values in same format as accepted
        by convert utility(the one bundled in imagemagick).
        First item in the list if always name
        of utlity iteself (convert).

        When recreate_paths is True - paths given as arguments to convert will
        be checked if they exists - if they don't - a warning will be issued
        and paths will be created.
        """
        input_file_path = self.document_file.abspath
        output_dir_path = os.path.dirname(self.abspath(coord))

        if validate_paths:
            if not self.document_file.exists:
                raise ValueError(
                    "Breeding preview of non-existing doc '{}' failed.".format(
                        input_file_path
                    )
                )
            if not os.path.exists(output_dir_path):
                os.makedirs(output_dir_path)

        ret = (
            "/usr/bin/convert",
            # input file path
            input_file_path,
            # in pdftoppm utility,
            # size is specified with --scale-to Height
            # In convert utility size is specified as WxH :)
            # Thus - resize xH - scale to have height = H
            "-resize",
            "x{}".format(coord.height),
            # output directory path
            "{root}-{num:d}.{ext}".format(
                root=self.ppmroot(coord),
                num=1,
                ext=self.PREVIEW_EXT
            ),
        )

        return ret

    def offspring_cmdline(
        self,
        coord,
        validate_paths=False
    ):
        """
        Returns a list of string values in same format as accepted
        by pdftoppm utility/offspring. First item in the list if always name
        of utlity iteself (pdftoppm).

        When recreate_paths is True - paths given as arguments to pdftoppm will
        be checked if they exists - if they don't - a warning will be issued
        and paths will be created.
        """
        input_file_path = self.document_file.abspath
        output_dir_path = os.path.dirname(self.abspath(coord))

        if validate_paths:
            if not os.path.exists(input_file_path):
                raise ValueError(
                    "Breeding preview of non-existing doc '{}' failed.".format(
                        input_file_path
                    )
                )
            if not os.path.exists(output_dir_path):
                os.makedirs(output_dir_path, exist_ok=True)

        # for thumbnail images, poor jpeg qulity
        # is acceptable. We save same space this way.
        if coord.height < 300:
            quality = 40
        else:
            quality = 90
        # each argument must be a separate entry in array
        # https://stackoverflow.com/questions/53628699/subprocess-run-simple-scenario-fails
        ret = (
            "pdftoppm",
            "-jpeg",
            "-f",
            str(coord.page),
            "-l",  # generate only one page
            str(coord.page),
            "-scale-to",
            str(coord.height),
            "-jpegopt",
            "quality={}".format(quality),
            # input file path
            input_file_path,
            # output directory path
            self.ppmroot(coord),
        )

        return ret
