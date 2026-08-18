COMPILE_CALLS = 0


def reset_stats():
    global COMPILE_CALLS
    COMPILE_CALLS = 0


def get_stats():
    return {"compile_calls": COMPILE_CALLS}


def _escape(value):
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def compile_template(tokens, autoescape=False):
    global COMPILE_CALLS
    COMPILE_CALLS += 1

    def render(context, filters=None):
        filters = filters or {}
        out = []
        for kind, value in tokens:
            if kind == "text":
                out.append(value)
            elif kind == "var":
                rendered = context.get(value, "")
                out.append(_escape(rendered) if autoescape else str(rendered))
            elif kind == "upper":
                func = filters.get("upper", lambda item: str(item).upper())
                out.append(str(func(context.get(value, ""))))
        return "".join(out)

    return render
