from datetime import datetime


class Widget(object):
    """
    Widget takes care of converting between import and export representations.

    Widget objects have two functions:

    * converts object field value to export representation

    * converts import value and converts it to appropriate python
      representation
    """
    def clean(self, value):
        """
        Returns appropriate python objects for import value.
        """
        return value

    def render(self, value):
        """
        Returns export representation of python value.
        """
        return unicode(value)


class IntegerWidget(Widget):
    """
    Widget for converting integer fields.
    """

    def clean(self, value):
        if not value:
            return None
        return int(value)


class CharWidget(Widget):
    """
    Widget for converting text fields.
    """

    def render(self, value):
        return unicode(value)


class BooleanWidget(Widget):
    """
    Widget for converting boolean fields.
    """
    TRUE_VALUE = "1"
    FALSE_VALUE = "0"

    def render(self, value):
        return self.TRUE_VALUE if value else self.FALSE_VALUE

    def clean(self, value):
        return True if value == self.TRUE_VALUE else False


class DateWidget(Widget):
    """
    Widget for converting date fields.

    Takes optional ``format`` parameter.
    """

    def __init__(self, format=None):
        if format is None:
            format = "%Y-%m-%d"
        self.format = format

    def clean(self, value):
        if not value:
            return None
        return datetime.strptime(value, self.format).date()

    def render(self, value):
        return value.strftime(self.format)


class DateTimeWidget(Widget):
    """
    Widget for converting date fields.

    Takes optional ``format`` parameter.
    """

    def __init__(self, format=None):
        if format is None:
            format = "%Y-%m-%d %H:%M:%S"
        self.format = format

    def clean(self, value):
        if not value:
            return None
        return datetime.strptime(value, self.format)

    def render(self, value):
        return value.strftime(self.format)


class ForeignKeyWidget(Widget):
    """
    Widget for ``ForeignKey`` model field that represent ForeignKey as
    integer value.

    Requires a positional argument: the class to which the field is related.
    """

    def __init__(self, model, *args, **kwargs):
        self.model = model
        super(ForeignKeyWidget, self).__init__(*args, **kwargs)

    def clean(self, value):
        pk = super(ForeignKeyWidget, self).clean(value)
        return self.model.objects.get(pk=pk) if pk else None

    def render(self, value):
        if value is None:
            return ""
        return value.pk
