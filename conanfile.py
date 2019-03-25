from conans import ConanFile, tools

def git_get_semver():
    """Uses git to work out a semver compliant version tag"""
    git = tools.Git()
    try:
        # If not in a git repo this command will output error to stderr.
        # So we redirect the error message to /dev/null
        prev_tag = git.run("describe --tags --abbrev=0 2> /dev/null")
        commits_behind = int(git.run("rev-list --count %s..HEAD" % (prev_tag)))
        # Commented out checksum due to a potential bug when downloading from bintray
        #checksum = git.run("rev-parse --short HEAD")
        if prev_tag.startswith("v"):
            prev_tag = prev_tag[1:]
        if commits_behind > 0:
            prev_tag_split = prev_tag.split(".")
            prev_tag_split[-1] = str(int(prev_tag_split[-1]) + 1)
            output = "%s-%d" % (".".join(prev_tag_split), commits_behind)
        else:
            output = "%s" % (prev_tag)
        return output
    except:
        return '0.0.0'

class ConanTools(ConanFile):
    name = "conan-tools"
    version = git_get_semver()
    license = "Apache-2.0"
    description = "Functions used across multiple conanfile.py in the IncludeOS project"
    url = "https://github.com/includeos/conanTools"
