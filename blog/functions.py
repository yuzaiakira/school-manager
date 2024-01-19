from uuid import uuid4

def path_and_rename(instance, filename):
    return 'blog/{0}{1}'.format(str(uuid4())[:8], filename)

