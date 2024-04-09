from uuid import uuid4


def rename_profile_image(instance, filename):
    new_filename = str(uuid4())
    return 'profile/{}'.format(new_filename)
