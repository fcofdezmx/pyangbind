#!/usr/bin/env python

import sys
import os
import getopt

TESTNAME="list-tc01"

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "k", ["keepfiles"])
  except getopt.GetoptError as e:
    print str(e)
    sys.exit(127)

  k = False
  for o, a in opts:
    if o in ["-k", "--keepfiles"]:
      k = True

  pyangpath = os.environ.get('PYANGPATH') if os.environ.get('PYANGPATH') is not None else False
  pyangbindpath = os.environ.get('PYANGBINDPATH') if os.environ.get('PYANGBINDPATH') is not None else False
  assert not pyangpath == False, "could not find path to pyang"
  assert not pyangbindpath == False, "could not resolve pyangbind directory"

  this_dir = os.path.dirname(os.path.realpath(__file__))
  print "%s --plugindir %s -f pybind -o %s/bindings.py %s/%s.yang" % (pyangpath, pyangbindpath, this_dir, this_dir, TESTNAME)
  os.system("%s --plugindir %s -f pybind -o %s/bindings.py %s/%s.yang" % (pyangpath, pyangbindpath, this_dir, this_dir, TESTNAME))


  from bindings import list_tc01 as ytest
  from xpathhelper import YANGPathHelper
  yhelper =  YANGPathHelper()
  yobj = ytest(path_helper=yhelper)

  t1_leaflist(yobj,tree=yhelper)
  t2_list(yobj,tree=yhelper)

  if not k:
    os.system("/bin/rm %s/bindings.py" % this_dir)
    os.system("/bin/rm %s/bindings.pyc" % this_dir)

def t1_leaflist(yobj,tree=False):
  del_tree = False
  if not tree:
    del_tree = True
    tree = YANGPathHelper()

  for a in ["mackerel", "trout", "haddock", "flounder"]:
    yobj.container.t1.append(a)

  for tc in [("mackerel", True), ("haddock", True), ("minnow", False)]:
    validref = False
    try:
      yobj.reference.t1_ptr = tc[0]
      validref = True
    except ValueError:
      pass
    assert validref == tc[1], "Reference was incorrectly set for a leaflist" + \
        " (%s not in %s -> %s != %s)" % (tc[0], str(yobj.container.t1), validref, tc[1])

  if del_tree:
    del tree

def t2_list(yobj,tree=False):
  del_tree = False
  if not tree:
    del_tree = True
    tree = YANGPathHelper()

  for o in ["kangaroo", "wallaby", "koala", "dingo"]:
    yobj.container.t2.add(o)

  for tc in [("kangaroo", True), ("koala", True), ("wombat", False)]:
    validref = False
    try:
      yobj.reference.t2_ptr = tc[0]
      validref = True
    except ValueError:
      pass
    assert validref == tc[1], "Reference was incorrectly set for a list" + \
      " (%s not in %s -> %s ! %s)" % (tc[0], yobj.container.t2.keys(), validref, tc[1])


if __name__ == '__main__':
  import_path = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/../..")
  sys.path.insert(0, import_path)
  from xpathhelper import YANGPathHelper, XPathError
  main()
