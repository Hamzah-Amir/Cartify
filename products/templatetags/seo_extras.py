"""Small template helpers used to build SEO titles, descriptions and schema."""

import json

from django import template
from django.utils.safestring import mark_safe

from products.models import CATEGORY

register = template.Library()

CATEGORY_LABELS = dict(CATEGORY)


@register.filter
def category_label(slug):
    """'home-kitchen' -> 'Home & Kitchen'. Falls back to a tidied slug."""
    if not slug or slug == "all":
        return ""
    if slug in CATEGORY_LABELS:
        return CATEGORY_LABELS[slug]
    return slug.replace("-", " ").replace("/", " & ").title()


@register.filter
def meta_text(value, length=155):
    """Squash a description onto one line and cut it to a meta-safe length."""
    if not value:
        return ""
    text = " ".join(str(value).split())
    if len(text) <= length:
        return text
    return text[:length].rsplit(" ", 1)[0] + "…"


@register.filter
def json_string(value):
    """Escape a value so it is safe to drop inside a JSON-LD string."""
    return mark_safe(json.dumps(str(value))[1:-1])
