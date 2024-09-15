# sopel-npm

Sopel plugin to handle NPM links/searches

## Installing

Releases are hosted on PyPI, so after installing Sopel, all you need is `pip`:

```shell
$ pip install sopel-npm
```

## Using

`sopel-npm` offers two main features: link handling, and a search command.

### Link handling

If someone posts a link to a package on npmjs.com, `sopel-npm` should emit an
overview of that package's latest version:

```
<dgw> https://www.npmjs.com/package/plyr
<Sopel> [npm] plyr@3.7.8 | Published by sam_potts | MIT license | Unpacked
        size: 5.1 MiB in 124 files | A simple, accessible and customizable
        HTML5, YouTube and Vimeo media player
```

Links directly to a specific package version will show information for that
release instead:

```
<dgw> https://www.npmjs.com/package/plyr/v/2.0.18
<Sopel> [npm] plyr@2.0.18 | Published by sampotts | MIT license | A simple,
        accessible and customizable HTML5, YouTube and Vimeo media player
```

### `.npm` search command

Use `.npm keywords here` and `sopel-npm` will show details for the best match
as returned by the NPM registry's search engine:

```
<dgw> .npm best vue plugin
<Sopel> [npm] eslint-plugin-pinia@0.4.1 | Published by lisilinhart | MIT
        license | Unpacked size: 47.4 KiB in 8 files | ESLint plugin for Pinia
        best practices | https://www.npmjs.com/package/eslint-plugin-pinia
```

This feature will always show details for the latest version of the matching
package, if any.

### Robustness

NPM metadata has evolved over time, and the registry doesn't normalize metadata
for old releases. `sopel-npm` does its best to cope with missing data fields and
return _something_ useful, even if it's not complete.

[Bug reports][issue-tracker] or [pull requests][pull-requests] are welcome if
you run into a situation that this plugin can't handle gracefully!

[issue-tracker]: https://github.com/dgw/sopel-npm/issues
[pull-requests]: https://github.com/dgw/sopel-npm/pulls
