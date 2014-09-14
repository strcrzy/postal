import re
"""
postal.router
core logic for routing messages
"""


class Router():
    """
    a Router has Routes added to it, either directly via add_route, or
    indirectly via @router.match. it processes messages by attempting to match
    them against routes it knows about, in order, passing the message to the
    first matching receiver.
    """
    def __init__(self, routes=[]):
        self.routes = routes

    def add_route(self, predicate, receiver):
        self.routes.append(Route(predicate, receiver))

    def match(self, func=None, **options):
        """
        annotation provided as a convenience method to define routes.
        keyword arguments:
        from_ - string or regex to match against the sender of the message
        to - string or regex to match against the receiver of the message
        subject - string or regex to match against the subject of the message
        """
        if func is not None:
            if options:
                if len(options) is 1:
                    field = options.keys()[0].replace('_', '')
                    self.add_route(RegexPredicate(field, options[field]), func)
                else:
                    predicates = [RegexPredicate(field.replace('_', ''), regex)
                                  for field, regex in options.iteritems()]
                    self.add_route(AndPredicate(predicates), func)
            else:
                self.add_route(DefaultPredicate(), func)

            def inner(*args, **kwargs):
                func(*args, **kwargs)
            return inner
        else:
            def partial_inner(func):
                return self.match(func, **options)
            return partial_inner

    def route(self, msg):
        """
        attempt to match the message against one of the routes. if the message
        matches a route's predicate call its receiver with the matching message
        """
        print("route")
        for route in self.routes:
            if route.attempt(msg):
                return True
        return False


class Route():
    def __init__(self, predicate, receiver):
        self.predicate = predicate
        self.receiver = receiver

    def attempt(self, msg):
        if self.predicate.evaluate(msg):
            print("attempting")
            self.receiver(msg, **msg.matches)
            return True
        else:
            return False


class RegexPredicate():
    def __init__(self, field, regex):
        self.field = field
        self.regex = regex

    def evaluate(self, msg):
        match = re.match(self.regex, msg[self.field.capitalize()])
        print("matching %s against %s" % (self.regex, msg[self.field.capitalize()]))
        if match:
            print("matched")
            matches = msg.__dict__.get('matches', {})
            matches.update(match.groupdict())
            msg.matches = matches
            return True
        else:
            return False


class AndPredicate():
    def __init__(self, predicates):
        self.predicates = predicates

    def evaluate(self, msg):
        for predicate in self.predicates:
            if not predicate.evaluate(msg):
                return False
        return True
