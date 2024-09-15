import glob
import os

from .svc import svc


# --------------------
## perform the do_lint operation
class DoLint:
    # --------------------
    ## do_lint mainline.
    #
    # @param tech   technology: python, cpp or arduino
    # @param dogen  "dogen" generate build files, otherwise not
    # @param tool   for python: pylint (default) or ruff; for cpp: cppcheck or clang-tidy(default)
    # @return None
    def run(self, tech, dogen, tool):
        if not tech:
            # default to xplat.cfg value
            tech = svc.cfg.mod_tech
        if not tech:
            # not set, the default to python
            tech = 'python'

        if dogen == 'dogen':
            dogen = True
        else:
            dogen = False

        svc.log.highlight(f'{svc.gbl.tag}: starting tech:{tech} dogen:{dogen}...')
        if tech == 'python':
            self.run_python(dogen, tool)
        elif tech in ['cpp', 'arduino']:
            # arduino defaults to same as C++
            self.run_cpp(tool)
        else:
            svc.gbl.rc += 1
            svc.log.err(f'unknown tech:{tech}, use one of: python, cpp, arduino')

        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: pylint rc={svc.gbl.rc}')

    # --------------------
    ## run pylint
    #
    # @return None
    def run_python(self, dogen=False, tool='pylint'):
        if dogen:
            svc.gen_files.all(False)

        if not tool:
            tool = 'pylint'

        # always run pycodestyle
        svc.log.highlight(f'{svc.gbl.tag}: running pycodestyle')
        svc.utils_ps.run_process('pycodestyle', use_raw_log=True)
        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: pycodestyle rc={svc.gbl.rc}')

        if tool == 'pylint':
            svc.log.highlight(f'{svc.gbl.tag}: running pylint')
            dirs = self._get_dirs()
            rc_path = os.path.join(svc.utils_fs.root_dir, 'tools', 'pylint.rc')
            cmd = f'pylint --rcfile={rc_path} {dirs}'
            svc.utils_ps.run_process(cmd, use_raw_log=True)
        elif tool == 'ruff':
            svc.log.highlight(f'{svc.gbl.tag}: running ruff')
            toml_path = os.path.join(svc.utils_fs.root_dir, 'tools', 'xplat_utils', 'ruff.toml')
            cmd = f'ruff check --config {toml_path}'
            svc.utils_ps.run_process(cmd, use_raw_log=True)
        else:
            svc.gbl.rc += 1
            svc.log.err(f'unknown tool:"{tool}", use one of: pylint, ruff')

    # --------------------
    ## get list of directories to lint
    #
    # @return list of directories
    def _get_dirs(self):
        modules = ''
        if svc.cfg.is_module:
            modules += f'{svc.cfg.mod_dir_name} '
        else:
            modules += 'lib '

        files = glob.glob('*.py')
        if files:
            modules += '*.py '

        if svc.cfg.do_lint.include_tools:
            svc.log.line(f'{svc.gbl.tag}: including "tools" directory')
            modules += 'tools '
            path = os.path.join('tools', 'xplat_utils')
            modules += f'{path} '

        # include ver and ut only if the directories exist
        if os.path.isdir('ver'):
            modules += 'ver '
        if os.path.isdir('ut'):
            modules += 'ut '

        return modules

    # --------------------
    ## run cppcheck or clang-tidy
    #
    # @param tool  which lint tool to use: clang-tidy(default), cppcheck
    # @return None
    def run_cpp(self, tool):
        if not tool:
            # set default tool
            tool = 'cppcheck'

        if tool == 'clang-tidy':
            # skip regen for Makefile projects
            if os.path.isfile('CMakeLists.txt'):
                svc.log.highlight(f'{svc.gbl.tag}: cmake refresh compile_commands')
                cmd = 'cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON cmake-build-debug/'
                svc.utils_ps.run_process(cmd, use_raw_log=False)
                svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: compile_commands rc={svc.gbl.rc}')

            modules = ''
            # location of source files being covered
            for src_dir in svc.cfg.do_lint.src_dirs:
                modules += f'{src_dir}/* '  # pylint: disable=consider-using-join

            svc.log.highlight(f'{svc.gbl.tag}: run clang-tidy on: {modules}')
            cmd = f'clang-tidy -p=cmake-build-debug/compile_commands.json --quiet --header-filter=.* {modules}'
            svc.utils_ps.run_process(cmd, use_raw_log=False)
            svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: clang-tidy rc={svc.gbl.rc}')
        elif tool == 'cppcheck':
            modules = ''
            # location of source files being covered
            for src_dir in svc.cfg.do_lint.src_dirs:
                modules += f'{src_dir} '  # pylint: disable=consider-using-join

            svc.log.highlight(f'{svc.gbl.tag}: run cppcheck on: {modules}')
            cmd = f'cppcheck --enable=all --inconclusive  --max-ctu-depth=5 --language=c++ {modules}'
            svc.utils_ps.run_process(cmd, use_raw_log=False)
            svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: cppcheck rc={svc.gbl.rc}')
        else:
            svc.gbl.rc += 1
            svc.log.err(f'unknown tool:"{tool}", use one of: clang-tidy, cppcheck')
