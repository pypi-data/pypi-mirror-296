import logging
from concurrent.futures import ThreadPoolExecutor
from gettext import gettext as _
from multiprocessing import cpu_count
from pathlib import Path

import cv2

from ritm_annotation.utils.misc import try_tqdm

COMMAND_DESCRIPTION = _(
    # noqa: E501
    "Looks for common problems in datasets in mask form that are used for finetuning and generated by the annotator"
)

logger = logging.getLogger(__name__)


def command(parser):
    parser.add_argument(
        "input",
        type=Path,
        help=_("Folder where the ground truths/masks are stored"),
    )
    parser.add_argument(
        "-i",
        "--images",
        dest="images",
        type=Path,
        help=_("Folder where the dataset images are stored"),
    )
    parser.add_argument(
        "-j",
        "--jobs",
        dest="jobs",
        type=int,
        default=cpu_count(),
        help=_("How many concurrent checks"),
    )

    def handle(args):
        assert args.input.is_dir(), _("Dataset must be a directory")
        assert args.images is None or args.images.is_dir(), _(
            "Invalid image directory"
        )
        if args.images is not None:
            logger.info(_("Using images with masks!"))

        def handle_one(item):
            if not item.is_dir():
                logger.warning(_("'{item}': Dataset noise").format(item=item))
                return
            item_img = None
            if args.images is not None:
                image_file = args.images / item.name
                if not image_file.exists():
                    logger.warning(
                        _("'{image_file}': Image file doesn't exist").format(
                            image_file=image_file
                        )
                    )
                else:
                    item_img = cv2.imread(str(image_file))
                    if item_img is None:
                        logger.error(
                            _("'{item_img}': Invalid image").format(
                                item_img=item_img
                            )
                        )
                    else:
                        item_img = cv2.cvtColor(item_img, cv2.COLOR_BGR2RGB)
            for mask in item.iterdir():
                if mask.name.endswith(".json"):
                    continue
                mask_img = cv2.imread(str(mask), 0)
                if mask_img is None:
                    logger.error(_("'{mask}': Invalid mask").format(mask=mask))
                    continue
                if item_img is not None:
                    (wi, hi, di) = item_img.shape
                    (wm, hm) = mask_img.shape
                    if wi != wm:
                        logger.error(
                            _(
                                "'{mask}': First dimension doesn't match for image and mask"
                            ).format(
                                mask=mask
                            )  # noqa:E501
                        )
                    if hi != hm:
                        logger.error(
                            _(
                                "'{mask}': Second dimension doesn't match for image and mask"
                            ).format(
                                mask=mask
                            )  # noqa:E501
                        )

        items = list(args.input.iterdir())
        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            ops = try_tqdm(
                executor.map(handle_one, items, chunksize=8), total=len(items)
            )
            for item in ops:
                pass

    return handle
