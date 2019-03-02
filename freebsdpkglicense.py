#!/usr/bin/env python3
import subprocess
import json
import sys

chkedPkg={}

class PkgInfo:
    name=""
    lincenses=None
    deps2=None

def getInfo(pkgname):
    cmdstr="pkg search -R --raw-format json ^{}$".format(pkgname)
    proc = subprocess.run(cmdstr,stdout=subprocess.PIPE,shell=True)
    pkginfostr=proc.stdout.decode("utf8")
    pkginfo = json.JSONDecoder().decode(pkginfostr)
    rv=PkgInfo()
    rv.name=pkginfo["name"]
    rv.version=pkginfo["version"]
    rv.licenses=pkginfo["licenses"]
    if "deps" in pkginfo.keys():
        rv.deps2=pkginfo["deps"]
    else :
        rv.deps2=None
    return rv


def getAllInfo(pkgInfo):
    chkedPkg_key=pkgInfo.name+"-"+pkgInfo.version
    if chkedPkg_key in chkedPkg.keys():
        return
    chkedPkg[chkedPkg_key]=True
    for license in pkgInfo.licenses:
        for l in license.split(","):
            print("\""+chkedPkg_key+"\",\""+l.strip()+"\"")
    if pkgInfo.deps2 is None:
        return
    for pkgName in pkgInfo.deps2.keys():
        pkgVer=pkgInfo.deps2[pkgName]["version"]
        fullPkgName=pkgName+"-"+pkgVer
        nextPkgInfo=getInfo(fullPkgName)
        getAllInfo(nextPkgInfo)
        
if len(sys.argv)!=2 :
    print("usage: freebsdpkglicense pkgname")
    exit()
    
pkgname=sys.argv[1].strip()

pkgInfo=getInfo(pkgname)
getAllInfo(pkgInfo)

