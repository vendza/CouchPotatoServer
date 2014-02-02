from hashlib import md5
from CodernityDB.tree_index import TreeBasedIndex


class ReleaseIndex(TreeBasedIndex):

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '32s'
        super(ReleaseIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        return md5(key).hexdigest()

    def make_key_value(self, data):
        if data.get('_t') == 'release' and data.get('media_id'):
            return md5(data['media_id']).hexdigest(), {'media_id': data.get('media_id')}

    def run_for_media(self, db, media_id):
        for release in db.get_many('release', media_id, with_doc = True):
            yield release['doc']

    def run_with_status(self, db, status = []):

        status = list(status if isinstance(status, (list, tuple)) else [status])

        for s in status:
            for ms in db.get_many('release_status', s, with_doc = True):
                yield ms['doc']


class ReleaseStatusIndex(TreeBasedIndex):

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '32s'
        super(ReleaseStatusIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        return md5(key).hexdigest()

    def make_key_value(self, data):
        if data.get('_t') == 'release' and data.get('status'):
            return md5(data.get('status')).hexdigest(), None


class ReleaseIDIndex(TreeBasedIndex):

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '32s'
        super(ReleaseIDIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        return md5(key).hexdigest()

    def make_key_value(self, data):
        if data.get('_t') == 'release' and data.get('identifier'):
            return md5(data.get('identifier')).hexdigest(), None
