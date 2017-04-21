from utils.runner import update, fastUpdate


def run(*args):
    # skip recache lastactivity and speeches
    skipPersonRecache = True if 'fastUpdate' in args else False
    fastUpdate(fast=skipPersonRecache)
