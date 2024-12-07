from pydantic import BaseModel

from gui.resources.images.start_page.image_1 import image_1_path
from gui.resources.images.selection_interface_page.image_2 import image_2_path
from gui.resources.images.selection_interface_page.image_3 import image_3_path
from gui.resources.images.selection_interface_page.image_4 import image_4_path
from gui.resources.images.drowsiness_page.image_5 import image_5_path

from gui.resources.fonts.brittany_font import brittany_font_path
from gui.resources.fonts.cardo_font import cardo_font_path


class ImagePaths(BaseModel):
    # start page
    image_1: str = image_1_path

    # selection interface page
    image_2: str = image_2_path
    image_3: str = image_3_path
    image_4: str = image_4_path

    # drowsiness page
    image_5: str = image_5_path


class FontsPath(BaseModel):
    brittany_font: str = brittany_font_path
    cardo_font: str = cardo_font_path
