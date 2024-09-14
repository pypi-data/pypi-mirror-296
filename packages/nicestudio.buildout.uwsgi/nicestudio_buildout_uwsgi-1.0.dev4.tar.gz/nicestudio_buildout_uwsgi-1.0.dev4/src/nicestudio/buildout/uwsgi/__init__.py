# -*- coding: utf-8 -*-
# Copyright (c) 2024 niceStudio, Inc. All rights reserved.
# See also LICENSE.txt
import os
import shutil
import sys
import tempfile
import xml.etree.ElementTree as ET

import setuptools
import zc
import zc.recipe.egg
from zc.buildout import UserError
from zc.buildout.download import Download

# from xml.etree.ElementTree import indent

DOWNLOAD_URL = 'http://projects.unbit.it/downloads/uwsgi-latest.tar.gz'
EXCLUDE_OPTIONS = {
    'bin-directory', 'develop-eggs-directory', 'eggs', 'eggs-directory', 'executable', 'extra-paths', 'output',
    'download-url', 'find-links', 'python', 'recipe', 'pth-files', 'force-install-executable'}

_oprp = getattr(os.path, 'realpath', lambda path: path)


def realpath(path):
    return os.path.normcase(os.path.abspath(_oprp(path)))


class UWSGI:
    f"""
    Buildout recipe downloading, compiling if not exists, and configuring python paths for uWSGI.

    Usage::
    
        [uwsgi]
        recipe = nicestudio.buildout.uwsgi
        output = <OUTPUT_FILE_PATH>
        executable = <UWSGI_FILE_PATH>
        download-url = <DOWNLOAD_URL>
        force-install-executable = <FORCE_INSTALL_EXECUTABLE>
        <UWSGI_OPTION_NAME> = <UWSGI_OPTION_VALUE>
    
    OUTPUT_FILE_PATH: the output file path.
    UWSGI_FILE_PATH: the uWSGI file path.
    DOWNLOAD_URL: the download URL. default={DOWNLOAD_URL}
    FORCE_INSTALL_EXECUTABLE: force installation of uWSGI executable. default=false
    UWSGI_OPTION_NAME: the uWSGI option name. Ref: https://uwsgi-docs.readthedocs.io/en/latest/Options.html
    UWSGI_OPTION_VALUE: the uWSGI option value. Ref: https://uwsgi-docs.readthedocs.io/en/latest/Options.html
    """

    def __init__(self, buildout, name, options):
        self.egg = zc.recipe.egg.Egg(buildout, options['recipe'], options)
        self.name = name
        self.buildout = buildout

        if 'extra-paths' in options:
            options['pythonpath'] = options['extra-paths']
        else:
            options.setdefault('extra-paths', options.get('pythonpath', ''))

        self.output = options.get('output')
        if not self.output:
            self.output = os.path.join(
                self.buildout['buildout']['parts-directory'],
                self.name,
                'uwsgi.xml')

        # Collect configuration params from options.
        self.executable = options.get(
            'executable',
            os.path.join(buildout['buildout']['bin-directory'], name)
        )
        self.download_url = options.get('download-url', DOWNLOAD_URL)

        self.conf = dict(
            [(k, v) for k, v in options.items() if not k.startswith('_') and k not in EXCLUDE_OPTIONS]
        )
        self.options = options

    def download_release(self):
        """Download uWSGI release based on 'version' option and return
        path to downloaded file.
        """
        cache = tempfile.mkdtemp('download-cache')
        download = Download(cache=cache)
        download_path, is_temp = download(self.download_url)
        return download_path

    def extract_release(self, download_path):
        """Extracts uWSGI package and returns path containing
        uwsgiconfig.py along with path to extraction root.
        """
        uwsgi_path = None
        extract_path = tempfile.mkdtemp("-uwsgi")
        setuptools.archive_util.unpack_archive(download_path, extract_path)
        for root, dirs, files in os.walk(extract_path):
            if 'uwsgiconfig.py' in files:
                uwsgi_path = root
        return uwsgi_path, extract_path

    def build_release(self, uwsgi_path):
        """Build uWSGI and returns path to executable.
        """
        # Change dir to uwsgi_path for compile.
        sys_path_changed = False
        current_path = os.getcwd()
        os.chdir(uwsgi_path)

        try:
            # Add uwsgi_path to the Python path so we can import uwsgiconfig.
            if uwsgi_path not in sys.path:
                sys.path.append(uwsgi_path)
                sys_path_changed = True

            # Build uWSGI.
            uwsgiconfig = __import__('uwsgiconfig')
            bconf = '%s/buildconf/default.ini' % uwsgi_path
            uconf = uwsgiconfig.uConf(bconf)
            uconf.set('bin_name', self.name)
            uwsgiconfig.build_uwsgi(uconf)
        finally:
            # Change back to original path and remove uwsgi_path from
            # Python path if added.
            os.chdir(current_path)
            if sys_path_changed:
                sys.path.remove(uwsgi_path)

        shutil.copy(os.path.join(uwsgi_path, self.name), self.executable)

    def get_extra_paths(self):
        """Returns extra paths to include for uWSGI.
        """
        # Add libraries found by a site .pth files to our extra-paths.
        if 'pth-files' in self.options:
            import site
            for pth_file in self.options['pth-files'].splitlines():
                pth_libs = site.addsitedir(pth_file, set())
                if not pth_libs:
                    self.log.warning(
                        "No site *.pth libraries found for pth_file=%s" % (
                            pth_file,))
                else:
                    self.log.info("Adding *.pth libraries=%s" % pth_libs)
                    self.options['extra-paths'] += '\n' + '\n'.join(pth_libs)

        # Add local extra-paths.
        return [p.replace('/', os.path.sep) for p in
                self.options['extra-paths'].splitlines() if p.strip()]

    def create_xml_content(self, egg_paths):
        root = ET.Element('uwsgi')

        for key, value in self.conf.items():
            value = (value or "").lower()

            if value in ("true", "on", "yes"):
                ET.SubElement(root, key)
            else:
                if value not in ("false", "off", "no"):
                    for item in value.split("\n"):
                        ET.SubElement(root, key).text = item
                else:
                    ET.SubElement(root, key).text = value

        for egg_path in egg_paths:
            ET.SubElement(root, "pythonpath").text = egg_path

        ET.indent(root, space='    ')
        return ET.tostring(root, encoding='UTF-8').decode('UTF-8')

    def install(self):
        require_install = self.options.get('force-install-executable', False)
        if not require_install:
            if not os.path.exists(self.executable):
                # if executable is not existed, set `require_install` to `True`
                require_install = True
            elif not os.path.isfile(self.executable):
                raise UserError("'%s' existed, but it is not file" % self.executable)

        if require_install:
            # Download uWSGI.
            download_path = self.download_release()

            # Extract uWSGI.
            uwsgi_path, extract_path = self.extract_release(download_path)

            try:
                # Build uWSGI.
                self.build_release(uwsgi_path)
            finally:
                # Remove extracted uWSGI package.
                shutil.rmtree(extract_path)

        requirements, ws = self.egg.working_set()
        eggs_paths = [dist.location for dist in ws]
        eggs_paths.extend(self.get_extra_paths())
        # order preserving unique
        unique_egg_paths = []
        for p in eggs_paths:
            if p not in unique_egg_paths:
                unique_egg_paths.append(p)
        egg_paths = map(realpath, unique_egg_paths)

        output_dir = os.path.dirname(self.output)
        if output_dir and not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        content = self.create_xml_content(egg_paths)
        with open(self.output, 'w') as fp:
            fp.write(content)
        return [self.output]

    update = install
