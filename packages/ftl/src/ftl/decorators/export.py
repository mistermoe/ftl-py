def export(func):
    func._is_ftl_export = True
    return func