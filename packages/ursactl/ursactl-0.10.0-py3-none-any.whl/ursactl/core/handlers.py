def action(event_name):
    def annotate_action(func):
        func.event_name = event_name
        return func

    return annotate_action


def perception(perception_name):
    def annotate_perception(func):
        func.perception_name = perception_name
        return func

    return annotate_perception


class HandlerMetaclass(type):
    def __new__(cls, name, bases, dct):
        h = super().__new__(cls, name, bases, dct)
        actions = {}
        perceptions = {}
        for name, method in dct.items():
            if hasattr(method, "event_name"):
                actions[method.event_name] = method
            if hasattr(method, "perception_name"):
                perceptions[method.perception_name] = method
        h.actions = actions
        h.perceptions = perceptions
        return h


class Handler(metaclass=HandlerMetaclass):
    pass
