# --------------------
## holds global information
class Gbl:
    ## hold the name of the build directory; default is debug
    build_dir = 'debug'

    # --------------------
    ## override the default build directory name
    #
    # @param build_dir  the new build directory
    # @return None
    def set_build_dir(self, build_dir):
        ## see Gbl.build_dir
        self.build_dir = build_dir
