# To use this script, simply import it your setup.py file, and use the
# results of get_git_version() as your package version:
#
# from version import *
#
# setup(
#     version=get_git_version(),
#     .
#     .
#     .
# )
#

__all__ = ("get_git_version",)

from subprocess import Popen, PIPE


def call_git_describe(abbrev=6):
    try:
        p = Popen(['git', 'describe', '--abbrev=%d' % abbrev],
                  stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readlines()[0]
        return line.strip()

    except:
        return None


def read_release_version():
    try:
        f = open("RELEASE-VERSION", "r")

        try:
            version = f.readlines()[0]
            return version.strip()

        finally:
            f.close()

    except:
        return None


def write_release_version(version):
    f = open("RELEASE-VERSION", "w")
    f.write("%s\n" % version)
    f.close()


def get_git_version(abbrev=6):
    # Read in the version that's currently in RELEASE-VERSION.
    release_version = read_release_version()

    version = call_git_describe(abbrev)

    # If that doesn't work, fall back on the value that's in RELEASE-VERSION.
    if version is None:
        version = release_version

    # Adapt to PEP 386 compatible versioning scheme
    version = pep_386_adapt(version)

    # If we still don't have anything, that's an error.
    if version is None:
        raise ValueError("Cannot find the version number!")

    # Remove version prefix 'v' from version number
    if version[0] == 'v':
        version = version[1:]

    # If the current version is different from what's in the
    # RELEASE-VERSION file, update the file to be current.

    if version != release_version:
        write_release_version(version)

    return version


def pep_386_adapt(version):
    if version is not None and '-' in version:
        # Adapt git-describe version to be in line with PEP 386
        parts = version.split('-')
        parts[-2] = 'post' + parts[-2]
        version = '.'.join(parts[:-1])

    return version


if __name__ == "__main__":
    print get_git_version()
