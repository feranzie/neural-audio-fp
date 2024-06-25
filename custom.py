def get_custom_db_ds(self, source_root_dir):
    """ Construc DB (or query) from custom source files. """

    query_path = sorted(
        glob.glob(str(source_root_dir) + '/query/*.wav', recursive=True))
    db_path = sorted(
        glob.glob(str(source_root_dir) + '/db/*.wav', recursive=True))
    
    _ts_n_anchor = self.ts_batch_sz # Only anchors...

    query_ds = genUnbalSequence(
        db_path,
        self.ts_batch_sz,
        _ts_n_anchor,
        self.dur,
        self.hop,
        self.fs,
        shuffle=False,
        random_offset_anchor=False) # No augmentations, No drop-samples.
    db_ds = genUnbalSequence(
        query_path,
        self.ts_batch_sz,
        _ts_n_anchor,
        self.dur,
        self.hop,
        self.fs,
        shuffle=False,
        random_offset_anchor=False)
    return query_ds, db_ds

