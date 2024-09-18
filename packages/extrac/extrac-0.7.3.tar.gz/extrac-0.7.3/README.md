# extrac
[![PyPI version](https://img.shields.io/pypi/v/extrac?style=for-the-badge)](https://pypi.org/project/extrac/) [![License](https://img.shields.io/github/license/belingud/python_extrac.svg?style=for-the-badge)](https://opensource.org/licenses/MIT) ![Static Badge](https://img.shields.io/badge/language-Python-%233572A5?style=for-the-badge) ![PyPI - Downloads](https://img.shields.io/pypi/dm/extrac?logo=pypi&style=for-the-badge)


Homepage: https://github.com/belingud/python_extrac

One magic word to unpack archive, pure python implementation, no command-line tools required.

一个命令解压所有压缩文件，纯Python实现，不依赖任何命令行工具。

> Support 7z(.7z),AR(.a,.ar),RAR(.rar),ZIP(.zip,.jar),TAR(.tar.gz,.tgz,.tar.bz
  ,.tar.bz2,.tbz,.tbz2,.tar.xz,.txz),GZIP(.gz),compress(.Z),CAB(.cab),XZ(.xz,.
  lzma),BZIP2(.bz2),BZIP(.bz),ZSTD(.zstd,.zst),DEB(deb) archives for now.
>
> 目前支持7z(.7z),AR(.a,.ar),RAR(.rar),ZIP(.zip,.jar),TAR(.tar.gz,.tgz,.tar.bz
  ,.tar.bz2,.tbz,.tbz2,.tar.xz,.txz),GZIP(.gz),compress(.Z),CAB(.cab),XZ(.xz,.
  lzma),BZIP2(.bz2),BZIP(.bz),ZSTD(.zstd,.zst),DEB(deb) 后缀的压缩文件。

# Install

Recommended installation with pipx:

```shell
$ pipx install extrac
  installed package extrac x.x.x, installed using Python 3.12.3
  These apps are now globally available
    - extrac
    - x
done! ✨ 🌟 ✨
```

Support Format:

- [x] .ar/.a
- [x] .bz2/.bz/.dmg
- [x] .cab
- [x] .gz
- [x] .xz
- [x] .7z
- [x] .Z
- [x] .tar.gz/.tgz
- [x] .tar.bz/.tbz
- [x] .tar.xz/.txz
- [x] .tar
- [x] .rar
- [x] .zip/.jar
- [x] .zstd/.zst
- [x] .deb
- [x] .xz/.lzma
- [ ] .arj
- [ ] .rp
- [ ] .pkg

Usage:

Contains two commands x and extrac.

> Not support specified output filename yet

```shell
# Auto extract to current directory as sample/
x test/archives/sample.zip
extrac test/archives/sample.zip
# Specified output directory as test/sample/
x test/archives/sample.tar.bz test/
extrac test/archives/sample.tar.bz test/
```

# TO BE CONTINUE

# 未完待续
