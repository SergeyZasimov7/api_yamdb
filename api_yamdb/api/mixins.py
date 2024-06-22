from rest_framework import mixins


class ListCreateDestoyMixins(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    Набор миксинов, который предоставляет действия:
    перечислить, создать, удалить.
    """
    pass
