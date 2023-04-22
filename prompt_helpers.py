from generate_image import generate_image


QUALITY = ', professional, highly detailed, HDR, UHD, 64k'

# Image type
PHOTO = 'photo of'

# Perspective
CLOSE_UP = ', close up, macro lens'
WIDE_SHOT = ', wide shot, EF 70mm'

# Environment
STUDIO = ', studio, day, studio lighting'
OUTSIDE = ', outdoors, day, natural lighting'


def generate_object_close_up(description):
    generate_image(f"{PHOTO} {description} {CLOSE_UP} {STUDIO} {QUALITY}")


def generate_outside_wide_shot(description):
    generate_image(f"{PHOTO} {description} {WIDE_SHOT} {OUTSIDE} {QUALITY}")
