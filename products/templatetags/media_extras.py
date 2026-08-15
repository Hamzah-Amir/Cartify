"""Helpers for rendering product images safely.

Product.image is an ImageField, so it stores a path relative to MEDIA_ROOT
(e.g. "products/ps5.jpeg") and `.url` turns that into "/media/products/ps5.jpeg".

Two things can still go wrong, and this filter handles both:

1. Empty image  -> `.url` raises ValueError. We show a placeholder instead.
2. A row left over from when the field was a URLField, holding a full
   "https://..." link. Django would percent-encode that into
   "/media/https%3A/example.com/..." which 404s, so we return the link as-is.
"""

from django import template
from django.templatetags.static import static

register = template.Library()

PLACEHOLDER = "img/placeholder.svg"


@register.filter
def image_url(value):
    """Return a usable src for an ImageField, or a placeholder."""
    if not value:
        return static(PLACEHOLDER)

    # FieldFile stores the path in .name; a plain string has none
    name = (getattr(value, "name", None) or str(value)).strip()
    if not name:
        return static(PLACEHOLDER)

    # legacy rows that hold a real link - use it directly
    if name.startswith(("http://", "https://", "//")):
        return name

    # the normal case: an uploaded file
    try:
        return value.url
    except (AttributeError, ValueError):
        pass

    # a plain string that is already root-relative
    if name.startswith("/"):
        return name

    # a bare filename would be resolved against the current page, so refuse it
    return static(PLACEHOLDER)
