# Copyright (c) 2016-2017, NVIDIA CORPORATION.  All rights reserved.
from __future__ import absolute_import

import os

import wtforms
from flask.ext.wtf import Form
from wtforms import validators

from digits import utils
from digits.utils import subclass
from digits.utils.forms import validate_required_iff


@subclass
class DatasetForm(Form):
    """
    A form used to create an image processing dataset
    """

    method = wtforms.SelectField(u'Dataset type',
                                 choices=[
                                     ('folder', 'Folder'),
                                     ('textfile', 'Textfiles'),
                                 ],
                                 default='folder',
                                 )

    def validate_folder_path(form, field):
        if not field.data:
            pass
        else:
            # make sure the filesystem path exists
            if not os.path.exists(field.data) or not os.path.isdir(field.data):
                raise validators.ValidationError(
                    'Folder does not exist or is not reachable')
            else:
                return True

    def validate_file_path(form, field):
        if not field.data:
            pass
        else:
            # make sure the filesystem path exists
            if not os.path.exists(field.data) and not os.path.isdir(field.data):
                raise validators.ValidationError(
                    'File does not exist or is not reachable')
            else:
                return True

    feature_file = utils.forms.StringField(
        u'Feature image list file (.txt)',
        validators=[
            validate_file_path
        ],
        tooltip="Indicate a file list full of images."
    )

    label_file = utils.forms.StringField(
        u'Label image list file (.txt)',
        validators=[
            validate_file_path
        ],
        tooltip="Indicate a file list full of images. For each image in the feature"
                " image file list there must be one corresponding image in the label"
                " image file list. The label image must have the same filename except"
                " for the extension, which may differ. Label images are expected"
                " to be single-channel images (paletted or grayscale), or RGB"
                " images, in which case the color/class mappings need to be"
                " specified through a separate text file."
    )

    folder_pct_val = utils.forms.IntegerField(
        u'% for validation',
        default=10,
        validators=[
            validators.NumberRange(min=0, max=100)
        ],
        tooltip="You can choose to set apart a certain percentage of images "
                "from the training images for the validation set."
    )

    has_val_folder = utils.forms.BooleanField('Separate validation images',
                                              default=False,
                                              )

    validation_feature_file = utils.forms.StringField(
        u'Validation feature image list file (.txt)',
        validators=[
          validate_file_path
        ],
        tooltip="Indicate a file list full of images."
    )

    validation_label_file = utils.forms.StringField(
        u'Validation label image list file (.txt)',
        validators=[
          validate_file_path
        ],
        tooltip="Indicate a file list full of images. For each image in the feature"
                " image file list there must be one corresponding image in the label"
                " image file list. The label image must have the same filename except"
                " for the extension, which may differ. Label images are expected"
                " to be single-channel images (paletted or grayscale), or RGB"
                " images, in which case the color/class mappings need to be"
                " specified through a separate text file."
    )

    channel_conversion = utils.forms.SelectField(
        'Channel conversion',
        choices=[
            ('RGB', 'RGB'),
            ('L', 'Grayscale'),
            ('none', 'None'),
        ],
        default='none',
        tooltip="Perform selected channel conversion on feature images. Label"
                " images are single channel and not affected by this parameter."
    )

    class_labels_file = utils.forms.StringField(
        u'Class labels (optional)',
        validators=[
            validate_file_path,
        ],
        tooltip="The 'i'th line of the file should give the string label "
                "associated with the '(i-1)'th numeric label. (E.g. the "
                "string label for the numeric label 0 is supposed to be "
                "on line 1.)"
    )

    colormap_method = utils.forms.SelectField(
        'Color map specification',
        choices=[
            ('label', 'From label image'),
            ('textfile', 'From text file'),
        ],
        default='label',
        tooltip="Specify how to map class IDs to colors. Select 'From label "
                "image' to use palette or grayscale from label images. For "
                "RGB image labels, select 'From text file' and provide "
                "color map in separate text file."
    )

    colormap_text_file = utils.forms.StringField(
        'Color map file',
        validators=[
            validate_required_iff(colormap_method="textfile"),
            validate_file_path,
        ],
        tooltip="Specify color/class mappings through a text file. "
                "Each line in the file should contain three space-separated "
                "integer values, one for each of the Red, Green, Blue "
                "channels. The 'i'th line of the file should give the color "
                "associated with the '(i-1)'th class. (E.g. the "
                "color for class #0 is supposed to be on line 1.)"
    )
