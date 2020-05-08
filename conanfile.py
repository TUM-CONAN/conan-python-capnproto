import os

from conans import ConanFile, tools


class PythonCapnprotoConan(ConanFile):
    name = "python-capnproto"
    version = tools.get_env("GIT_TAG", "1.0-dev")
    license = "Apache"
    description = ("Python bindings for capnproto")
    settings = "os", "compiler", "build_type", "arch"

    scm = {
        "type": "git",
        "subfolder": "pycapnp-%s" % version,
        "url": "https://github.com/capnproto/pycapnp.git",
        "revision": "master"
     }

    # def source(self):
    #     tools.get("https://github.com/capnproto/pycapnp/archive/v%s.tar.gz" % self.version)

    def build_requirements(self):
        self.build_requires("generators/1.0.0@camposs/stable")
        self.build_requires("python-setuptools/[>=41.2.0]@camposs/stable")
        self.build_requires("python-pip/[>=19.2.3]@camposs/stable")

    def requirements(self):
        self.requires("python/[>=3.8.2]@camposs/stable")
        self.requires("python-setuptools/41.2.0@camposs/stable")
        self.requires("python-pip/[>=19.2.3]@camposs/stable")
        self.requires("cython/0.29.16@camposs/stable")
        self.requires("capnproto/0.8.0@camposs/stable")

    def build(self):
        py_path = os.path.join(self.package_folder, "lib", "python3.8", "site-packages")
        env = {
            "PYTHONPATH": os.environ["PYTHONPATH"] + os.pathsep + py_path + os.pathsep + os.pathsep.join(self.deps_env_info["cython"].PYTHONPATH),
            "PATH": os.environ["PATH"] + os.pathsep + os.pathsep.join(self.deps_env_info["cython"].PATH) + os.pathsep + os.pathsep.join(self.deps_env_info["python"].PATH),
        }

        os.makedirs(py_path)
        with tools.chdir("pycapnp-" + self.version), tools.environment_append(env):
            self.run('python3 -c "import sys; print(sys.path)"')
            self.run('python3 setup.py install --optimize=1 --prefix= --root="%s"' % self.package_folder)

    def package_info(self):
        self.env_info.PYTHONPATH.append(os.path.join(self.package_folder, "lib", "python3.8", "site-packages"))
