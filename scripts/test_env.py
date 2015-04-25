import traceback

def test_dev_env():
    try:
        import turntable  # NOQA
    except Exception, e:
        print '... INCOMPLETE ENVIORNMENT!'
        print '... %s' % e
        print '...'
        print traceback.format_exc()
    else:
        print "... ENVIRONMENT WELL-DEFINED"


if __name__ == '__main__':
    test_dev_env()
