from cmlibs.zinc.context import Context
from cmlibs.zinc.fieldmodule import Fieldmodule
from cmlibs.zinc.region import Region


def load_zinc(context_name: str = 'scaffold') -> tuple[Context, Region, Fieldmodule]:
    """
    Only needed because type annotations do not work by default with a lof of the Zinc objects.
    A simple way to get around this is to load the classes in this file and specify the class
    on the return arguments. In time I might add more and more arguments to this function

    :param context_name: Name of the context
    :type context_name: str
    :return: List with all the zinc-y objects
    :rtype: list[Context, Region, Fieldmodule]
    """
    context = Context(context_name)
    region = context.getDefaultRegion()
    fieldmodule = region.getFieldmodule()
    return [context, region, fieldmodule]
