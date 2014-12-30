from os import makedirs
from os.path import dirname
from shutil import copyfile

def ckan_extension_template(name, target_src):
    """
    Create ckanext-(name) in target_src directory.
    """
    setupdir = '{0}/ckanext-{1}'.format(target_src, name)
    extdir = setupdir + '/ckanext/{0}'.format(name)
    templatedir = extdir + '/templates/'
    staticdir = extdir + '/static/datacats'

    makedirs(templatedir + '/home/snippets')
    makedirs(staticdir)

    here = dirname(__file__)
    copyfile(here + '/chart.png', staticdir + '/chart.png')
    copyfile(here + '/datacats-footer.png', staticdir + '/datacats-footer.png')

    filecontents = [
        (setupdir + '/setup.py', SETUP_PY),
        (setupdir + '/.gitignore', DOT_GITIGNORE),
        (setupdir + '/ckanext/__init__.py', NAMESPACE_PACKAGE),
        (extdir + '/__init__.py', ''),
        (extdir + '/plugins.py', PLUGINS_PY),
        (templatedir + '/home/snippets/promoted.html', PROMOTED_SNIPPET),
        ]

    for filename, content in filecontents:
        with open(filename, 'w') as f:
            f.write(content.replace('##name##', name))

NAMESPACE_PACKAGE = '''# this is a namespace package
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)
'''

SETUP_PY = '''#!/usr/bin/env/python
from setuptools import setup

setup(
    name='ckanext-##name##',
    version='0.1',
    description='',
    license='AGPL3',
    author='',
    author_email='',
    url='',
    namespace_packages=['ckanext'],
    packages=['ckanext.##name##'],
    zip_safe=False,
    entry_points = """
        [ckan.plugins]
        ##name##_skin = ckanext.##name##.plugins:CustomSkin
    """
)
'''

PLUGINS_PY = '''
from ckan.plugins import toolkit, IConfigurer, SingletonPlugin, implements

class CustomSkin(SingletonPlugin):
    implements(IConfigurer)

    def update_config(self, config):
        toolkit.add_template_directory(config, "templates")
        toolkit.add_public_directory(config, "static")
'''

DOT_GITIGNORE = '''
*.pyc
ckanext_##name##.egg-info/*
build/*
dist/*
'''

PROMOTED_SNIPPET = '''{% set intro = g.site_intro_text %}

<div class="module-content box">
  <header>
    {% if intro %}
      {{ h.render_markdown(intro) }}
    {% else %}
      <h1 class="page-heading">{{ _("New Data Catalog") }}</h1>
      <p>
        {% trans %}
        Welcome to your new data catalog!
        <a href="/user/login">Log in</a> with the
        "admin" account password you created, then create a
        <a href="/dataset/new">new dataset</a> or a
        <a href="/organization/new">new organization</a>.
        {% endtrans %}
      </p>
      <p>
        {% trans %}
        Edit your catalog configuration such as the
        site title by opening the <code>"conf/ckan.ini"</code>
        file in a text editor. Reload your configuration
        with the command: <code>datacats reload</code>
        {% endtrans %}
      </p>
      <p>
        {% trans %}
        This site has been customized by a new CKAN extension
        created for you: <code>ckanext-##name##</code>.
        This extension redefines some HTML templates and adds
        static image files. Edit these files and add your own
        to the directories:
        <code>src/ckanext-##name##/ckanext/##name##/templates</code>
        and <code>src/ckanext-##name##/ckanext/##name##/static</code>
        then reload your changes with: <code>datacats reload</code>
        {% endtrans %}
      </p>
    {% endif %}
  </header>

  {% block home_image %}
    <section class="featured media-overlay hidden-phone">
      <h2 class="media-heading">{% block home_image_caption %}{{ _("This is a featured section") }}{% endblock %}</h2>
      {% block home_image_content %}
        <a class="media-image" href="#">
          <img src="{{ h.url_for_static('/datacats/chart.png') }}" alt="Example chart" width="420" height="220" />
        </a>
      {% endblock %}
    </section>
  {% endblock %}
</div>
'''
