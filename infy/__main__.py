from . import run
import pkg_resources
print(pkg_resources.resource_filename(__name__, 'assets/lean.svg'))
print('running run()')
run()
print('ran run()')
